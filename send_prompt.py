import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
from selenium.webdriver.common.keys import Keys
from prompt import get_initial_prompt, responses, tittle
from selenium.common.exceptions import TimeoutException
from threading import Lock
from clear_caracters import remove_special_characters
import os

#
mutex = Lock()

#
def copy_text(driver, button_xpath):
    while True:
        try:
            button_element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, button_xpath))
            )
            if button_element:
                button_element.click()
                time.sleep(1)
                break
            else:
                print("Botão de copiar não encontrado.")
                time.sleep(1)
        except TimeoutException:
            print(f"Tempo limite esgotado para encontrar o botão de copiar '{button_xpath}'. Tentando novamente...")
        except Exception as e:
            print(f"Erro inesperado durante o copiar resposta: {e}")

    copied_text = pyperclip.paste()
    return copied_text

#
def send_text_with_line_breaks(input_field, text):
    for chunk in text.split('\n'):
        input_field.send_keys(chunk)
        input_field.send_keys(Keys.SHIFT + Keys.ENTER)
    input_field.send_keys(Keys.ENTER)

#
def refresh_page(driver, responses_file, tittle_file, output_file, name, user_id):
    print("Atualizando a página e reiniciando o processo...")
    driver.refresh()
    time.sleep(5)
    send_prompts(driver, responses_file, tittle_file, output_file, name, user_id)

#
def send_prompts(driver, responses_file, tittle_file, output_file, name, user_id):
    def get_input_field():
        return WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="prompt-textarea"]'))
        )
    input_field = get_input_field()

    #
    with open(responses_file, 'r', encoding='utf-8') as file:
        responses_text = file.read()

    #
    full_prompt = get_initial_prompt()
    for i in range(0, len(full_prompt), 5000):
        input_field.send_keys(full_prompt[i:i + 5000])
        time.sleep(1)
    input_field.send_keys(Keys.ENTER)
    while True:
        try:
            button_copy_1 = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[2]/div/div/div[2]/div/div[2]/div/div/span[1]/button'))
            )
            if button_copy_1:
                print("button_copy_1 encontrado")
                time.sleep(2)
                break
            else:
                print("button_copy_1 não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrar o button_copy_1. Atualizando a página...")
            time.sleep(1)
            refresh_page(driver, responses_file, tittle_file, output_file, name, user_id)
        except Exception as e:
            print(f"Erro ao encontrar o button_copy_1: {e}")
            time.sleep(1)

    #
    responses_prompt = responses(responses_text)
    full_responses = ''.join(responses_prompt)
    full_responses += '\n Ok, passei as respostas, mas não faça nada ainda. Responda apenas OK, nada mais! Aguarde as instruções.\n'
    send_text_with_line_breaks(input_field, full_responses)
    input_field = get_input_field()
    while True:
        try:
            button_copy_2 = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[4]/div/div/div[2]/div/div[2]/div/div/span[1]/button'))
            )
            if button_copy_2:
                print("button_copy_2 encontrado")
                time.sleep(1)
                break
            else:
                print("button_copy_2 não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrar o button_copy_2. Atualizando a página...")
            time.sleep(1)
            refresh_page(driver, responses_file, tittle_file, output_file, name, user_id)
        except Exception as e:
            print(f"Erro ao encontrar o button_copy_2: {e}")
            time.sleep(1)

    # Trecho responsável por enviar o prompt que pega o capa do eBook com o Título e Autor, cortando também o texto para salvar também o título do eBook
    tittle_prompt = tittle(name)
    for i in range(0, len(tittle_prompt), 1000):
        input_field.send_keys(tittle_prompt[i:i + 1000])
        time.sleep(2)
    input_field.send_keys(Keys.ENTER)
    input_field = get_input_field()
    while True:
        try:
            button_copy_3 = '/html/body/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[6]/div/div/div[2]/div/div[2]/div/div/span[1]/button'
            if button_copy_3:
                print("button_copy_3 encontrado")
                time.sleep(2)
                copied_tittle = copy_text(driver, button_copy_3)
                with mutex:
                    with open(tittle_file, "w", encoding="utf-8") as file:
                        file.write(copied_tittle)
                        print(f"Título salvo em: {tittle_file}")

                # Lê o conteúdo do arquivo salvo e remove caracteres especiais usando a nova função
                with open(tittle_file, "r", encoding="utf-8") as file:
                    saved_title = file.read()
                cleaned_tittle = remove_special_characters(saved_title)

                # Extrai o texto entre "Título:" e "Autor: e ajusta os índices para capturar apenas o conteúdo entre as palavras-chave"
                start_keyword = "Título:"
                end_keyword = "Autor:"
                start_index = cleaned_tittle.find(start_keyword)
                end_index = cleaned_tittle.find(end_keyword)
                if start_index != -1 and end_index != -1:
                    start_index += len(start_keyword)
                    title_content = cleaned_tittle[start_index:end_index].strip()

                    # Salva o conteúdo extraído em um novo arquivo na pasta users/user_id/
                    user_folder = os.path.join("users", str(user_id))
                    extracted_file_path = os.path.join(user_folder, 'name_product.txt')
                    with open(extracted_file_path, "w", encoding="utf-8") as extra_file:
                        extra_file.write(title_content)
                        print(f"Conteúdo extraído salvo em: {extracted_file_path}")

                else:
                    print("Palavras-chave 'Título:' e 'Autor:' não encontradas no texto copiado.")
                time.sleep(1)
                break
            
            else:
                print("button_copy_3 não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrar o button_copy_3. Atualizando a página...")
            time.sleep(1)
            refresh_page(driver, responses_file, tittle_file, output_file, name, user_id)
        except Exception as e:
            print(f"Erro ao encontrar o button_copy_3: {e}")
            time.sleep(1)

    #
    confirmacao = 'OK, agora me forneça o restante do conteúdo. A introdução deve ser feita para ser utilizada como introdução e como descrição do conteúdo/eBook. Faça com que seja algo mais pessoal, abordando as respostas e, em alguns momentos em primeira pessoa, mas mantendo o profissionalismo. Lembrando da hash antes de: ####Introdução, ####Sumário, ####Conteúdo e ####Conclusão. Forneça esses tópicos assim e tudo em um único texto! Lembrando que quanto mais conteúdo foi fornecido de resposta, mais conteúdo será gerado. Apenas responda o que foi pedido, sem "essa foi a resposta, se precisar de mais..." não quero nada disso. Triplique o tamanho do conteúdo do ebook para cada tópico. Ou seja, me dê 3x mais de conteúdo para cada tópico do ebook do que o normal, tornando o ebook completo.'
    input_field.send_keys(confirmacao)
    time.sleep(1)
    input_field.send_keys(Keys.ENTER)
    while True:
        try:
            arrow_botton = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[1]/div[1]/div/div/div/div/button'))
            )
            if arrow_botton:
                print("arrow_botton encontrado")
                time.sleep(2)
                arrow_botton.click()
            else:
                print("arrow_botton não encontrado")
        except TimeoutException:
            pass

        try:
            keep_generate = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div/form/div/div[1]/div/div/div/div/button'))
            )
            if keep_generate:
                print("keep_generate encontrado")
                time.sleep(2)
                keep_generate.click()
            else:
                print("keep_generate não encontrado")
        except TimeoutException:
            pass

        #
        try:
            button_copy_4 = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[2]/div/div/span[1]/button'))
            )
            if button_copy_4:
                print("button_copy_4 encontrado")
                time.sleep(2)
                copied_text = copy_text(driver, '/html/body/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[2]/div/div/span[1]/button')
                with mutex:
                    with open(output_file, "w", encoding="utf-8") as file:
                        file.write(copied_text)

                # Lê o conteúdo do arquivo output_file
                with open(output_file, "r", encoding="utf-8") as file:
                    output_content = file.read()

                # Lógica para cortar o conteúdo entre "Introdução" e "Sumário"
                start_keyword = "Introdução"
                end_keyword = "Sumário"
                start_index = output_content.find(start_keyword)
                end_index = output_content.find(end_keyword)

                # Verifica se as palavras-chave foram encontradas
                if start_index != -1 and end_index != -1:
                    # Ajusta os índices para capturar apenas o conteúdo entre as palavras-chave
                    start_index += len(start_keyword)
                    description_content = output_content[start_index:end_index].strip()

                    # Salva o conteúdo extraído em um novo arquivo
                    user_folder = os.path.join("users", str(user_id))
                    description_file_path = os.path.join(user_folder, "descricao_product.txt")
                    
                    with open(description_file_path, "w", encoding="utf-8") as desc_file:
                        desc_file.write(description_content)
                        print(f"Conteúdo extraído salvo em: {description_file_path}")
                else:
                    print("Palavras-chave 'Introdução' e 'Sumário' não encontradas no texto copiado.")

                time.sleep(1)

                #
                driver.refresh()
                time.sleep(5)
                with open(description_file_path, "r", encoding="utf-8") as descricao:
                    descricao_kiwify = descricao.read()  
                input_field.send_keys("Resuma esse texto para a descrição de um eBook, escrevendo como se fosse o usuário, com no máximo 500 caracteres: ", descricao_kiwify)
                time.sleep(1)
                input_field.send_keys(Keys.ENTER)
                time.sleep(5000000)

                break
            else:
                print("button_copy_4 não encontrado")
                
        except TimeoutException:
            print("Tempo limite esgotado para encontrar o button_copy_4. Atualizando a página...")
            refresh_page(driver, responses_file, tittle_file, output_file, name, user_id)

        except Exception as e:
            print(f"Erro inesperado durante a execução: {e}")

'''
Variações dos elementos iteráveis:


button1 --> //*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[2]/div/div/div[2]/div/div[2]/div/div/span[1]/button
button1 --> //*[@id="__next"]/div[1]/div/main/div/div[1]/div[1]/div/div/div/div/article[2]/div/div/div[2]/div/div[2]/div/div/span[1]/button
button1 --> /html/body/div[1]/div/main/div/div[1]/div[1]/div/div/div/div/article[2]/div/div/div[2]/div/div[2]/div/div/span[1]/button/span
button1 --> /html/body/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[2]/div/div/div[2]/div/div[2]/div/div/span[1]/button

button2 --> //*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[4]/div/div/div[2]/div/div[2]/div/div/span[1]/button
button2 --> //*[@id="__next"]/div[1]/div/main/div/div[1]/div[1]/div/div/div/div/article[4]/div/div/div[2]/div/div[2]/div/div/span[1]/button
button2 --> /html/body/div[1]/div/main/div/div[1]/div[1]/div/div/div/div/article[4]/div/div/div[2]/div/div[2]/div/div/span[1]/button/span
button2 --> /html/body/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[4]/div/div/div[2]/div/div[2]/div/div/span[1]/button

button3 --> //*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[6]/div/div/div[2]/div/div[2]/div/div/span[1]/button
button3 --> //*[@id="__next"]/div[1]/div/main/div/div[1]/div[1]/div/div/div/div/article[6]/div/div/div[2]/div/div[2]/div/div/span[1]/button
button3 --> /html/body/div[1]/div/main/div/div[1]/div[1]/div/div/div/div/article[6]/div/div/div[2]/div/div[2]/div/div/span[1]/button/span
button3 --> /html/body/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[6]/div/div/div[2]/div/div[2]/div/div/span[1]/button

keep_generate --> //*[@id="__next"]/div[1]/div/main/div[1]/div[2]/div/div[1]/div/form/div/div[1]/div/div/div/div/button
keep_generate --> //*[@id="__next"]/div[1]/div/main/div/div[1]/div[2]/div/div[2]/div/form/div/div[1]/div/div/div/div/button
keep_generate --> /html/body/div[1]/div/main/div/div[1]/div[2]/div/div[2]/div/form/div/div[1]/div/div/div/div
keep_generate --> /html/body/div[1]/div/main/div/div[1]/div[2]/div/div[2]/div/form/div/div[1]/div/div/div/div/button
keep_generate --> /html/body/div[1]/div/main/div/div[1]/div[2]/div/div[2]/div/form/div/div[1]/div/div/div/div/button/div
keep_generate --> /html/body/div[1]/div/main/div/div[1]/div[2]/div/div[2]/div/form/div/div[1]/div/div/div/div/button/div/text()
keep_generate --> /html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div/form/div/div[1]/div/div/div/div/button

button4 --> //*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[2]/div/div/span[1]/button
button4 --> //*[@id="__next"]/div[1]/div/main/div/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[2]/div/div/span[1]/button
button4 --> /html/body/div[1]/div/main/div/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[2]/div/div/span[1]/button/span
button4 --> /html/body/div[1]/div/main/div/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[2]/div/div/span[1]/button
button4 --> /html/body/div[1]/div/main/div/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[2]/div/div/span[1]
button4 --> /html/body/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[2]/div/div/span[1]/button

erro --> /html/body/div[1]/div/main/div/div[1]/div[2]/div/div[2]/div[2]/button/div/text()
'''
