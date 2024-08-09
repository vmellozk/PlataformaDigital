from send_prompt import send_prompts
from selenium.webdriver.common.by import By
import time
import pyautogui
import os

# Apaga arquivos específicos
def delete_files(file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)

# Atualiza a página e reinicia o script
def handle_error(driver, responses_file, tittle_file, name):
    if pyautogui.locateCenterOnScreen('static/error/network_error.png', confidence=0.7):
        time.sleep(1)
        delete_files(['output.txt', 'tittle.txt'])
        pyautogui.hotkey('f5')
        time.sleep(7)

        input_field = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
        time.sleep(1)
        input_field.click()
        time.sleep(1)
        
        # Verifica se responses_file existe e não está vazio
        if os.path.exists(responses_file) and os.path.getsize(responses_file) > 0:
            send_prompts(driver, responses_file, tittle_file, name)
        else:
            print(f"Arquivo {responses_file} não encontrado ou está vazio.")

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
        # Adicionar logging aqui
        pass
    except Exception as e:
        # Adicionar logging aqui
        pass
    return False
