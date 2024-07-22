import os
import sqlite3
import openai
import pandas as pd
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_ebook(user_id):
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query("SELECT * FROM survey_responses WHERE user_id = ?", conn, params=(user_id,))
    df_user = pd.read_sql_query("SELECT email, author_name FROM users WHERE id = ?", conn, params=(user_id,))

    if df_user.empty:
        print("E-mail ou nome do autor não encontrado para o usuário.")
        return

    email = df_user.iloc[0]['email']
    author_name = df_user.iloc[0]['author_name']

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

        def add_cover(self, title, company_name, author_name):
            self.add_page()
            self.set_font('Arial', 'B', 24)
            self.set_y(80)
            self.cell(0, 10, company_name, 0, 1, 'C')
            self.set_font('Arial', 'B', 36)
            self.cell(0, 10, title, 0, 1, 'C')
            self.set_font('Arial', 'I', 20)
            self.cell(0, 10, f'By {author_name}', 0, 1, 'C')
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

    pdf = PDF()

    title = "Insights do Formulário"
    company_name = "Prática Sênior"
    pdf.add_cover(title, company_name, author_name)

    # Gerar o conteúdo do eBook
    prompt = f"""
    Crie um eBook com base nas respostas do formulário abaixo. O eBook deve seguir a estrutura abaixo:

    1. **Capa**: 
    - Título: "Insights do Formulário"
    - Autor: Seu nome

    2. **Introdução**: 
    - Apresente o propósito do eBook e o que será coberto.

    3. **Sumário**: 
    - Liste as principais seções e tópicos que serão abordados.

    4. **Conteúdo Principal**:
    - Divida o conteúdo em 5 seções(pode ser capitulos), com base nas respostas do formulário.
    - Cada seção deve cobrir um conjunto específico de respostas e ser apresentada de forma clara e concisa.
    - Disserte também sobre a área comentada na resposta e abrange falando do mercado atual e futuro, contando as evoluções e afins.

    5. **Conclusão**: 
    - Resuma os principais pontos discutidos e forneça uma visão geral das conclusões.

    Use o texto a seguir para compor o conteúdo do eBook:

    Certifique-se de que o eBook seja informativo e fácil de ler, com uma formatação limpa e organizada. Cada seção deve ser bem estruturada e os pontos principais destacados. Mantenha o conteúdo relevante e focado nos insights extraídos das respostas do formulário.
    
    \n\n{df.to_csv(index=False)}
    """

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=6000
        )
        ebook_content = response.choices[0].text.strip()

    except Exception as e:
        print(f"Erro ao chamar a API do ChatGPT: {e}")
        ebook_content = "Erro ao processar o texto com o ChatGPT."


    # Separar o conteúdo do eBook em partes
    sections = ebook_content.split('\n\n')
    # Adicionar Introdução
    pdf.add_introduction(sections[0])
    # Adicionar Sumário
    pdf.add_summary(sections[1])

    # Adicionar Conteúdo Principal
    content_start = 2
    content_end = min(content_start + 30, len(sections))
    for i in range(content_start, content_end):
        pdf.add_chapter(f"Seção {i - content_start + 1}", sections[i])
        
    # Adicionar Conclusão
    if len(sections) > content_end:
        pdf.add_conclusion(sections[content_end])


    file_path = f'ebooks/{email}_ebook.pdf'
    pdf.output(file_path)

    cursor = conn.cursor()
    cursor.execute('INSERT INTO ebooks (user_id, file_path) VALUES (?, ?)', (user_id, file_path))

    conn.commit()
    conn.close()
