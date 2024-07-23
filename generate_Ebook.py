import os
import sqlite3
import pandas as pd
from pdf_base import PDF
from dotenv import load_dotenv

load_dotenv()

def create_ebooks_directory():
    if not os.path.exists('ebooks'):
        os.makedirs('ebooks')

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
        create_ebooks_directory()

        cursor = conn.cursor()
        for index, row in df.iterrows():
            title = f"Response {index + 1}"
            questions_answers = '\n'.join([f"{col}: {row[col]}" for col in df.columns if col not in ['id', 'user_id']])
            
            # Utilizando respostas diretamente sem processamento da API
            ebook_content = f"**Título:** {title}\n\n**Respostas:**\n{questions_answers}"
            print(f"Conteúdo do eBook gerado com sucesso.")
            
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
