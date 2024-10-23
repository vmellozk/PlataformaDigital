import tempfile
import shutil
import threading
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from configuracoes_driver import ConfiguracoesDriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login_gamma import login_gamma
from criar_gamma import criar_gamma
import os

# Instanciando as configurações
configuracoes = ConfiguracoesDriver()

# Lock para sincronizar o acesso ao perfil fixo
profile_copy_lock = threading.Lock()

# Função de automação para cada usuário
def gamma_automation(driver, user_id):
    # Define a pasta de downloads específica para cada usuário
    user_folder_downloads = os.path.join("users", str(user_id), "downloads")
    os.makedirs(user_folder_downloads, exist_ok=True)  # Cria a pasta se não existir

    # Define o local do perfil fixo onde a sessão está salva e Cria um diretório temporário para o perfil da sessão de cada thread
    user_profile_path = r"C:\Users\Victor\AppData\Local\Google\Chrome for Testing\User Data\Default"
    profile_dir = tempfile.mkdtemp()

    # Sincroniza a cópia do perfil para evitar concorrência entre threads
    with profile_copy_lock:
        print(f"Copiando perfil fixo para o diretório temporário para o usuário {user_id}")
        shutil.copytree(user_profile_path, profile_dir, dirs_exist_ok=True)

    # Define as opções, parâmetros e adiciona o perfil temporário de usuário e Configura o Chrome para salvar os downloads automaticamente na pasta do usuário
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={profile_dir}")  # Reutiliza a sessão anterior copiada
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": user_folder_downloads,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # Inicia o Driver com o perfil temporário criado
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # **Comando CDP para reforçar comportamento de download**
        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": user_folder_downloads
        })

        # Adicionando a lógica de posição e tamanho da janela
        time.sleep(configuracoes.STARTUP_DELAY)
        with configuracoes.position_lock:
            free_position = configuracoes.find_free_position()
            if free_position is not None:
                configuracoes.set_window_position_and_size(driver, free_position)
            else:
                driver.quit()
                return

        # Abre o site do Kiwify
        driver.get('https://gamma.app')
        print(f"Abrindo o site Kiwify para o usuário {user_id}")

        # Condição que vai verificar se precisa fazer o login
        if WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/div')
        ):
            login_gamma(driver)

        else:
            criar_gamma(driver, user_id)

    finally:
        if driver.session_id:
            driver.close()
        # Após fechar o driver, remove o diretório temporário criado
        shutil.rmtree(profile_dir, ignore_errors=True)
        configuracoes.release_position(free_position)
        print(f"Automação do Kiwify concluída para o usuário {user_id}.")
