"""Generate InsureAssist sample product brochure PDFs from markdown."""

from __future__ import annotations

import re
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
EN_DIR = ROOT.parents[1] / "services" / "api" / "app" / "knowledge" / "approved"
MM_DIR = ROOT / "content" / "mm"
OUT_DIR = ROOT / "pdf"

FONT_EN = Path(r"C:\Windows\Fonts\calibri.ttf")
FONT_EN_B = Path(r"C:\Windows\Fonts\calibrib.ttf")
FONT_MM = Path(r"C:\Windows\Fonts\mmrtext.ttf")
FONT_MM_B = Path(r"C:\Windows\Fonts\mmrtextb.ttf")

NAVY = (15, 23, 42)
BLUE = (29, 78, 216)
SKY = (56, 189, 248)
GOLD = (196, 154, 58)
MUTED = (71, 85, 105)
INK = (15, 23, 42)
RULE = (226, 232, 240)
BANNER_BG = (254, 243, 199)
BANNER_INK = (120, 53, 15)
FOOTER = (100, 116, 139)

PRODUCTS = [
    ("dai_ichi_life_pro.md", "dai-ichi-life-pro"),
    ("dai_ichi_guard.md", "dai-ichi-guard"),
    ("dai_ichi_ci_plus.md", "dai-ichi-ci-plus"),
    ("dai_ichi_active_care.md", "dai-ichi-active-care"),
    ("htar_wa_ra_edu_goal.md", "htar-wa-ra-edu-goal"),
]


def parse_frontmatter(raw: str) -> tuple[dict[str, str], str]:
    text = raw.lstrip("\ufeff")
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    meta: dict[str, str] = {}
    for line in text[3:end].strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip().lower()] = value.strip().strip("\"'")
    return meta, text[end + 4 :].lstrip("\n")


def parse_blocks(body: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    kind, buf = "p", []
    for line in body.splitlines():
        if line.startswith("# "):
            if buf:
                blocks.append((kind, "\n".join(buf).strip()))
                buf = []
            blocks.append(("h1", line[2:].strip()))
            kind = "p"
            continue
        if line.startswith("## "):
            if buf:
                blocks.append((kind, "\n".join(buf).strip()))
                buf = []
            blocks.append(("h2", line[3:].strip()))
            kind = "p"
            continue
        if line.startswith("- "):
            if kind != "ul" and buf:
                blocks.append((kind, "\n".join(buf).strip()))
                buf = []
            kind = "ul"
            buf.append(line[2:].strip())
            continue
        if not line.strip():
            if buf:
                blocks.append((kind, "\n".join(buf).strip()))
                buf = []
            kind = "p"
            continue
        if kind == "ul" and buf:
            blocks.append((kind, "\n".join(buf).strip()))
            buf = []
            kind = "p"
        buf.append(line)
    if buf:
        blocks.append((kind, "\n".join(buf).strip()))
    return [(k, t) for k, t in blocks if t]


class Brochure(FPDF):
    def __init__(self, *, lang: str, product: str, title: str) -> None:
        super().__init__(format="A4", unit="mm")
        self.lang = lang
        self.product = product
        self.doc_title = title
        self.set_auto_page_break(auto=True, margin=22)
        self.set_margins(16, 28, 16)
        if lang == "mm":
            self.add_font("body", "", str(FONT_MM))
            self.add_font("body", "B", str(FONT_MM_B))
            self.set_text_shaping(True)
            self.body_size = 10.5
            self.lead = 6.6
        else:
            self.add_font("body", "", str(FONT_EN))
            self.add_font("body", "B", str(FONT_EN_B))
            self.body_size = 11
            self.lead = 6.2

    def header(self) -> None:
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 22, "F")
        self.set_fill_color(*BLUE)
        self.polygon(((8, 5), (16, 5), (12, 17)), fill=True)
        self.set_fill_color(*SKY)
        self.polygon(((12, 5), (20, 5), (16, 17)), fill=True)
        self.set_text_color(255, 255, 255)
        self.set_font("body", "B", 12)
        self.set_xy(24, 5)
        self.cell(0, 6, "Dai-ichi Life Insurance Myanmar")
        self.set_font("body", "", 8.5)
        self.set_xy(24, 12)
        label = "နမူနာ ထုတ်ကုန် စာရွက်စာတမ်း · InsureAssist" if self.lang == "mm" else "Sample product document  ·  InsureAssist"
        self.set_text_color(186, 198, 216)
        self.cell(0, 5, label)
        self.set_y(28)

    def footer(self) -> None:
        self.set_y(-16)
        self.set_draw_color(*RULE)
        self.set_line_width(0.3)
        self.line(16, self.get_y(), 194, self.get_y())
        self.set_y(-13)
        self.set_font("body", "", 8)
        self.set_text_color(*FOOTER)
        note = "နမူနာစာရွက်စာတမ်း — တရားဝင် အာမခံ စာချုပ် မဟုတ်ပါ" if self.lang == "mm" else "Illustrative sample — not an official policy contract"
        self.cell(0, 5, f"{self.product}  ·  {note}", align="L")
        self.set_xy(160, -13)
        self.cell(34, 5, str(self.page_no()), align="R")

    def h1(self, text: str) -> None:
        self.set_text_color(*NAVY)
        self.set_font("body", "B", 20 if self.lang == "en" else 16)
        self.multi_cell(0, 9, text, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*GOLD)
        self.set_line_width(1.1)
        y = self.get_y()
        self.line(16, y + 1, 72, y + 1)
        self.ln(6)

    def h2(self, text: str) -> None:
        self.ln(2)
        if self.get_y() > 262:
            self.add_page()
        self.set_fill_color(241, 245, 249)
        self.set_text_color(*BLUE)
        self.set_font("body", "B", 12 if self.lang == "en" else 11)
        self.cell(0, 8, f"  {text}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def para(self, text: str, *, banner: bool = False) -> None:
        if banner:
            self.set_fill_color(*BANNER_BG)
            self.set_text_color(*BANNER_INK)
            self.set_font("body", "", 9 if self.lang == "en" else 9.5)
            self.multi_cell(0, 5.6, text, fill=True, new_x="LMARGIN", new_y="NEXT")
            self.ln(4)
            return
        self.set_text_color(*INK)
        self.set_font("body", "", self.body_size)
        self.multi_cell(0, self.lead, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def bullets(self, items: list[str]) -> None:
        self.set_font("body", "", self.body_size)
        for item in items:
            if self.get_y() > 268:
                self.add_page()
            x, y = self.get_x(), self.get_y()
            self.set_fill_color(*GOLD)
            self.ellipse(x + 1.2, y + 2.1, 1.6, 1.6, "F")
            self.set_xy(x + 6, y)
            self.set_text_color(*INK)
            self.multi_cell(172, self.lead, item, new_x="LMARGIN", new_y="NEXT")
            self.ln(0.8)
        self.ln(1.5)


def is_disclaimer(text: str) -> bool:
    return bool(re.search(r"Document status|စာရွက်စာတမ်း အခြေအနေ", text, re.I))


def render(src: Path, out: Path, *, lang: str, slug: str) -> None:
    meta, body = parse_frontmatter(src.read_text(encoding="utf-8"))
    title = meta.get("title") or meta.get("name") or slug
    product = meta.get("name") or slug
    pdf = Brochure(lang=lang, product=product, title=title)
    pdf.add_page()
    pdf.set_title(title)
    pdf.set_author("InsureAssist demo")
    for kind, text in parse_blocks(body):
        if kind == "h1":
            pdf.h1(text)
            summary = meta.get("summary")
            if summary:
                pdf.set_text_color(*MUTED)
                pdf.set_font("body", "", 10.5 if lang == "en" else 10)
                pdf.multi_cell(0, 6.2, summary, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(3)
        elif kind == "h2":
            pdf.h2(text)
        elif kind == "ul":
            pdf.bullets([line for line in text.split("\n") if line.strip()])
        else:
            pdf.para(text, banner=is_disclaimer(text))
    out.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out))
    print(out)


def main() -> None:
    for filename, slug in PRODUCTS:
        render(EN_DIR / filename, OUT_DIR / "en" / f"{slug}-en.pdf", lang="en", slug=slug)
        render(MM_DIR / filename, OUT_DIR / "mm" / f"{slug}-mm.pdf", lang="mm", slug=slug)


if __name__ == "__main__":
    main()
