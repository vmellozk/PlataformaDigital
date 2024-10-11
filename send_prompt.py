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
import threading

#
mutex = Lock()

#
# Flags de controle para encerrar os loops
arrow_button_clicked = threading.Event()
keep_generate_clicked = threading.Event()
gerar_novamente_clicked = threading.Event()

#
def monitor_arrow_button(driver):
    while not arrow_button_clicked.is_set():
    #while True:
        try:
            arrow_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[1]/div[1]/div/div/div/div/button'))
            )
            if arrow_button:
                print("arrow_button encontrado")
                time.sleep(2)
                arrow_button.click()
                arrow_button_clicked.set()  # Sinaliza que o botão foi clicado
                break
        except TimeoutException:
            pass

def monitor_keep_generate(driver):
    while not keep_generate_clicked.is_set():
        try:
            keep_generate = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div/form/div/div[1]/div/div/div/div/button'))
            )
            if keep_generate:
                print("keep_generate encontrado")
                time.sleep(2)
                keep_generate.click()
                keep_generate_clicked.set()  # Sinaliza que o botão foi clicado
                break
        except TimeoutException:
            pass

# Obtém o campo de entrada para enviar um prompt e clica nele
def get_input_field(driver, timeout=30):
    try:
        input_field = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="prompt-textarea"]'))
        )
        input_field.click()
        return input_field
    except TimeoutException:
        print("Campo de entrada não encontrado.")
        return None

# Função para monitorar o erro: Gerar novamente, clicando nele para esperar a resposta
def monitor_gerar_novamente(driver):
    while not gerar_novamente_clicked.is_set():
        try:
            gerar_novamente = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/main/div[1]/div[2]/div/div[1]/div[2]/button/div"))
            )
            print("gerar_novamente encontrado")
            time.sleep(2)
            gerar_novamente.click()
            time.sleep(1)
            keep_generate_clicked.set()
            break
        except TimeoutException:
            pass

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
    #
    with open(responses_file, 'r', encoding='utf-8') as file:
        responses_text = file.read()

    #
    full_prompt = get_initial_prompt()

    # Obtendo o campo de entrada para enviar o primeiro prompt
    input_field = get_input_field(driver)
    if not input_field:
        return

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

    # Reutilizando a função para o próximo input field
    input_field = get_input_field(driver)
    if not input_field:
        return
    
    responses_prompt = responses(responses_text)
    full_responses = ''.join(responses_prompt)
    full_responses += '\n Ok, passei as respostas, mas não faça nada ainda. Responda apenas OK, nada mais! Aguarde as instruções.\n'
    send_text_with_line_breaks(input_field, full_responses)
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

    # Reutilizando a função para o próximo input field
    input_field = get_input_field(driver)
    if not input_field:
        return
    
    # Trecho responsável por enviar o prompt que pega o capa do eBook com o Título e Autor, cortando também o texto para salvar também o título do eBook
    tittle_prompt = tittle(name)
    for i in range(0, len(tittle_prompt), 1000):
        input_field.send_keys(tittle_prompt[i:i + 1000])
        time.sleep(2)
    input_field.send_keys(Keys.ENTER)
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

    # Reutilizando a função para o próximo input field
    input_field = get_input_field(driver)
    if not input_field:
        return

    confirmacao = 'OK, agora me forneça o restante do conteúdo. A introdução deve ser feita para ser utilizada como introdução e como descrição do conteúdo/eBook. Faça com que seja algo mais pessoal, abordando as respostas e, em alguns momentos em primeira pessoa, mas mantendo o profissionalismo. Lembrando da hash antes de: ####Introdução, ####Sumário, ####Conteúdo e ####Conclusão. Forneça esses tópicos assim e tudo em um único texto! Lembrando que quanto mais conteúdo foi fornecido de resposta, mais conteúdo será gerado. Apenas responda o que foi pedido, sem "essa foi a resposta, se precisar de mais..." não quero nada disso. Triplique o tamanho do conteúdo do ebook para cada tópico. Ou seja, me dê 3x mais de conteúdo para cada tópico do ebook do que o normal, tornando o ebook completo.'
    input_field.send_keys(confirmacao)
    time.sleep(1)
    input_field.send_keys(Keys.ENTER)

    # Iniciar threads para monitorar os botões
    arrow_button_thread = threading.Thread(target=monitor_arrow_button, args=(driver,))
    keep_generate_thread = threading.Thread(target=monitor_keep_generate, args=(driver,))
    gerar_novamente_thread = threading.Thread(target=monitor_gerar_novamente, args=(driver,))

    arrow_button_thread.start()
    keep_generate_thread.start()
    gerar_novamente_thread.start()

    while True:
        try:
            keep_generate = WebDriverWait(driver, 10).until(
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
            time.sleep(2)

        try:
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)  # Pressiona End para rolar até o final
            time.sleep(2)  # Aguardar novamente
            
            button_copy_4 = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[2]/div/div/span[1]/button'))
            )
            if button_copy_4:
                print("button_copy_4 encontrado")
                time.sleep(10)
                copied_text = copy_text(driver, '/html/body/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[2]/div/div/span[1]/button')
                with mutex:
                    with open(output_file, "w", encoding="utf-8") as file:
                        file.write(copied_text)
                time.sleep(1)
                break
            else:
                print("button_copy_4 não encontrado")

        except TimeoutException:
            print("Tempo limite esgotado para encontrar o button_copy_4. Atualizando a página...")
            refresh_page(driver, responses_file, tittle_file, output_file, name, user_id)

        except Exception as e:
            print(f"Erro inesperado durante a execução: {e}")

    #
    while True:
        try:
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
                description_file_path = os.path.join(user_folder, "descricao.txt")
                
                with open(description_file_path, "w", encoding="utf-8") as desc_file:
                    desc_file.write(description_content)
                    print(f"Conteúdo extraído salvo em: {description_file_path}")

            else:
                print("Palavras-chave 'Introdução' e 'Sumário' não encontradas no texto copiado.")
                pass

            #
            with open(description_file_path, "r", encoding="utf-8") as descricao:
                descricao_kiwify = descricao.read()

            # Reutilizando a função para o próximo input field
            input_field = get_input_field(driver)
            if not input_field:
                return
    
            time.sleep(1)
            input_field.send_keys("Reescreva a introdução como uma descrição para usar num site de vendas, NÃO ULTRAPASSANDO 400 caracteres, tem que ser abaixo de 400 caracteres contando com pontuações e espaços. Escrever como se fosse o usuário. Não ultrapasse 400 caracteres na resposta.", descricao_kiwify)
            time.sleep(5)
            #input_field.send_keys(Keys.ENTER)
            break

        except Exception as e:
            print("erro")
    
    #
    while True:
        try:
            # Simular o comportamento de pressionar as teclas Home e End para ajudar a localizar o botão
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME)  # Pressiona Home para rolar até o topo
            time.sleep(2)  # Aguardar para simular o movimento
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)  # Pressiona End para rolar até o final
            time.sleep(2)  # Aguardar novamente

            arrow_botton = WebDriverWait(driver, 10).until(
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
            # Simular o comportamento de pressionar as teclas Home e End para ajudar a localizar o botão
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME)  # Pressiona Home para rolar até o topo
            time.sleep(2)  # Aguardar para simular o movimento
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)  # Pressiona End para rolar até o final
            time.sleep(2)  # Aguardar novamente

            button_copy_5 = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[10]/div/div/div[2]/div/div[2]/div/div[2]/span[1]/button'))
            )
            if button_copy_5:
                print("button_copy_5 encontrado")
                
                # Copia o conteúdo clicando no botão
                time.sleep(1)
                desc_text = copy_text(driver, '/html/body/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[10]/div/div/div[2]/div/div[2]/div/div[2]/span[1]/button')
                time.sleep(5)
                
                # Define o arquivo correto para salvar o conteúdo (exemplo: descricao_product.txt)
                user_folder = os.path.join("users", str(user_id))  # Define o caminho do diretório do usuário
                description_file_path = os.path.join(user_folder, "descricao_product.txt")  # Define o nome do arquivo de descrição

                # Usa o mutex para garantir a escrita correta no arquivo
                with mutex:
                    with open(description_file_path, "w", encoding="utf-8") as file:
                        file.write(desc_text)  # Salva o conteúdo copiado no arquivo correto
                        print(f"Conteúdo copiado salvo em: {description_file_path}")
                
                time.sleep(1)
                # Caminho para o arquivo descricao.txt
                descricao_txt_path = os.path.join(user_folder, "descricao.txt")
                if os.path.exists(descricao_txt_path):
                    os.remove(descricao_txt_path)
                    print(f"Arquivo {descricao_txt_path} removido com sucesso.")
                else:
                    print(f"Arquivo {descricao_txt_path} não encontrado.")

                break
            else:
                print("Erro: button_copy_5 não encontrado")

        except Exception as e:
            print(f"Erro inesperado ao copiar e salvar o texto do button_copy_5: {e}")

    # Finalizando as threads
    arrow_button_clicked.set()
    keep_generate_clicked.set()
    gerar_novamente_clicked.set()

    # Espera que as threads terminem antes de continuar
    arrow_button_thread.join()
    keep_generate_thread.join()
    gerar_novamente_thread.join()

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
