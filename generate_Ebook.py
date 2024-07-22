import os
import sqlite3
import openai
import pandas as pd
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_ebook(user_id):
    try:
        print(f"Iniciando a geração do eBook para o usuário_id: {user_id}")
        conn = sqlite3.connect('database.db')
        print("Conexão com o banco de dados estabelecida.")
        
        # Obtenha as respostas do formulário para o usuário específico
        df = pd.read_sql_query("SELECT * FROM survey_responses WHERE user_id = ?", conn, params=(user_id,))
        print(f"Respostas do formulário obtidas: {df.shape[0]} respostas encontradas.")
        
        # Obtenha o e-mail e o nome do autor do usuário
        df_user = pd.read_sql_query("SELECT email, name FROM users WHERE id = ?", conn, params=(user_id,))
        if df_user.empty:
            print("E-mail ou nome do autor não encontrado para o usuário.")
            return

        email = df_user.iloc[0]['email']
        name = df_user.iloc[0]['name']
        print(f"E-mail do usuário: {email}")
        print(f"Nome do autor: {name}")

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

        pdf = PDF()
        title = "Insights do Formulário"
        company_name = "Prática Sênior"
        pdf.add_cover(title, company_name, name)

        # Adiciona introdução e sumário
        introduction = "Este eBook fornece uma visão detalhada baseada nas respostas do formulário. Aqui você encontrará uma introdução ao tema, um sumário dos tópicos abordados e uma análise das respostas."
        pdf.add_introduction(introduction)

        summary = "1. Introdução\n2. Seção 1\n3. Seção 2\n4. Seção 3\n5. Seção 4\n6. Seção 5\n7. Conclusão"
        pdf.add_summary(summary)

        response_number = 1
        if not os.path.exists('ebooks'):
            os.makedirs('ebooks')

        cursor = conn.cursor()
        for index, row in df.iterrows():
            title = f"Response {index + 1}"
            questions_answers = '\n'.join([f"{col}: {row[col]}" for col in df.columns if col not in ['id', 'user_id']])
            prompt = f"""
            Crie um eBook com base nas respostas do formulário abaixo. O eBook deve seguir a estrutura abaixo:

            1. **Capa**: 
            - Título: "Insights do Formulário"
            - Autor: {name}

            2. **Introdução**: 
            - Apresente o propósito do eBook e o que será coberto.

            3. **Sumário**: 
            - Liste as principais seções e tópicos que serão abordados.

            4. **Conteúdo Principal**:
            - Divida o conteúdo em 5 seções, com base nas respostas do formulário.
            - Cada seção deve cobrir um conjunto específico de respostas e ser apresentada de forma clara e concisa.
            - Disserte também sobre a área comentada na resposta e abranja falando do mercado atual e futuro, contando as evoluções e afins.

            5. **Conclusão**: 
            - Resuma os principais pontos discutidos e forneça uma visão geral das conclusões.

            Use o texto a seguir para compor o conteúdo do eBook:

            Certifique-se de que o eBook seja informativo e fácil de ler, com uma formatação limpa e organizada. Cada seção deve ser bem estruturada e os pontos principais destacados. Mantenha o conteúdo relevante e focado nos insights extraídos das respostas do formulário.
            
            \n\n{questions_answers}"""
            
            try:
                print(f"Enviando prompt para a API do ChatGPT...")
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=prompt,
                    max_tokens=3000,
                    temperature=0.7
                )
                print(f"Resposta da API recebida.")
                
                ebook_content = response['choices'][0]['text'].strip()
                print(f"Conteúdo do eBook gerado com sucesso.")

            except Exception as e:
                print(f"Erro ao chamar a API do ChatGPT: {e}")
                ebook_content = "Erro ao processar o texto com o ChatGPT."

            sections = ebook_content.split('\n\n')
            if len(sections) >= 2:
                pdf.add_introduction(sections[0])
                pdf.add_summary(sections[1])
            
            content_start = 2
            content_end = min(content_start + 5, len(sections))
            for i in range(content_start, content_end):
                pdf.add_chapter(f"Seção {i - content_start + 1}", sections[i])
            
            if len(sections) > content_end:
                pdf.add_conclusion(sections[content_end])

            file_path = f'ebooks/{email}_ebook_{response_number}.pdf'
            pdf.output(file_path)
            print(f"eBook salvo em: {file_path}")

            cursor.execute('INSERT INTO ebooks (user_id, file_path) VALUES (?, ?)', (user_id, file_path))
            response_number += 1

        conn.commit()
    except Exception as e:
        print(f"Erro durante a geração do eBook: {e}")
    finally:
        conn.close()
        print("Conexão com o banco de dados fechada.")