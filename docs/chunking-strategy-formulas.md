# 长篇文本切分策略优化公式

## 目标

CHARPICK 的文本处理分为两层：本地切分层保留细粒度章节、段落和证据片段；模型调用层把相邻片段拼成更大的任务包。这样既能保留后续 RAG 和角色证据追溯所需的细粒度结构，也能减少 vivo AIGC 或校园 API 的调用次数。

## 成本模型

设一次模型调用的总成本为：

```text
C_call = C_fixed + C_input + C_output
```

其中：

```text
C_input = P_in * T_input
C_output = P_out * T_output
```

`C_fixed` 表示每次请求都会重复消耗的系统提示词、任务说明、JSON 约束和网络开销。若把 10 章拆成 10 次调用，`C_fixed` 会重复 10 次；若 10 章合并成 1 次调用，`C_fixed` 只出现 1 次。因此，过细的模型调用通常不划算。

更适合的调用单元满足：

```text
T_prompt + T_block + T_expected_output <= T_model_limit * r_safe
```

推荐：

```text
r_safe = 0.65 ~ 0.75
```

其中 `T_model_limit` 是模型上下文窗口，`r_safe` 是安全系数，用来给模型推理、格式修复和异常冗余留空间。

## 最优合并粒度

对第 `i` 个本地片段，记 token 数为 `t_i`。一个模型调用任务包 `B_k` 包含从 `a` 到 `b` 的连续片段：

```text
B_k = {s_a, s_{a+1}, ..., s_b}
```

它需要满足：

```text
sum(t_i, i=a..b) + T_prompt + T_schema + T_output_budget <= T_budget
```

其中：

```text
T_budget = T_model_limit * r_safe
```

在满足预算的前提下，优先让 `B_k` 尽可能大：

```text
maximize |B_k|
```

但同一任务包不应该跨越明显的叙事断点，例如卷末、篇章转场、主线切换或角色视角切换。可加入语义惩罚项：

```text
Score(B_k) = α * Coverage(B_k) - β * BoundaryPenalty(B_k) - γ * OutputRisk(B_k)
```

其中：

```text
Coverage(B_k) = sum(t_i) / T_budget
BoundaryPenalty(B_k) = 跨越强叙事边界的次数
OutputRisk(B_k) = 预计输出过长或 JSON 失真的风险
```

推荐初始权重：

```text
α = 1.0
β = 0.4
γ = 0.3
```

## 推荐策略

### 本地切分

本地仍按细粒度切分：

```text
原文 -> 章节 -> 段落 -> RAG chunk
```

该层目标不是省调用次数，而是保留可追溯证据。每个片段应保存：

```text
book_id
chapter_index
chapter_title
paragraph_index
source_start
source_end
content_hash
```

### 模型调用

模型调用层按批合并：

```text
5 ~ 10 章 / 次
```

若章节很短，可以提高到 10 章以上；若章节很长，则单章内部再按 token 拆分。初始规则：

```text
if avg_chapter_tokens < 1200:
    batch_size = 10
elif avg_chapter_tokens < 2500:
    batch_size = 5
else:
    batch_size = 1 ~ 3
```

对 10 章小样本，建议直接合并成 1 个任务包做联通测试。

### 结果回写

模型返回的结构化结果不能只保存为一个大结果，应回写到原始细粒度索引：

```text
模型批处理结果 -> chapter_index / paragraph_index / evidence_text
```

这样后续生成角色卡、剧情时间线和 RAG 检索时，仍能追溯到原章节和证据片段。

## 调用次数估算

设全书共有 `N` 章，每个调用任务包平均包含 `k` 章，则调用次数约为：

```text
Q = ceil(N / k)
```

若每章单独调用：

```text
Q_single = N
```

节省比例：

```text
Saving = 1 - Q / Q_single
```

例如 100 章小说：

```text
k = 1  -> Q = 100
k = 5  -> Q = 20, Saving = 80%
k = 10 -> Q = 10, Saving = 90%
```

这就是“细存储、粗调用、再回写”的成本优势。

## 交互阶段拼接

交互问答阶段不应重新扫描全文，也不应逐 chunk 调模型。推荐流程：

```text
用户问题 -> RAG 检索 top_k chunk -> 证据重排 -> 拼接为一次 prompt -> 调用 vivo / 校园 API
```

拼接预算：

```text
T_question + T_system + sum(T_chunk_j) + T_answer_budget <= T_interaction_budget
```

若检索结果过多，使用以下排序：

```text
Rank(chunk) = λ1 * Similarity + λ2 * Recency + λ3 * CharacterMatch + λ4 * PlotImportance
```

推荐初始值：

```text
λ1 = 0.55
λ2 = 0.10
λ3 = 0.20
λ4 = 0.15
```

## 当前项目落地建议

当前阶段使用以下默认策略：

```text
本地切分：保持逐章和 RAG chunk 细粒度
联通测试：10章小样本合并为1次调用
L2章节抽取：5到10章合并为1次调用，结果再拆回章节
Summary汇总：沿用全局上下文，但限制每章摘要长度
角色卡生成：只拼接目标角色相关证据
交互问答：RAG top_k 证据拼接后一次调用
```

短期实现优先级：

1. vivo provider 连通。
2. 10章样本合并调用 smoke test。
3. 在 L2 调度层加入 batch_size 参数。
4. 批处理结果保留 chapter_index 和 evidence 字段。
5. 根据真实 token 消耗调整 batch_size。

## 风险控制

模型调用任务包过大时，容易出现 JSON 截断、字段遗漏或输出过长。可用以下规则降级：

```text
if parse_failed or output_truncated:
    retry with smaller batch_size
```

建议最大重试 2 次：

```text
batch_size -> ceil(batch_size / 2) -> 1
```

如果 vivo 返回限流或当日额度耗尽：

```text
vivo -> remote_api / ecnu
```

如果两个远程 provider 都不可用，再提示用户降低批量、换 key 或稍后重试。
