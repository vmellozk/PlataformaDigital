import time
import os
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from dotenv import load_dotenv
import pyperclip
import pyautogui
from prompt import get_initial_prompt, get_cover_prompt, get_table_of_contents_prompt, get_intro_prompt, get_content_prompt, get_conclusion_prompt, responses

def chatgpt_response(responses_file, output_directory, name):
    driver = uc.Chrome(version_main=126)

    # Cria o diretório de saída se não existir
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    try:
        # Abre o navegador e define o tempo máximo de espera
        driver.get('https://chat.openai.com')
        driver.maximize_window()
        wait = WebDriverWait(driver, 5)

         # Fazendo login na plataforma
        time.sleep(2)
        load_dotenv()
        email = os.getenv('EMAIL_GPT')
        password = os.getenv('PASSWORD_GPT')

        def click_image(image_path):
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
            if location:
                pyautogui.click(location)
                return True
            else:
                return False

        # Tente clicar nas imagens
        if not click_image('static/images/entrar.png'):
            return
        time.sleep(3)
        if not click_image('static/images/email_chat_gpt.png'):
            return
        time.sleep(1)
        pyautogui.write(email)
        time.sleep(1)
        if not click_image('static/images/continuar.png'):
            return
        time.sleep(3)
        if not click_image('static/images/senha.png'):
            return
        time.sleep(1)
        pyautogui.write(password)
        time.sleep(1)
        if not click_image('static/images/continuar_avancar.png'):
            return
        time.sleep(6)

        # Espera até que o campo de entrada esteja presente e clicável
        input_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="prompt-textarea"]'))
    )
        driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
        time.sleep(1)
        input_field.click()

        # Lê o texto do arquivo de respostas
        with open(responses_file, 'r', encoding='utf-8') as file:
            responses_text = file.read()

        # Criei uma lista das funções dos prompts para não ter que repetir o for em cada um prompt
        prompts = [
            (get_initial_prompt(), None),
            (responses(responses_text), None, 10),
            (get_cover_prompt(name), 'capa.txt', 5),
            (get_table_of_contents_prompt(), 'sumario.txt', 7),
            (get_intro_prompt(), 'introducao.txt', 20),
            (get_content_prompt(), 'conteudoprincipal.txt', 120),
            (get_conclusion_prompt(), 'conclusao.txt', 40)
        ]

        #
        for prompt_text, filename, *wait_time in prompts:
            for i in range(0, len(prompt_text), 5000):
                input_field.send_keys(prompt_text[i:i + 5000])
                time.sleep(1)
            time.sleep(3)
            input_field.send_keys(Keys.ENTER)
            
            if wait_time:
                time.sleep(wait_time[0])
            else:
                time.sleep(3)

            # Verifica se o filename é None antes de tentar copiar e salvar o texto
            if filename:
                try:
                    # Aguarda o botão de copiar para clicar
                    while True:
                        button_location = pyautogui.locateCenterOnScreen('static/images/button_copy_chat_gpt.png', confidence=0.8)
                        if button_location:
                            pyautogui.click(button_location)
                            break
                        time.sleep(0.5)
                    
                    time.sleep(1)
                    copied_text = pyperclip.paste()

                    # Salva a resposta em um arquivo separado
                    with open(f"{output_directory}/{filename}", "w", encoding="utf-8") as file:
                        file.write(copied_text)

                    # Recupera o campo de entrada novamente antes de enviar o próximo prompt
                    input_field.click()
                    time.sleep(3)

                except Exception as e:
                    print(f"Erro durante a automação para {filename}: {e}")

    finally:
        try:
            driver.quit()
        except Exception as e:
            print(f"Erro ao encerrar o driver: {e}")

if __name__ == "__main__":
    chatgpt_response('responses.txt', 'output_directory', 'name')