from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, '', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Prática Sênior', 0, 0, 'C')

    def add_cover(self, title):
        self.add_page()
        page_width = self.w - 2 * self.l_margin
        page_height = self.h
        self.set_font("Arial", 'B', 24)
        self.set_xy(self.l_margin, page_height / 3)
        self.multi_cell(page_width, 10, title, 0, 'C')
        self.ln(10)

    def add_section(self, title, content):
        if content.strip():  # Verifica se a seção não está vazia
            self.add_page()
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, title, 0, 1, 'C')
            self.ln(10)
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, content)

    def add_introduction(self, content):
        self.add_section("Introdução", content)

    def add_summary(self, content):
        self.add_section("Sumário", content)

    def add_chapter(self, title, content):
        self.add_section(title, content)

    def add_conclusion(self, content):
        self.add_section("Conclusão", content)
