#teste

from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Survey Responses eBook', 0, 1, 'C')

    def add_section(self, title, content):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, title, 0, 1, 'C')
        self.ln(10)
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, content)
