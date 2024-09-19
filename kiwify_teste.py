#Bibliotecas
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import threading
from login_kiwify import login_kw
from login_gmail import login_gm
from adquirir_codigo_kiwify import adq_codigo_kw
from criar_produto_kiwify import criar_produto_kw
from editar_principal import edit
from anexar_produto import anexar_produto
from afiliado import copiar_link_afiliado
from inserir_codigo_kiwify import inserir_codigo_kw
from configuracoes_driver import ConfiguracoesDriver

# Instanciando as configurações
configuracoes = ConfiguracoesDriver()

# Função para liberar vaga e chamar o próximo item da fila
def release_tab_and_process_queue():
    # Libera uma vaga no semáforo
    configuracoes.tab_semaphore.release()
    
    if not configuracoes.task_queue.empty():
        next_user_id = configuracoes.task_queue.get()
        print(f"Chamando a fila para processar o usuário {next_user_id}")
        # Inicia um novo thread para processar o próximo usuário
        threading.Thread(target=kiwify_automation, args=(next_user_id,)).start()

# Função de automação para cada usuário
def kiwify_automation(driver):
    #
    user_profile_path = r"C:\Users\Victor\AppData\Local\Google\Chrome for Testing\User Data\Default"

    # Define as opções, parâmetros e adiciona o perfil de usuário
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={user_profile_path}")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    #
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Use um lock para garantir que apenas uma aba seja aberta e posicionada por vez
    with configuracoes.position_lock:
        # Encontre a primeira posição livre
        free_position = configuracoes.find_free_position()
        
        if free_position is not None:
            # Define a posição e o tamanho da aba
            configuracoes.set_window_position_and_size(driver, free_position)
        else:
            # Caso não haja posição livre, fecha o driver
            driver.quit()
            return

    try:
        # Diminui o zoom da página para 90%
        driver.execute_script("document.body.style.zoom='90%'")
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
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
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

            criar_produto_kw(driver, user_id=1)
            time.sleep(1)
            edit(driver, user_id=1)
            time.sleep(1)
            anexar_produto(driver, user_id=1)
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
        configuracoes.release_position(free_position)
        time.sleep(configuracoes.TASK_QUEUE_DELAY)  # Aguarda um tempo antes de processar o próximo
        release_tab_and_process_queue()

#
if __name__ == "__main__":
    kiwify_automation('driver')

'''
user_id, responses_file, output_file, tittle_file, formatted_name, name
'''
