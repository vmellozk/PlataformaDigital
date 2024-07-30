from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Survey Responses eBook', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_chapter(self, title, body):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(body)

    def add_cover(self, title, company_name, name):
        self.add_page()
        self.set_font('Arial', 'B', 24)
        self.set_y(80)
        self.cell(0, 10, company_name, 0, 1, 'C')
        self.set_font('Arial', 'B', 36)
        self.cell(0, 10, title, 0, 1, 'C')
        self.set_font('Arial', 'I', 20)
        self.cell(0, 10, f'By {name}', 0, 1, 'C')
        self.ln(20)

    def add_introduction(self, text):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Introdução', 0, 1, 'L')
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, text)
        self.ln()

    def add_summary(self, text):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Sumário', 0, 1, 'L')
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, text)
        self.ln()

    def add_conclusion(self, text):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Conclusão', 0, 1, 'L')
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, text)
        self.ln()
