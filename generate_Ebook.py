import os
import sqlite3
import pandas as pd
from pdf_base import PDF
from automation import chatgpt_response
from clear_caracters import clean_text
from datetime import datetime

# Diretório para OutPut
output_directory = 'users'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

#
def generate_ebook(user_id, driver):
    # Diretório específico para o usuário
    user_directory = os.path.join(output_directory, str(user_id))
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)

    # Diretório para armazenar os eBooks dentro da pasta do usuário
    ebook_directory = os.path.join(user_directory, 'ebook')
    if not os.path.exists(ebook_directory):
        os.makedirs(ebook_directory)

    # Gera um timestamp único para os arquivos e coloca os arquivos dentro da pasta de cada usuário
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(user_directory, f'output_{user_id}_{timestamp}.txt')
    tittle_file = os.path.join(user_directory, f'tittle_{user_id}_{timestamp}.txt')

    try:
        # Conexão com o banco de dados e obtém os dados do usuário e as respostas
        conn = sqlite3.connect('database.db')
        df = pd.read_sql_query("SELECT * FROM survey_responses WHERE user_id = ?", conn, params=(user_id,))
        df_user = pd.read_sql_query("SELECT email, name FROM users WHERE id = ?", conn, params=(user_id,))
        if df_user.empty:
            print("E-mail ou nome do autor não encontrado para o usuário.")
            return None

        # Obtém o email e o nome do Banco de Dados
        email = df_user.iloc[0]['email']
        name = df_user.iloc[0]['name']

        # Separa o nome para pegar somente o primeiro e o último
        name_parts = name.split()
        if len(name_parts) > 1:
            first_name = name_parts[0]
            last_name = name_parts[-1]
            formatted_name = f'{first_name} {last_name}'
        else:
            formatted_name = name

        # Manipula o email para obter a parte antes do '@'
        email_parts = email.split('@')
        if len(email_parts) > 1:
            email_base = email_parts[0]
        else:
            email_base = email

        # Salva as respostas em um arquivo
        for index, row in df.iterrows():
            responses_file = os.path.join(user_directory, f'response_{index + 1}_{timestamp}.txt')
            with open(responses_file, 'w', encoding='utf-8') as file:
                questions_answers = '\n'.join([f"{col}: {row[col]}" for col in df.columns if col not in ['id', 'user_id']])
                file.write(f"Response {index + 1}:\n{questions_answers}\n\n")

        # Executa a função de automação para gerar o conteúdo
        chatgpt_response(driver, user_id, responses_file, output_file, tittle_file, formatted_name, name)

        # Verifica se o arquivo de resposta foi criado e lê o conteúdo do arquivo de resposta
        if not os.path.exists(output_file):
            raise FileNotFoundError(f"O arquivo de resposta '{output_file}' não foi criado.")
        with open(output_file, 'r', encoding='utf-8') as file:
            content = file.read()
        content = clean_text(content)

        # Lê o conteúdo do arquivo de título e limpa o título
        if os.path.exists(tittle_file):
            with open(tittle_file, 'r', encoding='utf-8') as file:
                tittle_content = file.read().strip()
        title = clean_text(tittle_content)

        # Cria o PDF e adiciona as seções ao PDF com base nas palavras-chave
        pdf = PDF()
        pdf.add_cover(title)
        sections = {
            "Introdução": "",
            "Sumário": "",
            "Conteúdo": "",
            "Conclusão": ""
        }
        current_section = None
        lines = content.split('\n')
        for line in lines:
            if "Introdução" in line:
                current_section = "Introdução"
            elif "Sumário" in line:
                current_section = "Sumário"
            elif "Conteúdo" in line:
                current_section = "Conteúdo"
            elif "Conclusão" in line:
                current_section = "Conclusão"
            elif current_section:
                sections[current_section] += line + '\n'

        # Adiciona a Introdução sem adicionar página extra
        pdf.add_introduction(clean_text(sections["Introdução"].strip()))

        # Adiciona as outras seções com verificação de conteúdo
        for section, text in sections.items():
            if section == "Introdução":
                continue
            if text.strip():
                if section == "Sumário":
                    pdf.add_summary(clean_text(text.strip()))
                elif section == "Conteúdo":
                    pdf.add_chapter("Conteúdo", clean_text(text.strip()))
                elif section == "Conclusão":
                    pdf.add_conclusion(clean_text(text.strip()))

        # Salva o arquivo PDF e verifica a numeração atual dos arquivos
        counter = 1
        while True:
            file_path = os.path.join(ebook_directory, f'{counter}_{email_base}_{timestamp}.pdf')
            if not os.path.exists(file_path):
                pdf.output(file_path)
                break
            counter += 1

        # Atualiza o banco de dados
        cursor = conn.cursor()
        cursor.execute('INSERT INTO ebooks (user_id, file_path) VALUES (?, ?)', (user_id, file_path))
        conn.commit()

        # Remove arquivos temporários
        if os.path.exists(file_path):
            os.remove(responses_file)
            os.remove(output_file)
            os.remove(tittle_file)
        else:
            print("O eBook não foi criado, mantendo arquivos temporários.")

        # Retorna o caminho do eBook gerado
        return file_path

    except Exception as e:
        print(f"Erro durante a geração do eBook: {e}")
        return None
    finally:
        conn.close()
