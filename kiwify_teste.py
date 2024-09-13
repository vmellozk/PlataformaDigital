#Bibliotecas
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import threading
import queue
from dotenv import load_dotenv
import os
from login_kiwify import login_kw
from login_gmail import login_gm
from adquirir_codigo_kiwify import adq_codigo_kw
from entrar_gmail import entrar_gm
from criar_produto_kiwify import criar_produto_kw
from editar_principal import edit
from anexar_produto import anexar_produto
from afiliado import copiar_link_afiliado

# Configurações
MAX_TABS = 4
TASK_QUEUE_DELAY = 3  # Tempo em segundos para aguardar antes de processar a próxima aba
STARTUP_DELAY = 3    # Tempo em segundos para aguardar antes de iniciar o processamento de qualquer aba
task_queue = queue.Queue()
tab_semaphore = threading.Semaphore(MAX_TABS)
position_lock = threading.Lock()
startup_lock = threading.Lock()  # Lock para controlar o atraso global

# Posições da janela do navegador (grade 2x2)
positions = [
    (0, 0),        # Canto superior esquerdo
    (960, 0),      # Canto superior direito
    (0, 540),      # Inferior esquerdo
    (960, 540)     # Inferior direito
]

# Lista para rastrear quais posições estão ocupadas (False = livre, True = ocupada)
occupied_positions = [False, False, False, False]

# Tamanho da janela do navegador
window_width = 960
window_height = 540

#
load_dotenv()
KW_EMAIL_ADDRESS=os.getenv('KW_EMAIL_ADDRESS')
KW_EMAIL_PASSWORD=os.getenv('KW_EMAIL_PASSWORD')
GM_EMAIL_ADDRESS=os.getenv('GM_EMAIL_ADDRESS')
GM_EMAIL_PASSWORD=os.getenv('GM_EMAIL_PASSWORD')

# Função para encontrar a primeira posição livre
def find_free_position():
    for index, occupied in enumerate(occupied_positions):
        if not occupied:
            return index
    return None  # Se todas as posições estiverem ocupadas

# Função que ajusta a posição e o tamanho da janela
def set_window_position_and_size(driver, position_index):
    x, y = positions[position_index]
    driver.set_window_size(window_width, window_height)
    driver.set_window_position(x, y)
    # Marcar a posição como ocupada
    occupied_positions[position_index] = True

# Função para liberar a posição quando a aba é fechada
def release_position(position_index):
    occupied_positions[position_index] = False

# Função para liberar vaga e chamar o próximo item da fila
def release_tab_and_process_queue():
    # Libera uma vaga no semáforo
    tab_semaphore.release()
    
    if not task_queue.empty():
        next_user_id = task_queue.get()
        print(f"Chamando a fila para processar o usuário {next_user_id}")
        # Inicia um novo thread para processar o próximo usuário
        threading.Thread(target=kiwify_automation, args=(next_user_id,)).start()

# Função de automação para cada usuário
def kiwify_automation(driver):
    #
    #user_profile_path = r"C:\Users\Victor\AppData\Local\Google\Chrome for Testing\User Data\Default"

    # Deifine as opções, parâmetros e adiciona o perfil de usuário
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument(f"user-data-dir={user_profile_path}")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    #
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Use um lock para garantir que apenas uma aba seja aberta e posicionada por vez
    with position_lock:
        # Encontre a primeira posição livre
        free_position = find_free_position()
        
        if free_position is not None:
            # Define a posição e o tamanho da aba
            set_window_position_and_size(driver, free_position)
        else:
            # Caso não haja posição livre, fecha o driver
            driver.quit()
            return

    try:
        #
        driver.get('https://dashboard.kiwify.com.br/')
        time.sleep(5)
        print(f"Abrindo o site")

        #
        kiwify_login = "https://dashboard.kiwify.com.br/login?redirect=%2F"
        time.sleep(2)
        current_url_1 = driver.current_url
        print(f"URL atual: {current_url_1}")
        if current_url_1 == kiwify_login:
            login_kw(driver)
            time.sleep(3)
            driver.execute_script("window.open('');")
            print("Nova aba aberta")
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1])
            driver.get("https://mail.google.com/")
            print("Segunda aba aberta: Gmail")
            time.sleep(3)
        else:
            print("não abriu o login kiwify")
            pass

        #
        gmail_entrar = 'https://www.google.com/intl/pt-BR/gmail/about/'
        time.sleep(2)
        current_url_2 = driver.current_url
        print(f"URL atual: {current_url_2}")  
        if gmail_entrar in current_url_2:
            entrar_gm(driver)
        else:
            print("não abriu o google/about")
            pass

        #
        gmail_login = 'https://accounts.google.com/'
        time.sleep(2)
        current_url_3 = driver.current_url
        print(f"URL atual: {current_url_3}")
        if gmail_login in current_url_3:
            login_gm(driver)
            time.sleep(3)
        else:
            print("não abriu o login gmail")
            pass

        #
        gmail = 'https://mail.google.com/'
        time.sleep(2)
        current_url_4 = driver.current_url
        print(f"URL atual: {current_url_4}")
        if gmail in current_url_4:
            adq_codigo_kw(driver)
            time.sleep(3)
            print("fechando a aba atual")
            driver.close()
            print("Voltando para a primeira aba")
        else:
            print("não abriu o gmail")
            pass

        #
        kiwify_verificacao = "https://dashboard.kiwify.com.br/verify-otp?redirect=%2F"
        time.sleep(2)
        current_url_5 = driver.current_url
        print(f"URL atual: {current_url_5}")
        if current_url_5 == kiwify_verificacao:
            # Procura onde está o campo para inserir o código e clica
            while True:
                try:
                    campo_inserir_codigo = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div/main/div[2]/div/div/div[2]/div[1]/input'))
                    )
                    if campo_inserir_codigo:
                        time.sleep(2)
                        campo_inserir_codigo.click()
                        print("Clicando em campo_inserir_codigo")
                        time.sleep(2)
                        #aqui adicionar um send_keys para ler o arquivo criado com o codigo capturado no email e inserir no campo
                        time.sleep(2)
                        break
                except Exception as e:
                    print("Aguardando o botão de 'campo_inserir_codigo' antes de clicar...")
                    time.sleep(2)

            # Procura onde está o botão de verificar e clica
            while True:
                try:
                    verificar = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div/main/div[2]/div/div/div[2]/div[2]/button'))
                    )
                    if verificar:
                        time.sleep(2)
                        verificar.click()
                        print("Clicando em verificar")
                        time.sleep(5)
                        break
                except Exception as e:
                    print("Aguardando o botão de 'verificar' antes de clicar...")
                    time.sleep(2)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # Começa o processo de automação principal
        #time.sleep(500000)
        kiwify_url = 'https://dashboard.kiwify.com.br/'
        current_url_6 = driver.current_url
        print(f"URL atual: {current_url_6}")
        if kiwify_url in current_url_6: 
            print("Página inicial detectada ou já logado.")

            criar_produto_kw(driver)
            time.sleep(1)
            edit(driver)
            time.sleep(1)
            anexar_produto(driver)
            time.sleep(1)
            copiar_link_afiliado(driver)

            '''
            aqui jogar a lógica para enviar o email via smtp lendo o arquivo da url de afiliado para enviar ao cliente
            '''

    #
    finally:
        driver.close()
        time.sleep(1)
        # Libera a vaga e chama o próximo item da fila com um atraso
        release_position(free_position)
        time.sleep(TASK_QUEUE_DELAY)  # Aguarda um tempo antes de processar o próximo
        release_tab_and_process_queue()

#
if __name__ == "__main__":
    kiwify_automation('driver')

'''
user_id, responses_file, output_file, tittle_file, formatted_name, name
'''
