import os
import sqlite3
import pandas as pd
from pdf_base import PDF
from automation import chatgpt_response
from text_utils import clean_text  # Importe a função de limpeza

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

        # Verifica se o arquivo de resposta foi criado e lê o conteúdo do arquivo de resposta
        if not os.path.exists(output_file):
            raise FileNotFoundError(f"O arquivo de resposta '{output_file}' não foi criado.")
        with open(output_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Limpa o conteúdo do arquivo de resposta
        content = clean_text(content)

        # Lê o conteúdo do arquivo de título
        if os.path.exists(tittle_file):
            with open(tittle_file, 'r', encoding='utf-8') as file:
                tittle_content = file.read().strip()

        # Limpa o título também
        title = clean_text(tittle_content)

        # Cria o PDF
        pdf = PDF()
        pdf.add_cover(title)

        # Divide o conteúdo nas seções e adiciona as seções ao PDF
        sections = content.split('####')
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

        # Remove arquivos temporários
        if os.path.exists(file_path):
            os.remove(output_file)
            os.remove(tittle_file)
        else:
            print("O eBook não foi criado, mantendo arquivos temporários.")

    except Exception as e:
        print(f"Erro durante a geração do eBook: {e}")
    finally:
        conn.close()
        print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    generate_ebook(user_id=1)
