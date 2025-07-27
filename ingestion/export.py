from fpdf import FPDF

def export_summary_txt(summary, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(summary)

def export_summary_pdf(summary, filepath):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(filepath)
