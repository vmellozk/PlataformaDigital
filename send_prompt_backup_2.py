import time
import pyperclip
from selenium.webdriver.common.keys import Keys
from prompt import get_initial_prompt, responses, tittle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from threading import Lock
from selenium.webdriver.chrome.options import Options

# Criação de um mutex para garantir que não haja conflitos entre múltiplas instâncias
mutex = Lock()

#
def copy_text(driver, button_xpath):
    while True:
        try:
            button_element = WebDriverWait(driver, 10).until(
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
            print("Tempo limite esgotado para encontrar o botão de copiar. Tentando novamente...")
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

def send_prompts(driver, responses_file, tittle_file, output_file, name):
    #
    def get_input_field():
        return WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="prompt-textarea"]'))
        )
    input_field = get_input_field()

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
            button_copy_1 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[2]/div/div/div[2]/div/div[2]/div/div/span[1]/button'))
            )
            if button_copy_1:
                print("button_copy_1 encontrado")
                time.sleep(1)
                break
            else:
                print("button_copy_1 não encontrado")
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
            button_copy_2 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[4]/div/div/div[2]/div/div[2]/div/div/span[1]/button'))
            )
            if button_copy_2:
                print("button_copy_2 encontrado")
                time.sleep(1)
                break
            else:
                print("button_copy_2 não encontrado")
        except Exception as e:
            print(f"Erro ao encontrar o button_copy_2: {e}")
            time.sleep(1)

    #
    tittle_prompt = tittle(name)
    for i in range(0, len(tittle_prompt), 1000):
        input_field.send_keys(tittle_prompt[i:i + 1000])
        time.sleep(2)
    input_field.send_keys(Keys.ENTER)
    input_field = get_input_field()
    while True:
        try:
            button_copy_3 = '//*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[6]/div/div/div[2]/div/div[2]/div/div/span/button'
            if button_copy_3:
                print("button_copy_3 encontrado")
                time.sleep(2)
                copied_tittle = copy_text(driver, button_copy_3)
                
                with mutex:
                    with open(tittle_file, "w", encoding="utf-8") as file:
                        file.write(copied_tittle)
                time.sleep(1)
                break
            else:
                print("button_copy_3 não encontrado")
        except Exception as e:
            print(f"Erro ao encontrar o button_copy_3: {e}")
            time.sleep(1)

    #
    confirmacao = 'OK, agora me forneça o restante do conteúdo. Faça com que seja algo mais pessoal, abordando as respostas e, em alguns momentos em primeira pessoa, mas mantendo o profissionalismo. Lembrando da hash antes de: ####Introdução, ####Sumário, ####Conteúdo e ####Conclusão. Forneça esses tópicos assim e tudo em um único texto! Lembrando que quanto mais conteúdo foi fornecido de resposta, mais conteúdo será gerado. Apenas responda o que foi pedido, sem "essa foi a resposta, se precisar de mais..." não quero nada disso. Triplique o tamanho do conteúdo do ebook para cada tópico. Ou seja, me dê 3x mais de conteúdo para cada tópico do ebook do que o normal, tornando o ebook completo.'
    input_field.send_keys(confirmacao)
    time.sleep(1)
    input_field.send_keys(Keys.ENTER)
    while True:
        try:
            keep_generate = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div/main/div[1]/div[2]/div[1]/div/form/div/div[1]/div/div/div/div/button'))
            )
            if keep_generate:
                print("Botão de continuar gerando texto encontrado")
                time.sleep(2)
                keep_generate.click()

                try:
                    response_button_xpath = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[2]/div/div/span/button'))
                    )
                    if response_button_xpath:
                        print("Botão de copiar resposta encontrado")
                        time.sleep(2)
                        copied_text = copy_text(driver, '//*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[2]/div/div/span/button')
                        with mutex:
                            with open(output_file, "w", encoding="utf-8") as file:
                                file.write(copied_text)
                        time.sleep(1)
                        break
                except TimeoutException:
                    print("Tempo limite esgotado para encontrar o botão de copiar resposta após clicar em 'keep_generate'. Tentando novamente...")
            else:
                print("Botão de continuar gerando texto não foi encontrado")

                try:
                    response_button_xpath = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[2]/div/div/span/button'))
                    )
                    if response_button_xpath:
                        print("Botão de copiar resposta encontrado")
                        time.sleep(2)
                        copied_text = copy_text(driver, '//*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[2]/div/div/span/button')
                        with mutex:
                            with open(output_file, "w", encoding="utf-8") as file:
                                file.write(copied_text)
                        time.sleep(1)
                        break
                except TimeoutException:
                    print("Tempo limite esgotado para encontrar o botão de copiar resposta diretamente. Tentando novamente...")

        except Exception as e:
            print(f"Erro inesperado durante a execução: {e}")
