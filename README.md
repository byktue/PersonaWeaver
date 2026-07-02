# CHARPICK - 长篇网文结构化提取系统

CHARPICK 是一个面向长篇小说、剧本杀文本和角色素材的结构化提取系统。当前后端以 FastAPI 为入口，支持章节切分、角色/剧情/物品/世界观抽取、摘要生成、角色卡生成，以及 RAG 向量检索链路。

当前主流程已不再要求本地 Ollama。为了适配 vivo 竞赛阶段的开发与演示，项目默认先通过校园远程 API 调用模型；Ollama 仅作为旧版兼容或本地兜底路径保留。

## 当前推荐运行方式

### 1. 创建本地环境变量文件

在项目根目录创建 `.env`，用于保存校园 API、数据库、OSS 等本地私密配置。仓库的 `.gitignore` 已经忽略 `.env` 和 `.env.*`，所以真实密钥不会被提交到 GitHub。

可以直接从 `.env.example` 复制：

```bash
copy .env.example .env
```

当前校园 API 的关键配置如下：

```env
ECNU_API_BASE_URL=https://chat.ecnu.edu.cn/open/api/v1/chat/completions
ECNU_API_KEY=<你的校园API密钥>
ECNU_MODEL_NAME=ecnu-max
```

后端会读取根目录 `.env`。不要把真实 API Key 写进 `backend/config.json`、README 或其他会提交的文件。

### 2. 确认后端模型配置

`backend/config.json` 当前默认配置为：

```json
{
  "llm": {
    "provider": "remote_api",
    "remote_api": {
      "base_url_env": "ECNU_API_BASE_URL",
      "api_key_env": "ECNU_API_KEY",
      "model_name_env": "ECNU_MODEL_NAME",
      "base_url": "https://chat.ecnu.edu.cn/open/api/v1/chat/completions",
      "model_name": "ecnu-max"
    }
  }
}
```

也就是说，实际运行时优先读取 `.env` 里的校园 API 配置；如果 `.env` 没有对应值，才使用 `config.json` 中的默认占位配置。

### 3. Conda 环境配置

项目提供 `environment.yml`，其中包含 Python、Node.js 和主要 Python 依赖。

```bash
conda env create -f environment.yml
conda activate charpick
```

如果环境已经创建过，只需激活：

```bash
conda activate charpick
```

也可以用 pip 补装依赖：

```bash
pip install -r requirements.txt
```

### 4. 数据库配置

当前项目支持 PostgreSQL / Supabase PostgreSQL。推荐把连接串放到根目录 `.env`：

```env
SUPABASE_DB_URL=postgresql://postgres.<project-ref>:<db-password>@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres?sslmode=require
DATABASE_URL=postgresql://postgres.<project-ref>:<db-password>@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require
```

RAG 向量库会按以下顺序读取数据库连接：

```text
REMOTE_DB_URL -> SUPABASE_DB_URL -> DATABASE_URL
```

如果只是做本地模型调用或接口 smoke test，可以先不配置数据库；涉及持久化、RAG、用户登录态和远程同步时再补齐。

### 5. 启动 FastAPI 后端

在项目根目录运行：

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

常用接口：

```text
GET  /health
POST /chat
POST /api/v1/extract
GET  /api/v1/tasks/{task_id}
POST /api/v1/rag/chunks/preview
POST /api/v1/rag/index-text
POST /api/v1/rag/query
```

`/chat` 可用于最小化验证校园 API 是否连通。

## 校园 API 连通验证

启动后端后，运行：

```bash
curl -s -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"请简短自我介绍\",\"model\":\"ecnu-max\"}"
```

如果 `.env` 中已经配置 `ECNU_API_KEY`，不需要在请求头里重复传 key。后端会从 `.env` 读取。

也可以临时通过请求头覆盖 key：

```bash
curl -s -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -H "x-api-key: <你的校园API密钥>" \
  -d "{\"message\":\"请简短自我介绍\",\"model\":\"ecnu-max\"}"
```

返回 JSON 中包含 `response` 字段，说明后端已经成功通过校园 API 获得模型输出。

## vivo 竞赛阶段的配置原则

当前 README 按“先用校园 API 跑通主链路”的方式整理。这样做更稳妥：

- 校园 API 已在代码中通过 `remote_api` 路径接入；
- 根目录 `.env` 可以集中保存本地密钥，不污染 GitHub；
- `backend/config.json` 不需要写真实 key；
- 后续正式切换 vivo AIGC API 时，只需要新增或调整 provider 适配层，并把 `VIVO_AIGC_BASE_URL`、`VIVO_AIGC_API_KEY`、`VIVO_AIGC_MODEL` 放进 `.env`。

`.env` 中可以先预留 vivo 配置：

```env
VIVO_AIGC_BASE_URL=<你的vivo AIGC接口地址>
VIVO_AIGC_API_KEY=<你的vivo AIGC密钥>
VIVO_AIGC_MODEL=<你的vivo模型名>
```

在 vivo provider 未完全接入前，不建议把 README 主流程写成本地 Ollama 或 vivo 直连；当前最可靠的主流程是 `remote_api + ECNU_API_*`。

## RAG 与 embedding 配置

默认 RAG embedding 使用 `hash` provider，只用于本地链路验证和数据库写入验证：

```env
RAG_EMBEDDING_PROVIDER=hash
RAG_EMBEDDING_MODEL=hash-embedding-256
RAG_EMBEDDING_DIM=256
RAG_TOP_K=10
```

如果后续切换到校园 embedding 服务或 OpenAI-compatible embedding 服务，再配置：

```env
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_MODEL=<embedding-model-name>
EMBEDDING_DIM=<embedding-dim>
EMBEDDING_BASE_URL=<embedding-endpoint>
EMBEDDING_API_KEY=<embedding-api-key>
```

## 项目结构

```text
backend/
  main.py                         FastAPI 统一接口入口
  config.json                     后端配置，不写真实密钥
  llm_dispatcher.py               L0-L2 流程调度与模型配置解析
  llm_dispatch/llm_client.py      本地/远程模型调用封装
  llm_chapter_extraction/         章节级结构化抽取
  rag/                            RAG chunk、embedding、vector store、retriever
  remote_persistence.py           Supabase / OSS 持久化配置
  source_preprocess/              文本解析、清洗、章节切分
  test/                           后端测试与 smoke test

docs/                             可提交的项目文档
docs_local/                       本地笔记和同步 README，不提交 GitHub
examples/                         示例输入与请求体
.env.example                      环境变量模板
.env                              本地真实配置，不提交 GitHub
```

## 常见问题

### README 里还需要 Ollama 吗

不需要放在主流程里。Ollama 是早期本地 LLM 服务方案，代码中仍有 legacy 兼容逻辑，但现在默认 provider 是 `remote_api`，主流程应以校园 API 为准。

### `.env` 放根目录合适吗

合适。后端启动时会自动读取项目根目录 `.env`，并且 `.gitignore` 已忽略 `.env` 和 `.env.*`。这是保存 API Key、数据库连接串、OSS 密钥最方便也更安全的方式。

### `.env.example` 和 `.env` 的区别是什么

`.env.example` 只放占位符和配置说明，可以提交 GitHub；`.env` 放真实密钥，只保存在本地。

### 校园 API 不通怎么办

先检查三项：

```env
ECNU_API_BASE_URL=https://chat.ecnu.edu.cn/open/api/v1/chat/completions
ECNU_API_KEY=<你的校园API密钥>
ECNU_MODEL_NAME=ecnu-max
```

然后重启 FastAPI 后端，再调用 `/chat` 做最小验证。如果返回 401/403，多半是 key 或权限问题；如果返回 504，多半是远程服务超时，可以调大 `timeout_seconds` 或稍后重试。

## 安全提醒

- 不要提交 `.env`、真实 API Key、数据库密码、OSS 密钥；
- 不要把真实密钥写进 README、`backend/config.json` 或测试文件；
- 如果误提交过密钥，应立即在对应平台重置密钥，并清理 Git 历史。
