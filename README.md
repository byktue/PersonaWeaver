# submission_llm_core —— 核心大模型调用代码包

本代码包是 **PersonaWeaver（灵织）** 长文本角色资产提取系统中「调用大模型」的核心链路，从主项目 `CharPick/backend/` 精选、脱敏而来，可独立运行、不含任何真实密钥、不依赖数据库或对象存储。

## 一、它做什么

输入一本小说（txt/md/pdf/docx/epub），完成从原文到结构化角色资产的三级大模型调用：

| 任务 | 命令 | 说明 |
| :--- | :--- | :--- |
| **章节提取（L2）** | `chapter` | 逐章调用 LLM，提取章节信息 / 剧情 / 角色 / 物品 / 世界观等维度，输出结构化 JSON |
| **整书汇总** | `summary` | 基于全部章节 JSON，汇总角色总表、物品总表、剧情时间线、世界观地点 |
| **角色卡生成** | `card` | 基于章节证据为指定角色生成 Markdown 角色展示卡 |
| **全文基准评测** | `benchmark_fulltext` | 逐章提取 vs 全文一次性直提，做质量与效率对比 |

## 二、目录结构

```
submission_llm_core/
├─ backend/                              # 保留原命名空间，代码零改动
│   ├─ llm_dispatcher.py                 # 章节/汇总/角色卡三级派发 CLI 入口
│   ├─ config.json                       # Prompt 全量 + provider 元信息（env 占位，无硬编码 key）
│   ├─ llm_dispatch/                     # 统一 LLM client（vivo / OpenAI 兼容 / ollama）
│   ├─ llm_chapter_extraction/           # 章节结构化提取
│   ├─ source_preprocess/                # L0/L1：编码归一、清洗、章节切分、多源输入适配(txt/md/pdf/docx/epub)
│   └─ benchmark_fulltext.py             # 全文 vs 逐章基准评测
├─ .env.example                          # 环境变量占位模板
├─ requirements.txt                      # requests + chardet + pypdf
├─ README.md                             # 本文档
└─ 使用说明.md                            # 一分钟中文上手
```

## 三、调用链

```
CLI (llm_dispatcher.py)
  → build_chapter_dispatch_from_source
      → source_preprocess.process_source_file   # L0/L1：解码→清洗→切章
      → dispatch_chapter_prompts
          → llm_chapter_extraction.extractor_client.call_ollama_json
              → llm_dispatch.llm_client.call_llm_json  # 按 provider 分发到 vivo / remote_api / glm / ollama
```

所有 provider 的 `base_url` / `api_key` / `model` 均通过 `config.json` 的 `*_env` 字段索引环境变量，运行时从 `.env` 或系统环境变量读入，**代码与配置中无任何硬编码密钥**。

## 四、复现命令（给评审）

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置密钥（三选一填写即可）
cp .env.example .env
# 编辑 .env 填入真实 key

# 3. 运行章节提取（以神游前几章为例）
python -m backend.llm_dispatcher chapter \
    --source-path path/to/神游.txt \
    --source-file-id demo \
    --book-title 神游 \
    --provider vivo
```

> 注意：命令须在 `submission_llm_core/` 目录下执行（保证 `backend` 包可被 `-m` 导入）。

## 五、脱敏说明

- `llm_dispatcher.py` 的 `_load_dotenv_simple` 只从**本代码包根目录**读 `.env`，不回溯主项目；本地无 `.env` 时静默跳过、不加载任何密钥。
- `config.json` 三通道（vivo / remote_api / glm）均用 `*_env` 字段索引环境变量，无硬编码 key，原样复制。
- 仓库仅提供 `.env.example`，且只含 LLM 三组占位（vivo / ECNU / GLM），不含任何 Supabase / OSS 等敏感配置。
- 不含数据库持久化、对象存储、测试与运维脚本，保证独立可跑、零敏感信息。
