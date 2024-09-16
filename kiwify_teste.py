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
from inserir_codigo_kiwify import inserir_codigo_kw

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
        # Abre um navegador com a url passada do kiwify
        driver.get('https://dashboard.kiwify.com.br/')
        time.sleep(5)
        print(f"Abrindo o site")

        # Verifica se a url é a passada é igual a atual. Se for, chama a função e começa o processo de login no kiwify e depois abra uma nova aba com a outra url passada. Se não for, ignora tudo e passa direto.
        kiwify_login = "https://dashboard.kiwify.com.br/login?redirect=%2F"
        time.sleep(2)
        current_url_1 = driver.current_url
        print(f"URL atual: {current_url_1}")
        if current_url_1 == kiwify_login:
            login_kw(driver)
            print("Fazendo o login na kiwify")
            time.sleep(3)
            driver.execute_script("window.open('');")
            print("Abrindo uma nova aba")
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1])
            driver.get("https://mail.google.com/")
            print("Segunda aba aberta: Gmail")
            time.sleep(3)
        else:
            print("Não foi preciso fazer o login no kiwify")
            pass

        # Verifica se a url passada é igual a atual. Se for, chama a função e faz o login na sessão que foi desconectada. Se não, passa direto. 
        gmail_entrar = 'https://www.google.com/intl/pt-BR/gmail/about/'
        time.sleep(2)
        current_url_2 = driver.current_url
        print(f"URL atual: {current_url_2}")  
        if gmail_entrar in current_url_2:
            entrar_gm(driver)
            print("Entrando no gmail")
            time.sleep(3)
        else:
            print("Não foi preciso entrar na sessão desconecta do gmail para adquirir o código do kiwify")
            pass

        # Verifica se a url passada é igual a atual. Se for, chama a função e faz o login. Se não, passa direto.
        gmail_login = 'https://accounts.google.com/'
        time.sleep(2)
        current_url_3 = driver.current_url
        print(f"URL atual: {current_url_3}")
        if gmail_login in current_url_3:
            login_gm(driver)
            print("Fazendo o login no gmail")
            time.sleep(3)
        else:
            print("Não foi preciso fazer o login no gmail para adquirir o código do kiwify")
            pass

        # Verifica se a url passada é igual a atual. Se for, chama a função para pegar o código que foi enviado para o login. Se não passa direto.
        gmail = 'https://mail.google.com/'
        time.sleep(2)
        current_url_4 = driver.current_url
        print(f"URL atual: {current_url_4}")
        if gmail in current_url_4:
            adq_codigo_kw(driver)
            time.sleep(3)
            print("fechando a aba atual e voltando para a primeira aba")
            driver.close()
        else:
            print("Não foi preciso adquirir o código de login do kiwify do gmail")
            pass

        # Verifica se a url passada é igual a atual. Se for, verifica se o campo de verificação está presente, depois verifica o campo para inserir o código, clica e insere o código adquirido na função "adq_codigo_kw()"
        kiwify_verificacao = "https://dashboard.kiwify.com.br/verify-otp?redirect=%2F"
        time.sleep(2)
        current_url_5 = driver.current_url
        print(f"URL atual: {current_url_5}")
        if current_url_5 == kiwify_verificacao:
            inserir_codigo_kw(driver)
            print("Inserindo o código no login kiwify")
            time.sleep(3)
        else:
            print("Não foi preciso fazer o login no kiwify")
            pass

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # Começa o processo de automação principal
        #time.sleep(500000)
        kiwify_url = 'https://dashboard.kiwify.com.br/'
        current_url_6 = driver.current_url
        print(f"URL atual: {current_url_6}")
        if kiwify_url in current_url_6: 
            print("Página inicial já logada.")

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
