#Função para Gerar o Ebook

import os
import sqlite3
import openai
import pandas as pd
from fpdf import FPDF

openai_key = 'chave_api_aqui'

def generate_ebook(user_id):
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query(f"SELECT * FROM survey_responses WHERE user_id = {user_id}", conn)
    df_user = pd.read_sql_query(f"SELECT email FROM users WHERE id = {user_id}", conn)

    if df_user.empty:
        print("E-mail não encontrado para o usuário.")
        return
    
    email = df_user.iloc[0]['email']

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
    response_number = 1

    if not os.path.exists('ebooks'):
        os.makedirs('ebooks')

    cursor = conn.cursor()

    for index, row in df.iterrows():
        title = f"Response {index + 1}"
        # Preparar perguntas e respostas
        questions_answers = '\n'.join([f"{col}: {row[col]}" for col in df.columns if col not in ['id', 'user_id']])

        # Enviar para o ChatGPT para melhorar o texto
        prompt = f"Baseado nas respostas abaixo, gere um texto detalhado e organizado para o eBook:\n\n{questions_answers}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1500
        )
        improved_text = response.choices[0].text.strip()

        pdf.add_chapter(title, improved_text)
        file_path = f'ebooks/{email}_ebook_{response_number}.pdf'
        pdf.output(file_path)

        cursor.execute('INSERT INTO ebooks (user_id, file_path) VALUES (?, ?)', (user_id, file_path))
        response_number += 1

    conn.commit()
    conn.close()