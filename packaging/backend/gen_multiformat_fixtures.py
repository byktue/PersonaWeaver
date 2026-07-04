# -*- coding: utf-8 -*-
"""用神游前 10 章文本生成 pdf/docx/epub 三种测试素材，供多源解析全链路验证。

- docx / epub：用标准库 zipfile 构造最小合法文件（与单测同法，无需第三方库）。
- pdf：用 pypdf 无法"写"文本，改用 reportlab 太重；这里用 fpdf2 若可用，否则跳过 pdf。
  实际上后端 pdf_parser 用 pypdf 读取，需要一个含真实文本的 pdf。用一个最小手写 PDF。

输出到 data/_multiformat_test/ 下。
"""
from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "data" / "book_6619b9d7_神游.txt" / "first_10_chapters.txt"
OUT = REPO / "data" / "_multiformat_test"
OUT.mkdir(parents=True, exist_ok=True)

text = SRC.read_text(encoding="utf-8")
# 取前 3 章体量，避免 pdf 手写过大；docx/epub 用全量前10章
chapters = text.split("\n\n")
sample = "\n\n".join(chapters[:40])  # 约前几章内容


def make_docx(path: Path, body: str) -> None:
    paras = [p.strip() for p in body.split("\n") if p.strip()]
    xml_paras = "".join(
        f"<w:p><w:r><w:t xml:space=\"preserve\">{_xml_escape(p)}</w:t></w:r></w:p>"
        for p in paras
    )
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{xml_paras}</w:body></w:document>"
    )
    with ZipFile(path, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",
                   '<?xml version="1.0" encoding="UTF-8"?>'
                   '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                   '</Types>')
        z.writestr("word/document.xml", document_xml)


def make_epub(path: Path, body: str) -> None:
    paras = [p.strip() for p in body.split("\n") if p.strip()]
    html_body = "".join(f"<p>{_xml_escape(p)}</p>" for p in paras)
    chapter_xhtml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<html xmlns="http://www.w3.org/1999/xhtml"><body>'
        f"{html_body}</body></html>"
    )
    with ZipFile(path, "w", ZIP_DEFLATED) as z:
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0" encoding="UTF-8"?>'
                   '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                   '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>'
                   '</container>')
        z.writestr("OEBPS/content.opf",
                   '<?xml version="1.0" encoding="UTF-8"?>'
                   '<package xmlns="http://www.idpf.org/2007/opf" version="3.0">'
                   '<manifest><item id="c1" href="c1.xhtml" media-type="application/xhtml+xml"/></manifest>'
                   '<spine><itemref idref="c1"/></spine></package>')
        z.writestr("OEBPS/c1.xhtml", chapter_xhtml)


def make_pdf(path: Path, body: str) -> None:
    """用 fpdf2 生成含中文文本的 pdf（若不可用则报错提示）。"""
    try:
        from fpdf import FPDF
    except ImportError:
        raise SystemExit("需要 fpdf2 才能生成中文 PDF：pip install fpdf2")
    pdf = FPDF()
    pdf.add_page()
    # 用系统中文字体
    import glob
    font_candidates = glob.glob(r"C:\Windows\Fonts\msyh*.tt*") + glob.glob(r"C:\Windows\Fonts\simsun.tt*")
    if not font_candidates:
        raise SystemExit("未找到中文字体")
    pdf.add_font("cn", "", font_candidates[0])
    pdf.set_font("cn", size=12)
    epw = pdf.epw  # 有效页宽
    for line in body.split("\n"):
        line = line.strip()
        if not line:
            continue
        # 中文无空格，按每 30 字硬切，避免 multi_cell 无法断行
        for i in range(0, len(line), 30):
            pdf.multi_cell(epw, 8, line[i:i + 30])
    pdf.output(str(path))


def _xml_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


if __name__ == "__main__":
    make_docx(OUT / "神游.docx", sample)
    print("docx OK:", (OUT / "神游.docx").stat().st_size, "bytes")
    make_epub(OUT / "神游.epub", sample)
    print("epub OK:", (OUT / "神游.epub").stat().st_size, "bytes")
    make_pdf(OUT / "神游.pdf", sample)
    print("pdf OK:", (OUT / "神游.pdf").stat().st_size, "bytes")
