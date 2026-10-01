"""C840 Learner Guide: explicit rewrite of the WSQ LG (TGS-2024045799) as the non-WSQ twin."""
import shutil, docx, docx.text.paragraph
from docxutil import *

SRC = "source-wsq/courseware/LG-Agentic AI for Product Development.docx"
OUT = "courseware/LG-AI for Product Development (C840).docx"
shutil.copy(SRC, OUT)
d = docx.Document(OUT)
retitle_all(d)
t_cover, t_ctrl = d.tables[0], d.tables[1]

set_text(para_by_text(d, "WSQ COURSEWARE"), "NON-WSQ COURSEWARE")


def kv(table, key):
    return next(r for r in table.rows if r.cells[0].text == key)


def heading(start):
    hits = [p for p in d.paragraphs if p.text.startswith(start) and p.style.name.startswith("Heading")]
    assert len(hits) == 1, start
    return hits[0]


def toc(start):
    hits = [p for p in d.paragraphs if p.text.startswith(start) and "\t" in p.text]
    assert len(hits) == 1, start
    return hits[0]


# Cover table
set_cell(kv(t_cover, "Course Code").cells[1], "C840")
t_cover._tbl.remove(kv(t_cover, "Technical Skills and Competencies")._tr)
set_cell(kv(t_cover, "Version").cells[1], "v1.0")
set_cell(kv(t_cover, "Release Date").cells[1], "1 October 2026")

# Document control -> single v1.0 row
t_ctrl._tbl.remove(t_ctrl.rows[2]._tr)
for c, v in zip(t_ctrl.rows[1].cells, ["Learner Guide", "1.0", "1 October 2026", "Tertiary Infotech Academy Pte. Ltd.",
                                       "Initial release of the AI for Product Development learner guide: concept notes "
                                       "for the 3 topics and detailed step-by-step guides for all 12 activities"]):
    set_cell(c, v)

# 1.2 Knowledge and Ability Map (WSQ K/A codes) goes; 1.3 -> 1.2
km = heading("1.2 Knowledge and Ability Map")
tbl = km._p.getnext()
assert tbl.tag.endswith("}tbl")
tbl.getparent().remove(tbl)
delete(km)
set_text(heading("1.3 End-to-End Reference Architecture"), "1.2 End-to-End Reference Architecture")
delete(toc("1.2 Knowledge and Ability Map"))
t = toc("1.3 End-to-End Reference Architecture")
set_text(t, t.text.replace("1.3 ", "1.2 ", 1))

# 7. Assessment Preparation goes; 8 -> 7
ap = heading("7. Assessment Preparation")
nxt = ap._p.getnext()
delete(ap)
while not docx.text.paragraph.Paragraph(nxt, d).text.startswith("8. References"):
    gone, nxt = nxt, nxt.getnext()
    gone.getparent().remove(gone)
set_text(heading("8. References"), "7. References")
delete(toc("7. Assessment Preparation"))
t = toc("8. References")
set_text(t, t.text.replace("8. ", "7. ", 1))

# References: non-WSQ course page + repo
set_text(para_by_text(d, "Current course page:"),
         "Current course page: https://www.tertiarycourses.com.sg/ai-for-product-development.html — "
         "Course identity, duration, learning outcomes and topics")
set_text(para_by_text(d, "Course repository:"),
         "Course repository: https://github.com/tertiarycourses/C840-AI-for-Product-Development")

d.core_properties.title = "LG-AI for Product Development (C840)"
d.save(OUT)
print("saved", OUT)
