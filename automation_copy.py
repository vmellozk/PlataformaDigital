import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pyperclip
import pyautogui
from prompt import (get_cover_prompt, get_intro_prompt, get_table_of_contents_prompt,
                           get_content_prompt, get_conclusion_prompt, get_final_conclusion_prompt)

def chatgpt_response(prompt_file, output_file):
    driver = uc.Chrome(version_main=126)

    try:
        driver.get('https://chat.openai.com')
        time.sleep(2)

        input_field = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
        time.sleep(0.5)
        input_field.click()
        time.sleep(0.5)

        # Lê o texto do arquivo de prompt
        with open(prompt_file, 'r', encoding='utf-8') as file:
            prompt_text = file.read()

        # Envia o prompt e obtém a resposta
        for i in range(0, len(prompt_text), 5000):
            input_field.send_keys(prompt_text[i:i + 5000])
            time.sleep(1)
        input_field.send_keys(Keys.ENTER)
        time.sleep(90)

        # Localiza o botão de copiar e clica nele
        try:
            print("Tentando localizar o botão de copiar.")
            copy_button_location = pyautogui.locateCenterOnScreen('static/images/button_copy_gpt.png', confidence=0.8)
            if copy_button_location:
                pyautogui.click(copy_button_location)
                time.sleep(1)
                copied_text = pyperclip.paste()
                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(copied_text)
                print("Texto copiado e salvo com sucesso.")
            else:
                print("Botão de copiar não encontrado.")

        except Exception as e:
            print(f"Erro durante a automação: {e}")

    finally:
        try:
            driver.quit()
        except Exception as e:
            print(f"Erro ao encerrar o driver: {e}")

def generate_ebook_parts(name, responses_text):
    prompts = {
        'cover': get_cover_prompt(name),
        'intro': get_intro_prompt(),
        'toc': get_table_of_contents_prompt(),
        'content': get_content_prompt(responses_text),
        'conclusion': get_conclusion_prompt(),
        'final_conclusion': get_final_conclusion_prompt()
    }
    
    for part, prompt_text in prompts.items():
        prompt_file = f'{part}_prompt.txt'
        output_file = f'{part}_output.txt'
        
        with open(prompt_file, 'w', encoding='utf-8') as file:
            file.write(prompt_text)
        
        print(f"Processando {part}...")
        chatgpt_response(prompt_file, output_file)
        print(f"{part.capitalize()} processado e salvo.")
