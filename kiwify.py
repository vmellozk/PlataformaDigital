#
import psutil
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from selenium import webdriver
import threading
import queue

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
    user_profile_path = r"C:\Users\Victor\AppData\Local\Google\Chrome for Testing\User Data\Default"

    # Deifine as opções, parâmetros e adiciona o perfil de usuário
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={user_profile_path}")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")

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
        driver.get('https://dashboard.kiwify.com.br/')
        time.sleep(5)
        print(f"Abrindo o site")

        current_url = driver.current_url
        print(f"URL atual: {current_url}")

        site_login = "https://dashboard.kiwify.com.br/login?redirect=%2F"
        if current_url == site_login:
            while True:
                try:
                    email = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/main/div[1]/div/div[2]/form/div[1]/div[1]/input'))
                    )
                    if email:
                        time.sleep(2)
                        email.click()
                        print("Campo de email encontrado")
                        break
                except Exception as e:
                    print("Aguardando o campo de email antes de continuar...")
                    time.sleep(2)

            while True:
                try:
                    password = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/main/div[1]/div/div[2]/form/div[2]/div/input'))
                    )
                    if password:
                        time.sleep(2)
                        password.click()
                        print("Campo de senha encontrado")
                        break
                except Exception as e:
                    print("Aguardando o campo de senha antes de continuar...")
                    time.sleep(2)

            while True:
                try:
                    login = driver.find_element(By.XPATH, '//*[@id="__layout"]/main/div[1]/div/div[2]/form/div[4]/span/button')
                    if login:
                        time.sleep(2)
                        login.click()
                        print("Clicando em logar")
                        break
                except Exception as e:
                    print("Aguardando o botão de 'logar' antes de clicar...")
                    time.sleep(2)

            '''
            aqui depois de clicar em logar tem que: abrir o email, pesquisar por kiwify, pegar o último email referente ao horário/dia atual, entrar nele, copiar o código, voltar para a aba de login, colar o código e clicar no botão. para só assim, depois, continuar a inserir o produto para o cliente.
            '''

        else:
            time.sleep(5)
            print("Página inicial detectada ou já logado.")
            
            #
            while True:
                try:
                    produtos = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[2]/div/div/div[2]/nav/div[1]/a[2]'))
                    )
                    if produtos:
                        time.sleep(2)
                        produtos.click()
                        print("Botão de produtos encontrado")
                        break
                except Exception as e:
                    print("Aguardando o botão de 'produtos' antes de continuar...")
                    time.sleep(2)

            #
            while True:
                try:
                    criar_produto = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[6]/span/div'))
                    )
                    if criar_produto:
                        time.sleep(2)
                        criar_produto.click()
                        print("Botão de criar produto encontrado")
                        break
                except Exception as e:
                    print("Aguardando botão de 'criar produto' antes de continuar...")
                    time.sleep(2)

            #
            while True:
                try:
                    continuar = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[2]/button')
                    if continuar:
                        time.sleep(2)
                        continuar.click()
                        print("Clicando em continuar")
                        break
                except Exception as e:
                    print("Aguardando o botão de 'continuar' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    nome_produto = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[1]/div[2]/div/input')
                    if nome_produto:
                        time.sleep(2)
                        nome_produto.click()
                        print("Clicando em nome do produto")
                        break
                except Exception as e:
                    print("Aguardando o campo de 'nome do produto' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    descricao = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[1]/div[3]/div/textarea')
                    if descricao:
                        time.sleep(2)
                        descricao.click()
                        print("Clicando em descrição")
                        break
                except Exception as e:
                    print("Aguardando o campo de 'descrição' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    pagina_vendas = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[1]/div[4]/div[2]/input')
                    if pagina_vendas:
                        time.sleep(2)
                        pagina_vendas.click()
                        print("Clicando em pagina de vendas")
                        break
                except Exception as e:
                    print("Aguardando o campo de 'página de vendas' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    preco = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[1]/div[5]/fieldset/div/input')
                    if preco:
                        time.sleep(2)
                        preco.click()
                        print("Clicando em preço")
                        break
                except Exception as e:
                    print("Aguardando o campo de 'preço' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    criar_produto_final = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[2]/button')
                    if criar_produto_final:
                        time.sleep(2)
                        criar_produto_final.click()
                        print("CLicando em criar produto final")
                        break
                except Exception as e:
                    print("Aguardando o botão 'criar produto final' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    categoria = driver.find_element(By.XPATH, '//*[@id="general"]/div[1]/div/div[2]/div/div/div[3]/div/select')
                    if categoria:
                        time.sleep(2)
                        categoria.click()
                        print("CLicando em categoria")

                        '''
                        criar uma lógica para selecionar a categoria. pode ser perguntando ao chatgpt, salvando em um arquivo de texto, lendo o texto, procurando na div onde tem aquilo e clicar
                        '''

                        break
                except Exception as e:
                    print("Aguardando o campo 'categoria' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    imagem_produto = driver.find_element(By.XPATH, '//*[@id="general"]/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div/button/div/div/span')
                    if imagem_produto:
                        time.sleep(2)
                        imagem_produto.click()
                        print("CLicando em imagem produto")
                        break
                except Exception as e:
                    print("Aguardando o botão 'imagem produto' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    email_suporte = driver.find_element(By.XPATH, '//*[@id="general"]/div[3]/div/div[2]/div/div/div/div[2]/div/div/input')
                    if email_suporte:
                        time.sleep(2)
                        email_suporte.click()
                        print("CLicando em email suporte")
                        break
                except Exception as e:
                    print("Aguardando o campo 'email suporte' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    nome_produtor = driver.find_element(By.XPATH, '//*[@id="general"]/div[3]/div/div[2]/div/div/div/div[3]/div/div/input')
                    if nome_produtor:
                        time.sleep(2)
                        nome_produtor.click()
                        print("CLicando em nome produtor")
                        break
                except Exception as e:
                    print("Aguardando o campo 'nome produtor' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    salvar = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[17]/div[2]/button')
                    if salvar:
                        time.sleep(2)
                        salvar.click()
                        print("CLicando em salvar")
                        break
                except Exception as e:
                    print("Aguardando o botão 'salvar' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    afiliados = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[12]/div/div[1]/nav/div[6]/a')
                    if afiliados:
                        time.sleep(2)
                        afiliados.click()
                        print("CLicando em afiliados")
                        break
                except Exception as e:
                    print("Aguardando o botão 'afiliados' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    habilitar_afiliados = driver.find_element(By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[1]/span/span')
                    if habilitar_afiliados:
                        time.sleep(2)
                        habilitar_afiliados.click()
                        print("CLicando em habilitar afiliados")
                        break
                except Exception as e:
                    print("Aguardando o botão 'habilitar afiliados' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    habilitar_market_place = driver.find_element(By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[3]/div/span')
                    if habilitar_market_place:
                        time.sleep(2)
                        habilitar_market_place.click()
                        print("CLicando em habilitar_market_place")

                        '''
                        criar uma lógica para selecionar a categoria. pode ser perguntando ao chatgpt, salvando em um arquivo de texto, lendo o texto, procurando na div onde tem aquilo e clicar
                        '''

                        break
                except Exception as e:
                    print("Aguardando o botão 'habilitar_market_place' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    email_suporte_afiliados = driver.find_element(By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[5]/div/div/div/input')
                    if email_suporte_afiliados:
                        time.sleep(2)
                        email_suporte_afiliados.click()
                        print("CLicando em email_suporte_afiliados")
                        break
                except Exception as e:
                    print("Aguardando o campo 'email_suporte_afiliados' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    descricao_afiliados = driver.find_element(By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[6]/div[1]/textarea')
                    if descricao_afiliados:
                        time.sleep(2)
                        descricao_afiliados.click()
                        print("CLicando em descricao_afiliados")
                        break
                except Exception as e:
                    print("Aguardando o campo 'descricao_afiliados' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    salvar_config_afiliados = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[18]/div[2]/button')
                    if salvar_config_afiliados:
                        time.sleep(2)
                        salvar_config_afiliados.click()
                        print("CLicando em salvar_config_afiliados")
                        break
                except Exception as e:
                    print("Aguardando o  'salvar_config_afiliados' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    teste = driver.find_element(By.XPATH, '')
                    if teste:
                        time.sleep(2)
                        teste.click()
                        print("CLicando em teste")
                        break
                except Exception as e:
                    print("Aguardando o  'teste' antes de clicar...")
                    time.sleep(2)

            #
            while True:
                try:
                    link_afiliado = driver.find_element(By.XPATH, '//*[@id="affiliates"]/div[3]/div/div[2]/div/div/div/div[2]/span/button')
                    if link_afiliado:
                        time.sleep(2)
                        link_afiliado.click()
                        print("CLicando em link_afiliado")

                        '''
                        usar o pyperclip para salvar o link em um arquivo para enviar no email do cliente
                        '''

                        break
                except Exception as e:
                    print("Aguardando o botão 'link_afiliado' antes de clicar...")
                    time.sleep(2)

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
