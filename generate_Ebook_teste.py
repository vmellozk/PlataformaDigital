import os
import sqlite3
import pandas as pd
from pdf_base_teste import PDF
from automation_teste import chatgpt_response

# Diretório para o eBook
ebook_directory = 'ebooks'
if not os.path.exists(ebook_directory):
    os.makedirs(ebook_directory)

def generate_ebook(user_id):
    responses_file = 'responses.txt'
    output_file = 'output.txt'
    tittle_file = 'tittle.txt'

    try:
        # Conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        df = pd.read_sql_query("SELECT * FROM survey_responses WHERE user_id = ?", conn, params=(user_id,))
        df_user = pd.read_sql_query("SELECT email, name FROM users WHERE id = ?", conn, params=(user_id,))
        if df_user.empty:
            print("E-mail ou nome do autor não encontrado para o usuário.")
            return

        email = df_user.iloc[0]['email']
        name = df_user.iloc[0]['name']

        # Salva as respostas em um arquivo
        with open(responses_file, 'w', encoding='utf-8') as file:
            for index, row in df.iterrows():
                questions_answers = '\n'.join([f"{col}: {row[col]}" for col in df.columns if col not in ['id', 'user_id']])
                file.write(f"Response {index + 1}:\n{questions_answers}\n\n")

        # Executa a função de automação para gerar o conteúdo
        chatgpt_response(responses_file, output_file, tittle_file, name)

        # Verifica se o arquivo de resposta foi criado
        if not os.path.exists(output_file):
            raise FileNotFoundError(f"O arquivo de resposta '{output_file}' não foi criado.")
        
        # Lê o conteúdo do arquivo de resposta
        with open(output_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Lê o conteúdo do arquivo de título
        if os.path.exists(tittle_file):
            with open(tittle_file, 'r', encoding='utf-8') as file:
                tittle_content = file.read().strip()
        else:
            tittle_content = "Título não disponível"

        # Cria o PDF
        pdf = PDF()
        title = tittle_content
        pdf.add_cover(title, name)

        # Divide o conteúdo nas seções
        sections = content.split('####')

        # Adiciona as seções ao PDF
        if len(sections) > 0:
            pdf.add_introduction(sections[0].strip())
        if len(sections) > 1:
            pdf.add_summary(sections[1].strip())
        for i in range(2, len(sections) - 1):
            pdf.add_chapter(f"Seção {i - 1}", sections[i].strip())
        if len(sections) > 2:
            pdf.add_conclusion(sections[-1].strip())

        # Salva o arquivo PDF
        file_path = f'ebooks/{email}_ebook.pdf'
        pdf.output(file_path)
        print(f"eBook salvo em: {file_path}")

        # Atualiza o banco de dados
        cursor = conn.cursor()
        cursor.execute('INSERT INTO ebooks (user_id, file_path) VALUES (?, ?)', (user_id, file_path))
        conn.commit()

    except Exception as e:
        print(f"Erro durante a geração do eBook: {e}")
    finally:
        conn.close()
        print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    generate_ebook(user_id=1)
