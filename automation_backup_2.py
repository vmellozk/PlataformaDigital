import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from handling_error import click_element_if_found, handle_error
from send_prompt import send_prompts
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import os

# Função
def kill_chrome_processes():
    try:
        os.system("taskkill /im chrome.exe /f")
        os.system("taskkill /im chromedriver.exe /f")
    except Exception as e:
        print(f"Erro ao encerrar os processos do Chrome: {e}")

#
def continuously_check_elements(driver, lock):
    while True:
        try:
            with lock:  # Sincroniza acesso ao driver
                found = click_element_if_found(driver)
                if found:
                    print("Elemento HTML de loguin identificado.")
        except Exception as e:
            pass
        time.sleep(2)

#
def continuously_check_errors(driver, responses_file, tittle_file, name, lock):
    while True:
        try:
            with lock:  # Sincroniza acesso ao driver
                handle_error(driver, responses_file, tittle_file, name)
            time.sleep(10)
        except Exception as e:
            pass
        time.sleep(2)

#
def chatgpt_response(responses_file, output_file, tittle_file, name):
    driver = uc.Chrome(version_main=126)
    image_check_thread = None
    error_check_thread = None
    lock = threading.Lock()

    try:
        #
        driver.maximize_window()
        driver.get('https://chat.openai.com')
        time.sleep(5)

        #
        while True:
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div[1]/div/div[2]'))
                )
                if element:
                    break
            except Exception as e:
                print("Aguardando o elemento 'ChatGPT' antes de continuar...")
                time.sleep(2)

        #
        input_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="prompt-textarea"]'))
        )
        time.sleep(1)
        input_field.click()
        time.sleep(1)

        #
        image_check_thread = threading.Thread(target=continuously_check_elements, args=(driver, lock), daemon=True)
        image_check_thread.start()
        error_check_thread = threading.Thread(target=continuously_check_errors, args=(driver, responses_file, tittle_file, name, lock), daemon=True)
        error_check_thread.start()

        #
        send_prompts(driver, responses_file, tittle_file, output_file, name)

    finally:
        #
        if image_check_thread is not None:
            print("Aguardando o término da thread image_check_thread")
            image_check_thread.join(timeout=5)
        if error_check_thread is not None:
            print("Aguardando o término da thread error_check_thread")
            error_check_thread.join(timeout=5)
        try:
            driver.quit()
        except Exception as e:
            print(f"Erro ao encerrar o driver: {e}")
        kill_chrome_processes()
