import time
import pyperclip
from selenium.webdriver.common.keys import Keys
from prompt import get_initial_prompt, responses, tittle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

output_file = 'output.txt'

#
def copy_text(driver, button_xpath):
    while True:
        try:
            button_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, button_xpath))
            )
            if button_element:
                button_element.click()
                time.sleep(2)
                break
            else:
                print("Botão de copiar não encontrado.")
                time.sleep(1)
        except Exception as e:
            print(f"Erro durante o copiar resposta: {e}")
            time.sleep(1)
    copied_text = pyperclip.paste()
    return copied_text

def send_prompts(driver, responses_file, tittle_file, name):
    # Reencontrar o campo de entrada para garantir que ele seja válido
    def get_input_field():
        return WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="prompt-textarea"]'))
        )
    input_field = get_input_field()

    # Lê o texto do arquivo de respostas
    with open(responses_file, 'r', encoding='utf-8') as file:
        responses_text = file.read()

    # Prompt 1
    full_prompt = get_initial_prompt()
    for i in range(0, len(full_prompt), 5000):
        input_field.send_keys(full_prompt[i:i + 5000])
        time.sleep(1)
    input_field.send_keys(Keys.ENTER)
    time.sleep(5)
    # Reencontrar o campo de entrada
    input_field = get_input_field()
    
    # Prompt 2
    responses_prompt = responses(responses_text)
    for i in range(0, len(responses_prompt), 5000):
        input_field.send_keys(responses_prompt[i:i + 5000])
        time.sleep(1)
    input_field.send_keys(Keys.ENTER)
    time.sleep(15)
    input_field = get_input_field()

    # Prompt 3
    tittle_prompt = tittle(name)
    for i in range(0, len(tittle_prompt), 1000):
        input_field.send_keys(tittle_prompt[i:i + 1000])
        time.sleep(2)
    input_field.send_keys(Keys.ENTER)
    time.sleep(8)
    input_field = get_input_field()

    # Aguarda a resposta ser gerada e o botão de copiar estar disponível e salvar num arquivo txt
    tittle_button_xpath = '//*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[6]/div/div/div[2]/div/div[2]/div/div/span/button'
    copied_tittle = copy_text(driver, tittle_button_xpath)
    with open(tittle_file, "w", encoding="utf-8") as file:
        file.write(copied_tittle)
    time.sleep(1)

    confirmacao = 'OK, agora me forneça o restante do conteúdo. Lembrando da hash antes de: ####Introdução, ####Sumário, ####Conteúdo e ####Conclusão. Forneça esses tópicos assim e tudo em um único texto! Lembrando que quanto mais conteúdo foi fornecido de resposta, mais conteúdo será gerado. Apenas responda o que foi pedido, sem "essa foi a resposta, se precisar de mais..." não quero nada disso. Triplique o tamanho da sua resposta padrão. Ou seja, me dê 3x mais de conteúdo para o ebook.'
    input_field.send_keys(confirmacao)
    time.sleep(1)
    input_field.send_keys(Keys.ENTER)
    time.sleep(60)

    # Clique no elemento encontrado e rola até o final da página
    while True:
        try:
            button_location = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"ChatGPT")]//span[contains(text(),"4o mini")]'))
            )
            if button_location:
                button_location.click()
                time.sleep(1)
                button_location.click()
                time.sleep(1)
                
                body = driver.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.END)
                time.sleep(3)
                break
            else:
                print("imagem chatgpt nao encontrada")
                time.sleep(1)
        except Exception as e:
            print(f"Erro para descer a página: {e}")
            time.sleep(2)

    # Aguarda a resposta ser gerada e o botão de copiar estar disponível e salvar num arquivo txt
    response_button_xpath = '//*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div/div/div/article[8]/div/div/div[2]/div/div[2]/div/div/span/button'
    copied_text = copy_text(driver, response_button_xpath)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(copied_text)
    time.sleep(1)
