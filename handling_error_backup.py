import time
import pyautogui
import os
import sys
from send_prompt import send_prompts
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configura o limite de tentativas
MAX_ATTEMPTS = 3
ATTEMPT_COUNTER_ENV_VAR = 'ATTEMPT_COUNTER'

def kill_chrome_processes():
    try:
        os.system("taskkill /im chrome.exe /f")
        os.system("taskkill /im chromedriver.exe /f")
    except Exception as e:
        print(f"Erro ao encerrar os processos do Chrome: {e}")

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
        pass
    except Exception as e:
        pass
    return False

# Atualiza a página e chama a função de envio de prompts
def handle_error(driver, responses_file, tittle_file, name):
    attempt_counter = int(os.environ.get(ATTEMPT_COUNTER_ENV_VAR, 0))
    try:
        # Aguarda até que o elemento SVG esteja presente
        svg_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".flex.max-w-full.flex-col.flex-grow .text-token-text-error svg.icon-lg"))
        )
        
        if svg_element:
            print("Elemento SVG encontrado.")
            time.sleep(1)
            delete_files(['output.txt', 'tittle.txt'])
            time.sleep(1)
            
            try:
                driver.quit()
                print("Driver encerrado com sucesso.")
            except Exception as e:
                print(f"Erro ao encerrar o driver: {e}")
            kill_chrome_processes()
            time.sleep(1)
            
            # Incrementa o contador de tentativas e salva na variável de ambiente
            attempt_counter += 1
            os.environ[ATTEMPT_COUNTER_ENV_VAR] = str(attempt_counter)
            
            if attempt_counter >= MAX_ATTEMPTS:
                print("Erro: O limite de tentativas foi alcançado. O processo será encerrado.")
                sys.exit(1)
            
            # Reinicia o script
            print("Reiniciando o script...")
            os.execv(sys.executable, ['python'] + ['generate_Ebook.py'] + sys.argv[1:])
        else:
            print("Elemento SVG não encontrado.")
    except Exception as e:
        print(f"Erro ao tentar detectar o elemento SVG: {e}")
