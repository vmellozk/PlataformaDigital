import time
import pyautogui
import os
from send_prompt_teste_1 import send_prompts
from selenium.webdriver.common.by import By

# Apaga arquivos específicos
def delete_files(file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)

# Verifica se a imagem 'image_path' está na tela e clica na imagem 'click_image_path' se encontrada
def click_image_if_found(image_path, click_image_path):
    try:
        image_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.7)
        if image_location:
            time.sleep(1)
            click_location = pyautogui.locateCenterOnScreen(click_image_path, confidence=0.7)
            if click_location:
                pyautogui.click(click_location)
                time.sleep(1)
                return True
        return False
    except pyautogui.ImageNotFoundException:
        # adicionar um logging
        pass
    except Exception as e:
        # adicionar um logging
        pass
    return False

# Atualiza a página e chama a função de envio de prompts
def handle_error(driver, input_field, responses_file, tittle_file, name):
    if pyautogui.locateCenterOnScreen('static/error/error_symbol.png', confidence=0.7):
        time.sleep(1)
        delete_files(['output.txt', 'tittle.txt'])
        pyautogui.hotkey('f5')
        time.sleep(5)  # Aguarda o tempo necessário para a página ser atualizada

        input_field = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
        time.sleep(1)
        input_field.click()
        time.sleep(1)

        send_prompts(input_field, responses_file, tittle_file, name)