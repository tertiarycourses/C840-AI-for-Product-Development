"""C840 Lesson Plan: explicit rewrite of the WSQ LP (TGS-2024045799) as the 2-day non-WSQ twin."""
import shutil, docx
from docxutil import *

SRC = "source-wsq/courseware/LP-Agentic AI for Product Development.docx"
OUT = "courseware/LP-AI for Product Development (C840).docx"
shutil.copy(SRC, OUT)
d = docx.Document(OUT)
retitle_all(d)
t_cover, t_ctrl, t_info, t_day1, t_day2, t_assess = d.tables

set_text(para_by_text(d, "WSQ COURSEWARE"), "NON-WSQ COURSEWARE")


def heading(start):
    hits = [p for p in d.paragraphs if p.text.startswith(start) and p.style.name.startswith("Heading")]
    assert len(hits) == 1, start
    return hits[0]


def kv(table, key):
    return next(r for r in table.rows if r.cells[0].text == key)


def drop(table, key):
    table._tbl.remove(kv(table, key)._tr)


# Cover table
set_cell(kv(t_cover, "Course Code").cells[1], "C840")
drop(t_cover, "Technical Skills and Competencies")
set_cell(kv(t_cover, "Version").cells[1], "v1.0")
set_cell(kv(t_cover, "Release Date").cells[1], "1 October 2026")

# Document control -> single v1.0 row
t_ctrl._tbl.remove(t_ctrl.rows[2]._tr)
for c, v in zip(t_ctrl.rows[1].cells, ["Lesson Plan", "1.0", "1 October 2026", "Tertiary Infotech Academy Pte. Ltd.",
                                       "Initial release of the AI for Product Development lesson plan: two 9:30am – 5:30pm "
                                       "days (15 instructional hours) covering all 3 topics and 12 activities, mapped to "
                                       "the v1.0 199-slide deck"]):
    set_cell(c, v)

# TOC
def toc(start):
    hits = [p for p in d.paragraphs if p.text.startswith(start) and "\t" in p.text]
    assert len(hits) == 1, start
    return hits[0]
delete(toc("6. Assessment and Evidence Plan"))
set_text(toc("4. Day 1 Detailed Schedule"), "4. Day 1 Detailed Schedule · 9:30am – 5:30pm\t3")
set_text(toc("5. Day 2 Detailed Schedule"), "5. Day 2 Detailed Schedule · 9:30am – 5:30pm\t4")
set_text(toc("7. Trainer Preparation Checklist"), "6. Trainer Preparation Checklist\t4")
set_text(toc("8. References"), "7. References\t5")

# 1. Course and delivery information
set_cell(kv(t_info, "Course code").cells[1], "C840")
drop(t_info, "TSC")
drop(t_info, "Assessment")
set_cell(kv(t_info, "Duration").cells[1],
         "2 days / 15 instructional hours (9:30am – 5:30pm daily, one 30-minute lunch)")
set_cell(kv(t_info, "Required resources").cells[1],
         "199-slide deck, Learner Guide, twelve activity folders, spreadsheet/JSON viewer and an approved agentic AI builder")

# 4 / 5. Schedules: 450 teaching minutes + one 30-minute lunch per day, closing on 5:30pm.
# Day 1: the WSQ rows (30/90/120/90/105/45 = 480 min) rescaled proportionally onto 450.
# Day 2: the WSQ non-assessment rows (60/90/90/60/60 = 360 min) rescaled onto the 450 freed by the assessment.
set_text(heading("4. Day 1 Detailed Schedule"), "4. Day 1 Detailed Schedule · 9:30am – 5:30pm")
rebuild_rows(t_day1, [
    (1, ["09:30–10:00", "Welcome, introductions, context, LMS access and course outline", "Facilitated briefing",
         "Slides 1–10", "Learner context and materials access"]),
    (2, ["10:00–11:25", "Topic 1: product opportunity, JTBD and research-agent evidence",
         "Mechanism dialogue + worked examples", "Slides 11–34", "Opportunity brief and claim ledger"]),
    (3, ["11:25–13:15", "Topic 1: builder comparison, readiness and build-buy-partner decisions",
         "Technical explanation + critique", "Slides 35–71", "Weighted matrix and readiness heatmap"]),
    (4, ["13:15–13:45", "Lunch", "—", "—", "—"]),
    (5, ["13:45–15:10", "Activities 01–03: opportunity, builder comparison and evidence pack",
         "Guided activity; individual evidence", "Activity 01–03 folders + LG §5.1–5.3",
         "Opportunity brief, comparison and claim ledger"]),
    (6, ["15:10–16:50", "Topic 2: product context, agent roles, handoffs and evaluation sets",
         "Mechanism dialogue + technical demonstration", "Slides 72–107", "Workflow canvas and evaluation contract"]),
    (7, ["16:50–17:30", "Activities 04–06: persona, workflow canvas and AI-ready PRD",
         "Guided setup + facilitated debrief", "Activity 04–06 folders + Topic 2 checkpoint",
         "Persona/JTBD map, handoff contract and PRD"]),
])
set_text(heading("5. Day 2 Detailed Schedule"), "5. Day 2 Detailed Schedule · 9:30am – 5:30pm")
rebuild_rows(t_day2, [
    (1, ["09:30–10:45", "Activities 07–08: prompt evaluation set and prototype experiment",
         "Guided activity; verifier-led evidence", "Activity 07–08 folders",
         "Frozen evaluation set and experiment ledger"]),
    (2, ["10:45–12:40", "Topic 3: deployment posture, architecture, security and observability",
         "Mechanism dialogue + technical demonstration", "Slides 133–163", "Deployment decision and control rationale"]),
    (4, ["12:40–13:10", "Lunch", "—", "—", "—"]),
    (3, ["13:10–15:00", "Activities 09–10: deployment and risk-control review",
         "Guided activity; individual verification", "Activity 09–10 folders + LG §5.9–5.10",
         "Reference architecture and risk register"]),
    (5, ["15:00–16:15", "Topic 3: KPI feedback, rollout and risk-adjusted recommendation",
         "Evidence analysis + worked comparison", "Slides 164–193", "Monitoring scorecard and rollout gate"]),
    (6, ["16:15–17:30", "Activities 11–12: KPI dashboard and executive recommendation; course close and feedback",
         "Individual capstone + decision review", "Activity 11–12 folders + LG §5.11–5.12; Slides 194–199",
         "KPI tree, bounded recommendation and course feedback"]),
])

# 6. Assessment and Evidence Plan goes (heading + table); 7/8 renumber
t_assess._tbl.getparent().remove(t_assess._tbl)
delete(heading("6. Assessment and Evidence Plan"))
set_text(heading("7. Trainer Preparation Checklist"), "6. Trainer Preparation Checklist")
set_text(heading("8. References"), "7. References")

# Trainer checklist + references
set_text(para_by_text(d, "Confirm the course identity, version and 207-slide deck"),
         "Confirm the course identity, version and 199-slide deck before class.")
delete(para_by_text(d, "Confirm assessment candidate papers"))
set_text(para_by_text(d, "Test LMS and attendance access"),
         "Test LMS access without exposing credentials on projected screens.")
set_text(para_by_text(d, "Current course page:"),
         "Current course page: https://www.tertiarycourses.com.sg/ai-for-product-development.html — "
         "Course identity, duration, learning outcomes and topics")

d.core_properties.title = "LP-AI for Product Development (C840)"
d.save(OUT)
print("saved", OUT)
