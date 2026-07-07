"""Genere rapport_evaluation.pdf a partir de la source editable rapport_evaluation.md.

Usage :
    python generate_report.py
"""

from __future__ import annotations

from pathlib import Path

import markdown
from xhtml2pdf import pisa

SOURCE_MD = Path("rapport_evaluation.md")
OUTPUT_PDF = Path("rapport_evaluation.pdf")

CSS = """
<style>
body { font-family: Helvetica, sans-serif; font-size: 11pt; line-height: 1.4; }
h1 { font-size: 18pt; margin-top: 0; }
h2 { font-size: 14pt; margin-top: 20px; border-bottom: 1px solid #ccc; }
h3 { font-size: 12pt; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; }
th, td { border: 1px solid #999; padding: 6px 8px; text-align: left; white-space: nowrap; }
th { background-color: #eee; }
img { max-width: 350px; }
blockquote { color: #444; border-left: 3px solid #ccc; padding-left: 10px; margin-left: 0; }
</style>
"""


def main() -> None:
    md_text = SOURCE_MD.read_text(encoding="utf-8")
    body_html = markdown.markdown(md_text, extensions=["tables"])
    html = f"<html><head>{CSS}</head><body>{body_html}</body></html>"

    with open(OUTPUT_PDF, "wb") as f:
        result = pisa.CreatePDF(html, dest=f)

    if result.err:
        raise RuntimeError(f"Erreur lors de la generation du PDF ({result.err} erreurs).")

    print(f"Rapport genere : {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
