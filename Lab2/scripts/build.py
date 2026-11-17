#!/usr/bin/env python3
"""Build the Lab-2 report: report.md -> HTML -> .docx (LibreOffice), screenshots inlined.

Same markdown -> HTML -> soffice route as Lab 1, minus the PDF step: the handout
asks for a document and the PDF export is done by hand afterwards.
"""
import base64, os, struct, subprocess

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(R, ".build")
SHOTS = os.path.join(R, "screenshots")

CSS = """
@page{size:A4 portrait;margin:16mm 14mm}
body{font-family:"DejaVu Sans",Helvetica,Arial,sans-serif;font-size:10px;line-height:1.5;color:#111}
h1{font-size:20px;margin:0 0 10px;text-align:center}
h2{font-size:14px;margin:18px 0 6px;color:#1a3d6d}
h3{font-size:12px;margin:14px 0 5px;color:#1a3d6d}
h4{font-size:11px;margin:12px 0 4px;color:#333}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:8.6px}
th,td{border:1px solid #999;padding:4px 5px;vertical-align:top;word-wrap:break-word}
th{background:#e8eef6;font-weight:700;text-align:left;white-space:nowrap}
thead{display:table-header-group}
tr{page-break-inside:avoid}
blockquote{margin:8px 0;padding:6px 10px;background:#f4f7fb;border-left:3px solid #1a3d6d}
blockquote p{margin:0}
hr{border:0;border-top:1px solid #bbb;margin:14px 0}
ol,ul{margin:6px 0 6px 20px;padding:0}li{margin:3px 0}
code{background:#f2f2f2;padding:1px 3px}
p.figtitle{font-size:12px;margin:0 0 6px;page-break-before:always;page-break-after:avoid}
p.shot{margin:0 0 14px;page-break-inside:avoid}
img{max-width:100%;height:auto;display:block;border:1px solid #bbb}
"""

# LibreOffice links rather than embeds an <img src> path, which would leave the
# .docx with a broken reference anywhere else - so inline every shot as a data URI.
FIGS = [
    ("01-backlog-epics-stories.png", "Backlog and User Stories"),
    ("02-story-points.png",          "Story Points"),
    ("03-active-sprint-board.png",   "Active Sprint Board"),
    ("04-burndown-chart.png",        "Burndown Chart"),
    ("05-issue-comments.png",        "Issue Comments"),
]


# A4 portrait, 14mm side margins -> ~182mm of text, ~660px at 96dpi.
PAGE_PX = 660


def png_size(raw):
    w, h = struct.unpack(">II", raw[16:24])
    return w, h


def img_tag(path):
    """LibreOffice's HTML importer ignores CSS max-width and places every image at
    its native pixel size, so state the scaled size as legacy width/height attributes."""
    raw = open(path, "rb").read()
    w, h = png_size(raw)
    scale = PAGE_PX / w
    uri = "data:image/png;base64," + base64.b64encode(raw).decode()
    return '<img src="%s" width="%d" height="%d">' % (uri, PAGE_PX, round(h * scale))


def build():
    import markdown
    body = markdown.markdown(open(os.path.join(R, "report.md")).read(),
                             extensions=["tables", "sane_lists"])
    figs = []
    for name, cap in FIGS:
        p = os.path.join(SHOTS, name)
        if not os.path.exists(p):
            print("  ! missing", name)
            continue
        # LibreOffice's HTML importer drops <figure>/<figcaption> and floats every
        # caption to the end, so emit plain paragraphs instead.
        figs.append('<p class="figtitle"><b>%s</b></p><p class="shot">%s</p>' % (cap, img_tag(p)))
    body += "\n".join(figs)

    # LibreOffice's HTML importer ignores CSS cell borders, so restate them as
    # legacy table attributes.
    body = body.replace("<table>", '<table border="1" cellspacing="0" cellpadding="3" width="100%">')

    page = os.path.join(TMP, "LAB2_SE_Final_Report.html")
    open(page, "w").write('<meta charset="utf-8"><style>%s</style>%s' % (CSS, body))

    subprocess.run(["soffice", "--headless", "--convert-to", "docx:MS Word 2007 XML",
                    "--outdir", TMP, page], capture_output=True, timeout=300, check=True)
    dest = os.path.join(R, "LAB2_SE_Final_Report.docx")
    os.replace(os.path.join(TMP, "LAB2_SE_Final_Report.docx"), dest)
    print("->", os.path.relpath(dest, R), os.path.getsize(dest), "bytes")


if __name__ == "__main__":
    os.makedirs(TMP, exist_ok=True)
    build()
