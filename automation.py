import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pyperclip
import pyautogui
from prompt import get_full_prompt, get_responses_prompt

def chatgpt_response(responses_file, output_file, name):
    driver = uc.Chrome(version_main=126)

    try:
        driver.get('https://chat.openai.com')
        time.sleep(2)

        input_field = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
        time.sleep(0.5)
        input_field.click()
        time.sleep(0.5)

        # Lê o texto do arquivo de respostas
        with open(responses_file, 'r', encoding='utf-8') as file:
            responses_text = file.read()

        # Prompt 1
        full_prompt = get_full_prompt(name)
        for i in range(0, len(full_prompt), 5000):
            input_field.send_keys(full_prompt[i:i + 5000])
            time.sleep(1)
        input_field.send_keys(Keys.ENTER)
        time.sleep(2.5)

        # Prompt 2
        responses_prompt = get_responses_prompt(responses_text)
        for i in range(0, len(responses_prompt), 5000):
            input_field.send_keys(responses_prompt[i:i + 5000])
            time.sleep(1)
        input_field.send_keys(Keys.ENTER)
        
        time.sleep(90)

        # Aguarda a resposta ser gerada e o botão de copiar estar disponível
        #WebDriverWait(driver, 90).until(
            #EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Copiar código')]"))
        #)

        # Localiza o botão de copiar e clica nele
        try:
            print("Tentando localizar o botão de copiar.")
            pyautogui.click(pyautogui.locateCenterOnScreen('static/images/button_copy_gpt.png'))
            time.sleep(1)
            copied_text = pyperclip.paste()
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(copied_text)

        except Exception as e:
            print(f"Erro durante a automação: {e}")

    finally:
        try:
            driver.quit()
        except Exception as e:
            print(f"Erro ao encerrar o driver: {e}")

