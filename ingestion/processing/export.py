from fpdf import FPDF
import os

def export_summary_txt(summary: str, filepath: str):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(summary)

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        font_path = os.path.join("fonts", "DejaVuSans.ttf")  # assure-toi que ce fichier existe
        self.add_font("DejaVu", "", font_path, uni=True)
        self.add_page()
        self.set_font("DejaVu", "", 12)

    def write_utf8(self, text: str):
        self.multi_cell(0, 10, text)

def export_summary_pdf(summary: str, filepath: str):
    pdf = PDF()
    pdf.write_utf8(summary)
    pdf.output(filepath)

