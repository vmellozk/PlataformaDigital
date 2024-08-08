import time
import pyautogui
import pyperclip
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from prompt import get_initial_prompt, responses, tittle

output_file = 'output.txt'
responses_file = 'responses.txt'

def send_prompts(driver, responses_file=responses_file, tittle_file='tittle.txt', name='default_name'):
    def get_input_field():
        return driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')

    # Lê o texto do arquivo de respostas
    with open(responses_file, 'r', encoding='utf-8') as file:
        responses_text = file.read()

    # Prompt 1
    full_prompt = get_initial_prompt()
    input_field = get_input_field()
    for i in range(0, len(full_prompt), 5000):
        input_field.send_keys(full_prompt[i:i + 5000])
        time.sleep(1)
    input_field.send_keys(Keys.ENTER)
    time.sleep(10)

    # Prompt 2
    responses_prompt = responses(responses_text)
    input_field = get_input_field()
    for i in range(0, len(responses_prompt), 5000):
        input_field.send_keys(responses_prompt[i:i + 5000])
        time.sleep(1)
    input_field.send_keys(Keys.ENTER)
    time.sleep(20)

    # Prompt 3
    tittle_prompt = tittle(name)
    input_field = get_input_field()
    for i in range(0, len(tittle_prompt), 1000):
        input_field.send_keys(tittle_prompt[i:i + 1000])
        time.sleep(2)
    input_field.send_keys(Keys.ENTER)
    time.sleep(7)

    # Aguarda a resposta ser gerada e o botão de copiar estar disponível e salvar num arquivo txt
    while True:
        try:
            copy_button_location = pyautogui.locateCenterOnScreen('static/images/button_copy_chat_gpt.png')
            if copy_button_location:
                pyautogui.click(copy_button_location)
                time.sleep(2)
                break
            else:
                print("Botão de copiar não encontrado.")
                time.sleep(1)
        except Exception as e:
            print(f"Erro durante a automação de copiar: {e}")
            time.sleep(1)

    copied_tittle = pyperclip.paste()
    with open(tittle_file, "w", encoding="utf-8") as file:
        file.write(copied_tittle)
    time.sleep(1)

    confirmacao = 'OK, agora me forneça o restante do conteúdo. Lembrando da hash antes de: ####Introdução, ####Sumário, ####Conteúdo e ####Conclusão. Forneça esses tópicos assim e tudo em um único texto! Apenas responda o que foi pedido, sem "essa foi a resposta, se precisar de mais..." não quero nada disso. '
    input_field = get_input_field()
    input_field.send_keys(confirmacao)
    time.sleep(1)
    input_field.send_keys(Keys.ENTER)
    time.sleep(55)

    # Verifica a presença do botão 'emoji_gpt.png' e realiza ações associadas
    while True:
        try:
            button_location = pyautogui.locateCenterOnScreen('static/images/emoji_gpt1.png')
            if button_location is None:
                button_location = pyautogui.locateCenterOnScreen('static/images/emoji_gpt2.png')
            if button_location is None:
                button_location = pyautogui.locateCenterOnScreen('static/images/seta.png')
            if button_location is None:
                button_location = pyautogui.locateCenterOnScreen('static/images/introducao.png')
            if button_location is None:
                button_location = pyautogui.locateCenterOnScreen('static/images/sumario.png')
            if button_location is None:
                button_location = pyautogui.locateCenterOnScreen('static/images/conteudo.png')
            if button_location:
                pyautogui.click(button_location)
                time.sleep(1)
                pyautogui.press('end')
                time.sleep(3)
                break
            else:
                print("Nenhum botão 'emoji_gpt' encontrado.")
                time.sleep(1)
        except Exception as e:
            print(f"Erro durante a automação para achar o emoji: {e}")
            time.sleep(1)

    # Verifica a presença do botão 'button_copy_chat_gpt.png' e realiza ações associadas
    while True:
        try:
            copy_button_location = pyautogui.locateCenterOnScreen('static/images/button_copy_chat_gpt.png')
            if copy_button_location:
                pyautogui.click(copy_button_location)
                time.sleep(2)
                break
            else:
                print("Botão de copiar não encontrado.")
                time.sleep(1)
        except Exception as e:
            print(f"Erro durante a automação de copiar a mensagem: {e}")
            time.sleep(1)
    copied_text = pyperclip.paste()
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(copied_text)
    time.sleep(1)
