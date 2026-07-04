# source_preprocess 多源解析说明

## 职责边界

`source_preprocess` 位于 LLM 提取、RAG、数据库写入之前，负责把上传文件转换为后续流水线可以消费的原始文本。

`parsers` 只做输入源适配：

```text
文件格式 -> 原始文本字符串
```

它不负责文本清洗、章节切分、LLM 调用、RAG 写入、数据库写入和角色卡生成。

## 当前支持格式

| source_type | parser | 说明 |
|---|---|---|
| `txt` | `txt_parser.py` | 自动识别常见编码并输出文本 |
| `md` | `txt_parser.py` | 按普通文本读取 |
| `pdf` | `pdf_parser.py` | 使用 `pypdf` 提取页面文本 |
| `docx` | `docx_parser.py` | 读取 `word/document.xml` 并按段落输出文本 |
| `epub` | `epub_parser.py` | 读取 EPUB spine 中的 XHTML/HTML 章节文本 |

暂不支持旧版二进制 Word `.doc`、图片 OCR、网页抓取。

## 调用方式

统一入口是：

```python
from backend.source_preprocess.parsers import parse_input_to_text

text = parse_input_to_text("examples/inputs/sample.pdf", source_type="pdf")
```

主流程 `backend.source_preprocess.process_source_file(...)` 会在复制或下载源文件后调用同一个 parser 入口。

## 相关文件

```text
backend/source_preprocess/parsers/router.py
backend/source_preprocess/parsers/txt_parser.py
backend/source_preprocess/parsers/pdf_parser.py
backend/source_preprocess/parsers/docx_parser.py
backend/source_preprocess/parsers/epub_parser.py
backend/test/test_source_parsers.py
```

## 验证命令

```bash
pytest backend/test/test_source_parsers.py -q
pytest backend/test/test_source_parsers.py backend/test/test_chapter_chunker.py -q
```
