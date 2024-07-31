import os
import sqlite3
import pandas as pd
from pdf_base import PDF
from automation import chatgpt_response

# Diretório para salvar os eBooks e arquivos temporários
ebook_directory = 'ebooks'
output_directory = 'output'
if not os.path.exists(ebook_directory):
    os.makedirs(ebook_directory)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def generate_ebook(user_id):
    responses_file = 'responses.txt'

    try:
        conn = sqlite3.connect('database.db')
        
        # Obtenha as respostas do formulário para o usuário específico
        df = pd.read_sql_query("SELECT * FROM survey_responses WHERE user_id = ?", conn, params=(user_id,))
        # Obtenha o e-mail e o nome do autor do usuário
        df_user = pd.read_sql_query("SELECT email, name FROM users WHERE id = ?", conn, params=(user_id,))
        if df_user.empty:
            print("E-mail ou nome do autor não encontrado para o usuário.")
            return

        #
        email = df_user.iloc[0]['email']
        name = df_user.iloc[0]['name']

        # Escrever as respostas no arquivo responses.txt
        with open(responses_file, 'w', encoding='utf-8') as file:
            for index, row in df.iterrows():
                questions_answers = '\n'.join([f"{col}: {row[col]}" for col in df.columns if col not in ['id', 'user_id']])
                file.write(f"Response {index + 1}:\n{questions_answers}\n\n")

        # Obter as respostas do ChatGPT e salvar em arquivos separados
        chatgpt_response(responses_file, output_directory, name)

        # Ler e combinar o conteúdo dos arquivos de saída para o PDF
        combined_content = ""
        for filename in ['capa.txt', 'sumario.txt', 'introducao.txt', 'conteudoprincipal.txt', 'conclusao.txt']:
            file_path = f"{output_directory}/{filename}"
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    combined_content += file.read() + "\n\n"

        # Criar o eBook em PDF
        pdf = PDF()

        # Adicionar uma página e o conteúdo ao PDF
        pdf.add_page()
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, combined_content)

        file_path = f'{ebook_directory}/{email}_ebook.pdf'
        pdf.output(file_path)
        print(f"eBook salvo em: {file_path}")

        # Inserir o caminho do eBook no banco de dados
        cursor = conn.cursor()
        cursor.execute('INSERT INTO ebooks (user_id, file_path) VALUES (?, ?)', (user_id, file_path))
        conn.commit()

        # Remover arquivos temporários apenas se o eBook foi criado com sucesso
        if os.path.exists(file_path):
            os.remove(responses_file)
            for filename in os.listdir(output_directory):
                os.remove(f"{output_directory}/{filename}")
            os.rmdir(output_directory)
            print("Arquivos temporários removidos.")
        else:
            print("O eBook não foi criado, mantendo arquivos temporários.")
        
    except Exception as e:
        print(f"Erro durante a geração do eBook: {e}")
    finally:
        conn.close()
        print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    generate_ebook(user_id=1)
