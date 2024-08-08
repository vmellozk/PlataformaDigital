import time
import pyautogui
import pyperclip
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from prompt import get_initial_prompt, responses, tittle
from error_handling import click_image_if_found 
import threading

# Declara a variável global para 
image_check_thread = None

# Verifica continuamente se a imagem está presente e clica na imagem especificada.
def continuously_check_images():
    while True:
        try:
            found = click_image_if_found('static/error/thanks_for_use_error.png', 'static/error/continue_desconected.png')
            if found:
                pass
        except Exception as e:
            pass
        time.sleep(2)

# Declara que vamos usar a variável global e 
def chatgpt_response(responses_file, output_file, tittle_file, name):
    global image_check_thread
    driver = uc.Chrome(version_main=126)

    try:
        #
        driver.maximize_window()
        driver.get('https://chat.openai.com')
        time.sleep(2)

        # Inicia a verificação contínua em uma thread separada
        image_check_thread = threading.Thread(target=continuously_check_images, daemon=True)
        image_check_thread.start()

        #
        input_field = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
        time.sleep(1)
        input_field.click()
        time.sleep(1)

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

        # Prompt 2
        responses_prompt = responses(responses_text)
        for i in range(0, len(responses_prompt), 5000):
            input_field.send_keys(responses_prompt[i:i + 5000])
            time.sleep(1)
        input_field.send_keys(Keys.ENTER)
        time.sleep(15)

        # Prompt 3
        tittle_prompt = tittle(name)
        for i in range(0, len(tittle_prompt), 1000):
            input_field.send_keys(tittle_prompt[i:i + 1000])
            time.sleep(2)
        input_field.send_keys(Keys.ENTER)
        time.sleep(8)

        # Aguarda a resposta ser gerada e o botão de copiar estar disponível
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
                print(f"Erro durante a automação: {e}")
                time.sleep(1)

        #
        copied_tittle = pyperclip.paste()
        with open(tittle_file, "w", encoding="utf-8") as file:
            file.write(copied_tittle)
        time.sleep(1)
    
        #
        confirmacao = 'OK, agora me forneça o restante do conteúdo. Lembrando da hash antes de: ####Introdução, ####Sumário, ####Conteúdo e ####Conclusão. Forneça esses tópicos assim e tudo em um único texto! Apenas responda o que foi pedido, sem "essa foi a resposta, se precisar de mais..." não quero nada disso. '
        input_field.send_keys(confirmacao)
        time.sleep(1)
        input_field.send_keys(Keys.ENTER)
        time.sleep(45)

        # Aguarda a resposta ser gerada e o botão de copiar estar disponível
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
                print(f"Erro durante a automação: {e}")
                time.sleep(1)

        #
        copied_text = pyperclip.paste()
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(copied_text)
            time.sleep(1)

    finally:
        # Encerrar a verificação contínua
        if image_check_thread is not None:
            image_check_thread.join(timeout=10)
        try:
            driver.quit()
        except Exception as e:
            print(f"Erro ao encerrar o driver: {e}")
