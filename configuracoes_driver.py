import threading
import queue
from dotenv import load_dotenv
import os
import subprocess
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

class ConfiguracoesDriver:
    def __init__(self):
        # Carrega as variáveis de ambiente
        load_dotenv()
        self.EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
        self.EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
        self.SMTP_SERVER = os.getenv('SMTP_SERVER')
        self.SMTP_PORT = int(os.getenv('SMTP_PORT'))

        # Configurações
        self.MAX_TABS = 4
        self.TASK_QUEUE_DELAY = 3
        self.STARTUP_DELAY = 3
        self.task_queue = queue.Queue()
        self.tab_semaphore = threading.Semaphore(self.MAX_TABS)
        self.position_lock = threading.Lock()
        self.startup_lock = threading.Lock()

        # Posições da janela do navegador (grade 2x2)
        self.positions = [
            (0, 0),        # Canto superior esquerdo
            (960, 0),      # Canto superior direito
            (0, 540),      # Inferior esquerdo
            (960, 540)     # Inferior direito
        ]

        # Lista para rastrear quais posições estão ocupadas (False = livre, True = ocupada)
        self.occupied_positions = [False, False, False, False]

        # Tamanho da janela do navegador
        self.window_width = 960
        self.window_height = 540

    #
    def get_chrome_version(self):
        try:
            version = subprocess.check_output(
                r'"C:\Program Files\Google\Chrome\Application\chrome.exe" --version',  # Note as aspas
                stderr=subprocess.STDOUT,
                shell=True
            ).decode('utf-8')
            print(f"Versão do Chrome: {version.strip()}")
            return version.strip().split()[2]  # Retorna apenas a versão, que é o terceiro elemento
        except Exception as e:
            print(f"Erro ao obter a versão do Chrome: {e}")
            return None

    #
    def get_chromedriver_version(self):
        try:
            driver_path = ChromeDriverManager().install()  # Instala e obtém o caminho do ChromeDriver
            version = driver_path.split("\\")[-1]  # Extrai a versão do caminho
            print(f"Versão do ChromeDriver: {version}")
            return version
        except Exception as e:
            print(f"Erro ao obter a versão do ChromeDriver: {e}")
            return None

    #
    def compare_versions(self, chrome_version, chromedriver_version):
        if chrome_version and chromedriver_version:
            if chrome_version.startswith(chromedriver_version):
                print("As versões do Chrome e do ChromeDriver estão compatíveis.")
            else:
                print("As versões do Chrome e do ChromeDriver não estão compatíveis.")
                self.update_chrome()  # Atualiza o Chrome se houver incompatibilidade
        else:
            print("Não foi possível comparar as versões.")

    #
    def update_chrome(self):
        print("Atualizando o Google Chrome...")
        try:
            subprocess.run(["winget", "install", "--id=Google.Chrome"], check=True)
            print("Google Chrome atualizado com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao atualizar o Google Chrome: {e}")

    #
    def create_driver(self):
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        service = Service(ChromeDriverManager().install())
        return uc.Chrome(service=service, options=chrome_options)

    #
    def find_free_position(self):
        for index, occupied in enumerate(self.occupied_positions):
            if not occupied:
                return index
        return None
    
    #
    def set_window_position_and_size(self, driver, position_index):
        x, y = self.positions[position_index]
        driver.set_window_size(self.window_width, self.window_height)
        driver.set_window_position(x, y)
        self.occupied_positions[position_index] = True

    #
    def release_position(self, position_index):
        self.occupied_positions[position_index] = False
