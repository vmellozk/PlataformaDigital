import time
import threading
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from handling_error import click_element_if_found, handle_error
from send_prompt import send_prompts
import os

# Função para encerrar processos do Chrome
def kill_chrome_processes():
    try:
        os.system("taskkill /im chrome.exe /f")
        os.system("taskkill /im chromedriver.exe /f")
    except Exception as e:
        print(f"Erro ao encerrar os processos do Chrome: {e}")

# Função para verificar continuamente elementos no driver
def continuously_check_elements(driver, lock):
    while True:
        try:
            with lock:  # Sincroniza acesso ao driver
                found = click_element_if_found(driver)
                if found:
                    print("Elemento HTML de login identificado.")
        except Exception as e:
            pass
        time.sleep(2)

# Função para verificar continuamente erros no driver
def continuously_check_errors(driver, responses_file, tittle_file, name, lock):
    while True:
        try:
            with lock:
                handle_error(driver, responses_file, tittle_file, name)
            time.sleep(10)
        except Exception as e:
            pass
        time.sleep(2)

# Função de automação para cada usuário
def chatgpt_response(driver, user_id, responses_file, output_file, tittle_file, name):
    # Determinar o número de abas a serem abertas com base na capacidade e necessidade
    MAX_TABS = 4
    current_tabs = threading.active_count()  # Verifica o número de abas atuais
    needed_tabs = min(MAX_TABS - current_tabs, 1)  # Abre até uma aba por vez

    # Definir posições e tamanhos para até 4 abas na tela
    offsets = [(0, 0), (960, 0), (0, 540), (960, 540)]
    window_width = 960
    window_height = 540

    drivers = []
    threads = []
    lock = threading.Lock()

    try:
        for offset in offsets:
            if len(drivers) >= MAX_TABS:
                break  # Não abra mais de 4 abas

            # Configurar o navegador com tamanho inicial pequeno
            chrome_options = uc.options.ChromeOptions()
            chrome_options.add_argument(f'--window-position={offset[0]},{offset[1]}')
            chrome_options.add_argument(f'--window-size={window_width},{window_height}')
            driver = uc.Chrome(options=chrome_options)
            
            # Abrir o navegador e ajustar a posição e o tamanho
            driver.get('about:blank')  # Carregar uma página em branco para garantir que o navegador seja inicializado
            driver.set_window_size(window_width, window_height)
            driver.set_window_position(offset[0], offset[1])

            drivers.append(driver)

            # Criar e iniciar a thread para automação
            def automation_thread(driver, offset):
                # Abertura do site e ajuste
                driver.get('https://chat.openai.com')
                print(f"Abrindo o site na posição {offset}")
                time.sleep(5)

                # Verificar continuamente a presença do elemento chatgpt
                while True:
                    try:
                        element = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="radix-:r8:"]'))
                        )
                        if element:
                            print("Elemento chatgpt encontrado")
                            break
                    except Exception as e:
                        print("Aguardando o elemento 'ChatGPT' antes de continuar...")
                        time.sleep(2)

                # Verificar continuamente a presença do elemento textarea
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

                # Clicar no campo de input
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
                threading.Thread(target=continuously_check_elements, args=(driver, lock), daemon=True).start()
                threading.Thread(target=continuously_check_errors, args=(driver, responses_file, tittle_file, name, lock), daemon=True).start()
                print("Chamando send_prompts()")
                send_prompts(driver, responses_file, tittle_file, output_file, name)
                driver.quit()

            # Iniciar a thread de automação
            thread = threading.Thread(target=automation_thread, args=(driver, offset))
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
    chatgpt_response('driver', 'user_id', 'responses.txt', 'output.txt', 'tittle.txt', name='Victor Mello')
