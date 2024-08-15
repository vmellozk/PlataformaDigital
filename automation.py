import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from handling_error import click_image_if_found, handle_error
from send_prompt import send_prompts
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import pyautogui
import os

#
image_check_thread = None
error_check_thread = None

def kill_chrome_processes():
    try:
        os.system("taskkill /im chrome.exe /f")
        os.system("taskkill /im chromedriver.exe /f")
    except Exception as e:
        print(f"Erro ao encerrar os processos do Chrome: {e}")

#
def continuously_check_images():
    while True:
        try:
            found = click_image_if_found('static/error/thanks_for_use_error.png', 'static/error/continue_desconected.png')
            if found:
                pass
        except Exception as e:
            pass
        time.sleep(2)

#
def continuously_check_errors(driver, responses_file, tittle_file, name):
    while True:
        try:
            handle_error(driver, responses_file, tittle_file, name)
            time.sleep(10)
        except Exception as e:
            pass
        time.sleep(2)

#
def chatgpt_response(responses_file, output_file, tittle_file, name):
    global image_check_thread, error_check_thread
    driver = uc.Chrome(version_main=126)

    try:
        driver.maximize_window()
        driver.get('https://chat.openai.com')
        time.sleep(3)

        while not pyautogui.locateCenterOnScreen('static/images/chatgpt.png'):
            print("Aguardando a imagem 'chatgpt.png' antes de continuar...")
            time.sleep(2)

        input_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="prompt-textarea"]'))
        )
        time.sleep(1)
        input_field.click()
        time.sleep(1)

        image_check_thread = threading.Thread(target=continuously_check_images, daemon=True)
        image_check_thread.start()
        
        # Passa os argumentos como uma tupla
        error_check_thread = threading.Thread(target=continuously_check_errors, args=(driver, responses_file, tittle_file, name), daemon=True)
        error_check_thread.start()

        send_prompts(driver, responses_file, tittle_file, name)

    finally:
        if image_check_thread is not None:
            image_check_thread.join(timeout=5)
        if error_check_thread is not None:
            error_check_thread.join(timeout=5)
        try:
            driver.quit()
        except Exception as e:
            print(f"Erro ao encerrar o driver: {e}")
        kill_chrome_processes()
