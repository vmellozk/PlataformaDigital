import tempfile
import shutil
import threading
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from login_kiwify import login_kw
from login_gmail import login_gm
from adquirir_codigo_kiwify import adq_codigo_kw
from criar_produto_kiwify import criar_produto_kw
from editar_principal import edit
from anexar_produto import anexar_produto
from afiliado import copiar_link_afiliado
from inserir_codigo_kiwify import inserir_codigo_kw
from configuracoes_driver import ConfiguracoesDriver
from send_email import send_email
import time

# Instanciando as configurações
configuracoes = ConfiguracoesDriver()

# Lock para sincronizar o acesso ao perfil fixo
profile_copy_lock = threading.Lock()

# Função de automação para cada usuário
def kiwify_automation(driver, user_id):
    # Define o local do perfil fixo onde a sessão está salva
    user_profile_path = r"C:\Users\Victor\AppData\Local\Google\Chrome for Testing\User Data\Default"
    # Cria um diretório temporário para o perfil da sessão de cada thread
    profile_dir = tempfile.mkdtemp()
    # Sincroniza a cópia do perfil para evitar concorrência entre threads
    with profile_copy_lock:
        print(f"Copiando perfil fixo para o diretório temporário para o usuário {user_id}")
        shutil.copytree(user_profile_path, profile_dir, dirs_exist_ok=True)

    # Define as opções, parâmetros e adiciona o perfil temporário de usuário
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={profile_dir}")  # Reutiliza a sessão anterior copiada
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Inicia o Driver com o perfil temporário criado
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Adicionando a lógica de posição e tamanho da janela
        time.sleep(configuracoes.STARTUP_DELAY)
        with configuracoes.position_lock:
            free_position = configuracoes.find_free_position()
            if free_position is not None:
                configuracoes.set_window_position_and_size(driver, free_position)
            else:
                driver.quit()
                return

        # Diminui o zoom da página para 90%
        driver.execute_script("document.body.style.zoom='90%'")
        # Abre o site do Kiwify
        driver.get('https://dashboard.kiwify.com.br/')
        print(f"Abrindo o site Kiwify para o usuário {user_id}")

        # Verifica se a url é a passada é igual a atual. Se for, chama a função e começa o processo de login no kiwify e depois abra uma nova aba com a outra url passada. Se não for, ignora tudo e passa direto.
        kiwify_login = "https://dashboard.kiwify.com.br/login?redirect=%2F"
        current_url_1 = driver.current_url
        print(f"URL atual: {current_url_1}")
        if current_url_1 == kiwify_login:
            time.sleep(1)
            login_kw(driver)
            print(f"Fazendo o login na Kiwify para o usuário {user_id}")
            driver.execute_script("window.open('');")
            print("Abrindo uma nova aba para o Gmail")
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1])
            driver.get("https://mail.google.com/")
        else:
            print("Já logado no Kiwify")
            pass

        # Verifica se a url passada é igual a atual. Se for, chama a função e faz o login. Se não, passa direto.
        gmail_login = 'https://accounts.google.com/'
        current_url_3 = driver.current_url
        print(f"URL atual: {current_url_3}")
        if gmail_login in current_url_3:
            time.sleep(1)
            login_gm(driver)
            print("Fazendo o login no gmail")
        else:
            print("Não foi preciso fazer o login no gmail para adquirir o código do kiwify")
            pass

        # Verifica se a url passada é igual a atual. Se for, chama a função para pegar o código que foi enviado para o login. Se não passa direto.
        gmail = 'https://mail.google.com/'
        current_url_4 = driver.current_url
        print(f"URL atual: {current_url_4}")
        if gmail in current_url_4:
            time.sleep(1)
            adq_codigo_kw(driver)
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
        current_url_5 = driver.current_url
        print(f"URL atual: {current_url_5}")
        if current_url_5 == kiwify_verificacao:
            time.sleep(1)
            inserir_codigo_kw(driver)
            print("Inserindo o código no login kiwify")
        else:
            print("Não foi preciso fazer o login no kiwify")
            pass

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # Começa o processo de automação principal
        kiwify_url = 'https://dashboard.kiwify.com.br/'
        current_url_6 = driver.current_url
        print(f"URL atual: {current_url_6}")
        if kiwify_url in current_url_6:
            time.sleep(1)
            print("Página inicial já logada.")

            criar_produto_kw(driver, user_id)
            time.sleep(1)
            edit(driver, user_id)
            time.sleep(1)
            anexar_produto(driver, user_id)
            time.sleep(1)
            copiar_link_afiliado(driver, user_id)
            time.sleep(1)

    finally:
        if driver.session_id:
            driver.close()
        # Após fechar o driver, remove o diretório temporário criado
        shutil.rmtree(profile_dir, ignore_errors=True)
        configuracoes.release_position(free_position)
        print(f"Automação do Kiwify concluída para o usuário {user_id}.")

'''
user_id, responses_file, output_file, tittle_file, formatted_name, name
'''
