import os
import sqlite3
import pandas as pd
from pdf_base import PDF
from automation import chatgpt_response

ebook_directory = 'ebooks'
if not os.path.exists(ebook_directory):
    os.makedirs(ebook_directory)

def generate_ebook(user_id):
    responses_file = 'responses.txt'
    response_file = 'response.txt'

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

        with open(responses_file, 'w') as file:
            for index, row in df.iterrows():
                questions_answers = '\n'.join([f"{col}: {row[col]}" for col in df.columns if col not in ['id', 'user_id']])
                file.write(f"Response {index + 1}:\n{questions_answers}\n\n")

        # Obter a resposta do ChatGPT usando Selenium
        chatgpt_response(responses_file, response_file, name)

        if not os.path.exists(response_file):
            raise FileNotFoundError(f"O arquivo de resposta '{response_file}' não foi criado.")

        # Criar o eBook em PDF
        pdf = PDF()
        title = "Insights do Formulário"
        company_name = "Prática Sênior"
        pdf.add_cover(title, company_name, name)

        with open(response_file, 'r') as file:
            content = file.read()

        sections = content.split('\n\n')
        if len(sections) >= 2:
            pdf.add_introduction(sections[0])
            pdf.add_summary(sections[1])

        content_start = 2
        content_end = min(content_start + 5, len(sections))
        for i in range(content_start, content_end):
            pdf.add_chapter(f"Seção {i - content_start + 1}", sections[i])
        
        if len(sections) > content_end:
            pdf.add_conclusion(sections[content_end])

        file_path = f'ebooks/{email}_ebook.pdf'
        pdf.output(file_path)
        print(f"eBook salvo em: {file_path}")

        cursor = conn.cursor()
        cursor.execute('INSERT INTO ebooks (user_id, file_path) VALUES (?, ?)', (user_id, file_path))
        conn.commit()

        # Remover arquivos temporários apenas se o eBook foi criado com sucesso
        if os.path.exists(file_path):
            os.remove(responses_file)
            os.remove(response_file)
        else:
            print("O eBook não foi criado, mantendo arquivos temporários.")
        
    except Exception as e:
        print(f"Erro durante a geração do eBook: {e}")
    finally:
        conn.close()
        print("Conexão com o banco de dados fechada.")
