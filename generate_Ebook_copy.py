import os
import sqlite3
import pandas as pd
from pdf_base_copy import PDF
from automation_copy import chatgpt_response

# Diretório para salvar os eBooks
ebook_directory = 'ebooks'
if not os.path.exists(ebook_directory):
    os.makedirs(ebook_directory)

def generate_ebook(user_id):
    responses_file = 'responses.txt'
    output_file = 'output.txt'

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

        # Escrever as respostas no arquivo responses.txt
        with open(responses_file, 'w', encoding='utf-8') as file:
            for index, row in df.iterrows():
                questions_answers = '\n'.join([f"{col}: {row[col]}" for col in df.columns if col not in ['id', 'user_id']])
                file.write(f"Response {index + 1}:\n{questions_answers}\n\n")

        # Obter a resposta do ChatGPT usando Selenium
        print("Obtendo a resposta do ChatGPT...")
        chatgpt_response(responses_file, output_file, name)
        print("Resposta do ChatGPT obtida.")

        if not os.path.exists(output_file):
            raise FileNotFoundError(f"O arquivo de resposta '{output_file}' não foi criado.")
        
        # Ler o conteúdo do arquivo output.txt
        with open(output_file, 'r', encoding='utf-8') as file:
            content = file.read()
            print("Conteúdo do arquivo output.txt:")
            print(content)

        # Criar o eBook em PDF
        print("Criando o eBook em PDF...")
        pdf = PDF()

        # Adicionar uma página e o conteúdo do arquivo output.txt ao PDF
        pdf.add_page()
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, content)

        file_path = f'ebooks/{email}_ebook.pdf'
        pdf.output(file_path)
        print(f"eBook salvo em: {file_path}")

        # Inserir o caminho do eBook no banco de dados
        cursor = conn.cursor()
        cursor.execute('INSERT INTO ebooks (user_id, file_path) VALUES (?, ?)', (user_id, file_path))
        conn.commit()
        print("Caminho do eBook inserido no banco de dados.")

        # Remover arquivos temporários apenas se o eBook foi criado com sucesso
        if os.path.exists(file_path):
            os.remove(responses_file)
            os.remove(output_file)
            print("Arquivos temporários removidos.")
        else:
            print("O eBook não foi criado, mantendo arquivos temporários.")
        
    except Exception as e:
        print(f"Erro durante a geração do eBook: {e}")
    finally:
        conn.close()
        print("Conexão com o banco de dados fechada.")
