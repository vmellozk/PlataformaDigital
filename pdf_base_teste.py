from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, '', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Prática Sênior', 0, 0, 'C')

    def add_cover(self, title, author_name):
        self.add_page()
        self.set_font("Arial", size=24)
        self.cell(200, 10, txt=title, ln=True, align='C')
        self.set_font("Arial", size=16)
        self.cell(200, 10, txt=f"by {author_name}", ln=True, align='C')

    def add_section(self, title, content):
        if not self.page_no():  # Se ainda não há páginas, adicione uma nova
            self.add_page()
        else:
            self.ln(10)  # Adiciona uma linha em branco antes da nova seção

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
