import time
import threading
import psutil
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from handling_error import click_element_if_found, handle_error
from send_prompt import send_prompts
import os

# Lista para armazenar drivers ativos
current_tabs = []

# Função para verificar continuamente elementos no driver
def continuously_check_elements(driver):
    while True:
        try:
            found = click_element_if_found(driver)
            if found:
                print("Elemento HTML de login identificado.")
        except Exception as e:
            pass
        time.sleep(2)

# Função para verificar continuamente erros no driver
def continuously_check_errors(driver, responses_file, tittle_file, name):
    while True:
        try:
            handle_error(driver, responses_file, tittle_file, name)
            time.sleep(10)
        except Exception as e:
            pass
        time.sleep(2)

# Função para encerrar processos do Chrome relacionados ao driver específico
def kill_chrome_processes(driver):
    try:
        # Obtém o ID do processo do ChromeDriver associado ao driver
        driver_pid = driver.service.process.pid
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['name'] == 'chrome.exe' and 'chrome' in proc.info['cmdline']:
                # Verifica se o processo do Chrome é associado ao driver específico
                if str(driver_pid) in ' '.join(proc.info['cmdline']):
                    proc.terminate()  # Ou use proc.kill() se necessário
                    print(f"Terminando processo do Chrome: PID {proc.info['pid']}")
            elif proc.info['name'] == 'chromedriver.exe' and str(driver_pid) in ' '.join(proc.info['cmdline']):
                proc.terminate()  # Ou use proc.kill() se necessário
                print(f"Terminando processo do Chromedriver: PID {proc.info['pid']}")
    except Exception as e:
        print(f"Erro ao encerrar os processos do Chrome: {e}")

# Função de automação para cada usuário
def chatgpt_response(driver, user_id, responses_file, output_file, tittle_file, formatted_name, name):
    try:
        driver.get('https://chat.openai.com')
        print(f"Abrindo o site")

        while True:
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[1]/div[1]/div/div[1]/div/div[2]/div[1]'))
                )
                if element:
                    print("Elemento chatgpt encontrado")
                    break
            except Exception as e:
                print("Aguardando o elemento 'ChatGPT' antes de continuar...")
                time.sleep(2)

        while True:
            try:
                input_field = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="prompt-textarea"]'))
                )
                if input_field:
                    print("Elemento textarea encontrado")
                    break
            except Exception as e:
                print("Aguardando o elemento 'Textarea' antes de continuar...")
                time.sleep(2)

        while True:
            try:
                textarea = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
                if textarea:
                    textarea.click()
                    print("Elemento textarea clicado")
                    break
            except Exception as e:
                print("Aguardando o elemento 'Textarea' antes de clicar...")
                time.sleep(2)

        time.sleep(1)
        threading.Thread(target=continuously_check_elements, args=(driver,), daemon=True).start()
        threading.Thread(target=continuously_check_errors, args=(driver, responses_file, tittle_file, name), daemon=True).start()
        
        print("Chamando send_prompts()")
        send_prompts(driver, responses_file, tittle_file, output_file, name, user_id)
        time.sleep(5)

    finally:
        driver.close()
        time.sleep(1)
        kill_chrome_processes(driver)

'''
Elementos Variáveis


element --> //*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div[1]
element --> /html/body/div[1]/div/main/div/div[1]/div[1]/div/div[1]/div/div[3]
element --> /html/body/div[1]/div/main/div[1]/div[1]/div/div[1]/div/div[2]/div[1]
'''
