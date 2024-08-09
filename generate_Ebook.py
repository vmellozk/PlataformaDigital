import os
import sqlite3
import pandas as pd
from pdf_base import PDF
from automation import chatgpt_response
from clear_caracters import clean_text

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
        with open(responses_file, 'w', encoding='utf-8') as file:
            for index, row in df.iterrows():
                questions_answers = '\n'.join([f"{col}: {row[col]}" for col in df.columns if col not in ['id', 'user_id']])
                file.write(f"Response {index + 1}:\n{questions_answers}\n\n")

        # Executa a função de automação para gerar o conteúdo
        chatgpt_response(responses_file, output_file, tittle_file, formatted_name)

        # Verifica se o arquivo de resposta foi criado e lê o conteúdo do arquivo de resposta e çimpa o conteúdo do arquivo de resposta
        if not os.path.exists(output_file):
            raise FileNotFoundError(f"O arquivo de resposta '{output_file}' não foi criado.")
        with open(output_file, 'r', encoding='utf-8') as file:
            content = file.read()
        content = clean_text(content)

        # Lê o conteúdo do arquivo de título e Limpa o título também
        if os.path.exists(tittle_file):
            with open(tittle_file, 'r', encoding='utf-8') as file:
                tittle_content = file.read().strip()
        title = clean_text(tittle_content)

        # Cria o PDF e Adiciona as seções ao PDF com base nas palavras-chave
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
            file_path = f'ebooks/{email_base}_{counter}.pdf'
            if not os.path.exists(file_path):
                break
            counter += 1
        pdf.output(file_path)

        # Atualiza o banco de dados
        cursor = conn.cursor()
        cursor.execute('INSERT INTO ebooks (user_id, file_path) VALUES (?, ?)', (user_id, file_path))
        conn.commit()

        # Remove arquivos temporários
        if os.path.exists(file_path):
            #os.remove(responses_file)
            os.remove(output_file)
            os.remove(tittle_file)
        else:
            print("O eBook não foi criado, mantendo arquivos temporários.")

    except Exception as e:
        print(f"Erro durante a geração do eBook: {e}")
    finally:
        conn.close()
        print("Conexão com o banco de dados fechada.")
