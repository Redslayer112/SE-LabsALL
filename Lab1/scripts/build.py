#!/usr/bin/env python3
"""Build the three Lab-1 PDF deliverables into exports/.

Markdown docs -> python-markdown -> headless Chromium print-to-pdf.
.drawio       -> draw.io desktop app CLI export.
"""
import base64, glob, os, subprocess, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(R, "exports")
TMP = os.path.join(R, ".build")

STUDENT = {"NAME": "________________", "SRN": "________________", "SECTION": "____"}

CSS = """
@page{size:A4 %(orient)s;margin:14mm 12mm}
body{font-family:"DejaVu Sans",Helvetica,Arial,sans-serif;font-size:%(fs)s;line-height:1.45;color:#111}
h1{font-size:19px;margin:0 0 4px;border-bottom:2px solid #333;padding-bottom:5px}
h2{font-size:15px;margin:16px 0 6px;color:#1a3d6d}
h3{font-size:13px;margin:14px 0 5px;color:#1a3d6d}
table{border-collapse:collapse;width:100%%;margin:8px 0;table-layout:%(tlayout)s}
th,td{border:1px solid #999;padding:5px 6px;vertical-align:top;word-wrap:break-word}
th{background:#e8eef6;font-weight:700;text-align:left}
th:nth-child(1){width:7%%}th:nth-child(2){width:11%%}th:nth-child(3){width:25%%}
th:nth-child(4){width:8%%}th:nth-child(5){width:29%%}th:nth-child(6){width:20%%}
thead{display:table-header-group}
tr{page-break-inside:avoid}
hr{border:0;border-top:1px solid #bbb;margin:12px 0}
ol,ul{margin:6px 0 6px 20px;padding:0}li{margin:3px 0}
code{background:#f2f2f2;padding:1px 3px}
img{max-width:100%%;height:auto;display:block;margin:10px auto}
"""


def chromium(src_html, out_pdf):
    for exe in ("chromium", "chromium-browser", "google-chrome"):
        try:
            subprocess.run([exe, "--headless", "--disable-gpu", "--no-sandbox",
                            "--no-pdf-header-footer", "--virtual-time-budget=25000",
                            "--print-to-pdf=" + out_pdf, "file://" + src_html],
                           capture_output=True, timeout=240, check=True)
            print("  ->", os.path.relpath(out_pdf, R), os.path.getsize(out_pdf), "bytes")
            return
        except FileNotFoundError:
            continue
    sys.exit("no chromium/chrome binary found")


def md_pdf(md, out, orient="portrait", fs="10px", tlayout="fixed", extra_css="", subs=None):
    import markdown
    raw = open(os.path.join(R, md)).read()
    for k, v in (subs or {}).items():
        raw = raw.replace(k, v)
    body = markdown.markdown(raw, extensions=["tables", "sane_lists"])
    style = CSS % {"orient": orient, "fs": fs, "tlayout": tlayout}
    if tlayout == "auto":  # narrow metadata tables, not the requirements grid
        style += "table{width:auto}thead{display:none}td:first-child{background:#f4f7fb;white-space:nowrap}"
    style += extra_css
    page = os.path.join(TMP, os.path.basename(out) + ".html")
    open(page, "w").write('<meta charset="utf-8"><style>%s</style>%s' % (style, body))
    print(md)
    chromium(page, os.path.join(OUT, out))
    return page


def docx(src_html, out, tw=1028):
    """Convert the rendered HTML to .docx (handout asks for Word/Excel)."""
    # LibreOffice's HTML importer ignores CSS cell borders, so restate them as legacy
    # table attributes and widen the ID column, which renders narrower in Word than in Chromium.
    h = open(src_html).read()
    # LibreOffice ignores CSS nth-child widths, so state them as a <colgroup> instead.
    # LibreOffice ignores CSS nth-child widths and mis-scales colgroup percentages,
    # so give it absolute px summing to the landscape text width (~273mm at 96dpi).
    cols = "".join('<col width="%d">' % round(tw * f) for f in
                   (.076, .109, .243, .086, .292, .194))
    h = h.replace("<table>", '<table border="1" cellspacing="0" cellpadding="3" width="%d">' % tw +
                             '<colgroup>%s</colgroup>' % cols)
    src_html = src_html.replace(".html", ".docx.html")
    open(src_html, "w").write(h)
    subprocess.run(["soffice", "--headless", "--convert-to", "docx:MS Word 2007 XML",
                    "--outdir", TMP, src_html], capture_output=True, timeout=300, check=True)
    made = os.path.join(TMP, os.path.splitext(os.path.basename(src_html))[0] + ".docx")
    dest = os.path.join(OUT, out)
    os.replace(made, dest)
    print("  ->", os.path.join("exports", out), os.path.getsize(dest), "bytes")


def data_uri(name):
    """Inline the image: LibreOffice links rather than embeds an <img src> path,
    which would leave the .docx with a broken reference on any other machine."""
    with open(os.path.join(OUT, name), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def _drawio(src, out, fmt, extra=None):
    """Export via the draw.io desktop app's own CLI (set $DRAWIO to override)."""
    app = os.environ.get("DRAWIO") or next(
        (p for p in glob.glob(os.path.expanduser("~/Downloads/drawio-*.AppImage"))
         + ["/usr/bin/drawio", "/opt/drawio/drawio"] if os.path.exists(p)), None)
    if not app:
        sys.exit("draw.io app not found - set $DRAWIO to the AppImage or binary")
    print(src)
    subprocess.run([app, "--export", "--format", fmt, "--crop", "--border", "20"] + (extra or []) +
                   ["--output", os.path.join(OUT, out), os.path.join(R, src)],
                   capture_output=True, timeout=300, check=True)
    print("  ->", os.path.join("exports", out), os.path.getsize(os.path.join(OUT, out)), "bytes")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    _drawio("use-case-diagram.drawio", "use-case-diagram.png", "png", ["--scale", "2"])
    docx(md_pdf("requirements-table.md", "requirements-table.pdf", "landscape", "9px"),
         "requirements-table.docx")
    docx(md_pdf("use-case-flow.md", "use-case-flow.pdf", "portrait", "10px", tlayout="auto"),
         "use-case-flow.docx")
    _drawio("use-case-diagram.drawio", "use-case-diagram.pdf", "pdf")
    docx(md_pdf("final-report.md", "LAB1_SE_Final_Report.pdf", "portrait", "10px",
                extra_css="table{font-size:7.4px}td,th{padding:3px 4px}"
                          "h1{font-size:22px;text-align:center;border:0}"
                          "h2{font-size:14px;margin-top:18px;border-bottom:1px solid #999;padding-bottom:3px}",
                subs={"USE_CASE_DIAGRAM_PNG": data_uri("use-case-diagram.png"),
                      "{{NAME}}": STUDENT["NAME"], "{{SRN}}": STUDENT["SRN"],
                      "{{SECTION}}": STUDENT["SECTION"]}),
         "LAB1_SE_Final_Report.docx", tw=703)
