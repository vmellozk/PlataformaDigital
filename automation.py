import time
import threading
import queue  # Adicionado para usar as filas
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from handling_error import click_element_if_found, handle_error
from send_prompt import send_prompts
import os

# Lista para armazenar drivers ativos
current_tabs = []

# Filas para gerenciar a entrada e saída de abas
task_queue = queue.Queue()  # Para gerenciar tarefas pendentes
tab_queue = queue.Queue()   # Para gerenciar abas disponíveis

# Lock para sincronização de acesso a recursos compartilhados
lock = threading.Lock()

# Função para encerrar processos do Chrome
def kill_chrome_processes():
    try:
        os.system("taskkill /im chrome.exe /f")
        os.system("taskkill /im chromedriver.exe /f")
    except Exception as e:
        print(f"Erro ao encerrar os processos do Chrome: {e}")

# Função para verificar continuamente elementos no driver
def continuously_check_elements(driver):
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
def continuously_check_errors(driver, responses_file, tittle_file, name):
    while True:
        try:
            with lock:
                handle_error(driver, responses_file, tittle_file, name)
            time.sleep(10)
        except Exception as e:
            pass
        time.sleep(2)
    
# Função de automação para cada usuário
def chatgpt_response(driver, user_id, responses_file, output_file, tittle_file, formatted_name, name):
    global current_tabs

    with lock:
        # Verifique se já há 4 abas abertas
        if len(current_tabs) >= 4:
            print(f"Fila cheia. Adicionando {user_id} na fila de espera.")
            task_queue.put(user_id)  # Adiciona o user_id à fila de tarefas
            return

        # Adicione o driver atual à lista de abas
        current_tabs.append(driver)
        print(f"Abrindo aba para o user_id: {user_id}")

    # Configurar o navegador com tamanho inicial pequeno
    chrome_options = uc.options.ChromeOptions()
    chrome_options.add_argument('--window-size=960,540')

    # Definir a posição da aba com base no número de abas ativas
    offsets = [(0, 0), (960, 0), (0, 540), (960, 540)]

    # Posicionar a aba
    position = offsets[len(current_tabs) - 1]
    chrome_options.add_argument(f'--window-position={position[0]},{position[1]}')

    try:
        # Inicializar o driver
        driver = uc.Chrome(options=chrome_options)
        driver.set_window_size(960, 540)
        driver.set_window_position(position[0], position[1])

        # Criar e iniciar a thread para automação
        def automation_thread(driver, position):
            # Abertura do site e ajuste
            driver.get('https://chat.openai.com')
            print(f"Abrindo o site na posição {position}")
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
            threading.Thread(target=continuously_check_elements, args=(driver,), daemon=True).start()
            threading.Thread(target=continuously_check_errors, args=(driver, responses_file, tittle_file, name), daemon=True).start()
            
            print("Chamando send_prompts()")
            send_prompts(driver, responses_file, tittle_file, output_file, name)
            driver.quit()

        # Iniciar a thread de automação
        thread = threading.Thread(target=automation_thread, args=(driver, position))
        thread.start()
        thread.join()

    finally:
        with lock:
            # Remova o driver da lista quando a automação estiver concluída
            current_tabs.remove(driver)
            driver.quit()

            # Notificar o sistema para processar o próximo item na fila
            if not task_queue.empty():
                next_user_id = task_queue.get()
                tab_queue.put(next_user_id)

        # Função fictícia para garantir que todos os processos do Chrome sejam encerrados
        kill_chrome_processes()

if __name__ == "__main__":
    chatgpt_response('driver', 'user_id', 'responses.txt', 'output.txt', 'tittle.txt', 'formatted_name', name='Victor Mello')
