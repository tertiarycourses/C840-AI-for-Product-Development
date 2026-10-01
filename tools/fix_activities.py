"""Rewrite course code / title / version in the activity tree (MD, YAML, and the ReportLab README PDFs in place)."""
import pathlib, re, pypdf
from reportlab.pdfbase.pdfmetrics import stringWidth

SUBS = [("TGS-2024045799", "C840"), ("Agentic AI for Product Development", "AI for Product Development"),
        ("v7.0", "v1.0")]
for f in pathlib.Path("activities").rglob("*"):
    if f.suffix in (".md", ".yaml", ".json", ".py", ".csv") and f.is_file():
        s = o = f.read_text()
        for a, b in SUBS:
            s = s.replace(a, b)
        if s != o:
            f.write_text(s)

# PDFs: the title line is centred via "<x> 0 Td (title) Tj T* -<x> 0 Td" at Helvetica-Bold 22
old_t, new_t = "Agentic AI for Product Development", "AI for Product Development"
shift = (stringWidth(old_t, "Helvetica-Bold", 22) - stringWidth(new_t, "Helvetica-Bold", 22)) / 2
rx = re.compile(rb"([\d.]+) 0 Td \(" + old_t.encode() + rb"\) Tj T\* -([\d.]+) 0 Td")
n = 0
for f in sorted(pathlib.Path("activities").rglob("*.pdf")):
    w = pypdf.PdfWriter(clone_from=str(f))
    for pg in w.pages:
        co = pg.get_contents()
        d = co.get_data()
        d = rx.sub(lambda m: b"%.5f 0 Td (%s) Tj T* -%.5f 0 Td" % (float(m.group(1)) + shift, new_t.encode(),
                                                                   float(m.group(2)) + shift), d)
        d = d.replace(b"(TGS-2024045799 \\177 v7.0)", b"(C840 \\177 v1.0)")
        d = d.replace(b"TGS-2024045799", b"C840").replace(old_t.encode(), new_t.encode())
        co.set_data(d)
        pg.replace_contents(co)
    w.write(open(f, "wb"))
    n += 1
print("pdfs", n)
