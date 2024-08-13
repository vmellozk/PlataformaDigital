import time
import pyautogui
import os
import sys
from send_prompt_teste_4 import send_prompts
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
def handle_error(driver, responses_file, tittle_file, name):
    try:
        # Verifica se o símbolo de erro está presente na tela
        if pyautogui.locateCenterOnScreen('static/error/error_symbol.png', confidence=0.7):
            time.sleep(1)
            # Deleta os arquivos especificados se existirem
            delete_files(['output.txt', 'tittle.txt'])
            time.sleep(1)
            
            # Fecha o navegador
            driver.quit()
            time.sleep(3)
            os.execv(sys.executable, ['python', 'automation_teste_4.py'] + sys.argv[1:])

    except Exception as e:
        pass
        # Opcional: Se houver um erro ao tentar reiniciar, o programa pode ser encerrado
        # os._exit(1)
