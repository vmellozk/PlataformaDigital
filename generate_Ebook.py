#Função para Gerar o Ebook

import sqlite3
import pandas as pd
from fpdf import FPDF

def generate_ebook(user_id):
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query(f"SELECT * FROM survey_responses WHERE user_id = {user_id}", conn)
    conn.close()

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

    pdf = PDF()
    for index, row in df.iterrows():
        title = f"Response {index + 1}"
        body = '\n'.join([f"{col}: {row[col]}" for col in df.columns if col not in ['id', 'user_id']])
        pdf.add_chapter(title, body)

    pdf.output(f'survey_responses_ebook_{user_id}.pdf')