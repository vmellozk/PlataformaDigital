from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, '', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Prática Sênior', 0, 0, 'C')

    def add_section(self, title, content):
        self.add_page()  # Adiciona uma nova página
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, title, 0, 1, 'C')
        self.ln(10)
        self.set_font('Arial', '', 12)
        # Remove a codificação 'latin-1' e use UTF-8
        self.multi_cell(0, 10, content)
