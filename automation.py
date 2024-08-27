import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from handling_error import click_element_if_found, handle_error
from send_prompt import send_prompts
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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
            with lock:
                handle_error(driver, responses_file, tittle_file, name)
            time.sleep(10)
        except Exception as e:
            pass
        time.sleep(2)

#
def chatgpt_response(responses_file, output_file, tittle_file, name):
    offsets = [
        (0, 0), (960, 0),
        (0, 540), (960, 540)
    ]
    window_width = 960
    window_height = 540

    drivers = []
    threads = []
    lock = threading.Lock()

    try:
        for offset in offsets:
            # Configurar o navegador com tamanho inicial pequeno
            chrome_options = Options()
            chrome_options.add_argument(f'--window-position={offset[0]},{offset[1]}')
            chrome_options.add_argument(f'--window-size={window_width},{window_height}')
            driver = uc.Chrome(version_main=126, options=chrome_options)
            
            # Abrir o navegador e ajustar a posição e o tamanho
            driver.get('about:blank')  # Carregar uma página em branco para garantir que o navegador seja inicializado
            driver.set_window_size(window_width, window_height)
            driver.set_window_position(offset[0], offset[1])

            drivers.append(driver)

            # Criar e iniciar a thread para automação
            thread = threading.Thread(target=lambda d=driver, o=offset: (
                (lambda: (
                    d.get('https://chat.openai.com'),
                    print(f"Abrindo o site na posição {o}"),
                    time.sleep(5),
                    (lambda: (
                        WebDriverWait(d, 20).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div/main/div[1]/div[1]/div/div[1]/div/div[2]'))
                        ),
                        print("Elemento chatgpt encontrado")
                    ))(),
                    (lambda: (
                        WebDriverWait(d, 20).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="prompt-textarea"]'))
                        ),
                        print("Elemento textarea encontrado")
                    ))(),
                    time.sleep(1),
                    d.find_element(By.XPATH, '//*[@id="prompt-textarea"]').click(),
                    time.sleep(1),
                    threading.Thread(target=continuously_check_elements, args=(d, lock), daemon=True).start(),
                    threading.Thread(target=continuously_check_errors, args=(d, responses_file, tittle_file, name, lock), daemon=True).start(),
                    print("Chamando send_prompts()"),
                    send_prompts(d, responses_file, tittle_file, output_file, name),
                    d.quit()
                ))()
            ))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    finally:
        # Garantir que todos os drivers sejam encerrados
        for driver in drivers:
            try:
                driver.quit()
            except Exception as e:
                print(f"Erro ao encerrar o driver: {e}")

        # Função fictícia para garantir que todos os processos do Chrome sejam encerrados
        kill_chrome_processes()

if __name__ == "__main__":
    chatgpt_response('responses.txt', 'output.txt', 'tittle.txt', name='Victor Mello')
