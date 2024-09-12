#Bibliotecas
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

    #Bloco try except para tentar executar o código dentro
    try:
        driver.get('https://dashboard.kiwify.com.br/')
        time.sleep(5)
        print(f"Abrindo o site")

        #Detecta a url atual e comparada a com url passada, se for igual, ele vai fazer o login, abrindo o email para pegar o código, voltar para a aba e colar o código para logar
        current_url = driver.current_url
        print(f"URL atual: {current_url}")
        site_login = "https://dashboard.kiwify.com.br/login?redirect=%2F"
        if current_url == site_login:
            #Clica no campo de email e insere o email
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

            #Clica no campo de senha e insere a senha
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

            #Clica no botão de login
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

            #Abre uma nova aba para abrir o gmail para pegar o código e voltar para colar o código na kiwify e logar no site
            driver.execute_script("window.open('');")
            print("Nova aba aberta")
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1])
            driver.get("https://mail.google.com/")
            print("Segunda aba aberta: Gmail")
            time.sleep(3)

            #Detecta a url atual e verifica com a url passada, se for igual, ele vai logar, fornecendo a senha se for preciso e entrando no email
            current_url = driver.current_url
            print(f"URL atual: {current_url}")
            gmail_login = 'https://accounts.google.com/'
            if current_url == gmail_login:
                #Procura onde está o campo de email, clica e insere o email
                while True:
                    try:
                        email = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
                        if email:
                            time.sleep(2)
                            email.click()
                            print("Clicando em email")
                            break
                    except Exception as e:
                        print("Aguardando o campo de 'email' antes de clicar...")
                        time.sleep(2)

                #Procura onde está o botão de próximo e clica
                while True:
                    try:
                        email_proximo = driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button')
                        if email_proximo:
                            time.sleep(2)
                            email_proximo.click()
                            print("Clicando em email_proximo")
                            break
                    except Exception as e:
                        print("Aguardando o botão de 'email_proximo' antes de clicar...")
                        time.sleep(2)
                
                # Procura o campo de senha, clica e insere a senha
                while True:
                    try:
                        password = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
                        if password:
                            time.sleep(2)
                            password.click()
                            print("Clicando em password")
                            break
                    except Exception as e:
                        print("Aguardando o campo de 'password' antes de clicar...")
                        time.sleep(2)

                # Procura onde está o botão de próximo e clica
                while True:
                    try:
                        password_proximo = driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button')
                        if password_proximo:
                            time.sleep(2)
                            password_proximo.click()
                            print("Clicando em password_proximo")
                            break
                    except Exception as e:
                        print("Aguardando o botão de 'password_proximo' antes de clicar...")
                        time.sleep(2)
            else:
                pass

            # Detecta a url atual, verifica com a url passada, se for igual, vai clicar em fazer login, selecionar o email, se aparecer o campo de senha vai clicar em senha e clicar em logar para abrir o email
            current_url = driver.current_url
            print(f"URL atual: {current_url}")            
            gmail_entrar = 'https://www.google.com/intl/pt-BR/gmail/about/'
            if current_url == gmail_entrar:
                # Procura o botão de fazer login e clica
                while True:
                    try:
                        fazer_login_gmail = driver.find_element(By.XPATH, '/html/body/header/div/div/div/a[2]')
                        if fazer_login_gmail:
                            time.sleep(2)
                            fazer_login_gmail.click()
                            print("Clicando em fazer_login_gmail")
                            break
                    except Exception as e:
                        print("Aguardando o botão de 'fazer_login_gmail' antes de clicar...")
                        time.sleep(2)

                # Procura o campo do primeiro email e clica
                while True:
                    try:
                        email_clicar = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/form/span/section/div/div/div/div/ul/li[1]/div')
                        if email_clicar:
                            time.sleep(2)
                            email_clicar.click()
                            print("Clicando em email_clicar")
                            break
                    except Exception as e:
                        print("Aguardando o campo de 'email_clicar' antes de clicar...")
                        time.sleep(2)

                #Criar uma lógica para que se aparecer o campo de inserir a senha, é para inserir a lógica passada abaixo
                # Procura o campo de senha, clica e insere a senha
                while True:
                    try:
                        teste = driver.find_element(By.XPATH, '')
                        if teste:
                            time.sleep(2)
                            teste.click()
                            print("Clicando em teste")
                            break
                    except Exception as e:
                        print("Aguardando o botão de 'teste' antes de clicar...")
                        time.sleep(2)

                # Procura o botão de próximo e clica
                while True:
                    try:
                        teste = driver.find_element(By.XPATH, '')
                        if teste:
                            time.sleep(2)
                            teste.click()
                            print("Clicando em teste")
                            break
                    except Exception as e:
                        print("Aguardando o botão de 'teste' antes de clicar...")
                        time.sleep(2)
            else:
                pass

            # Alternar de volta para a primeira aba
            driver.switch_to.window(driver.window_handles[0])
            print("Voltando para a primeira aba")

        #
        else:
            #time.sleep(500000)
            print("Página inicial detectada ou já logado.")
            # Procura o botão de produtos e clica nele
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

            # Procura o botão de criar_produto e clica nele
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

            # Procura o botão de continuar e clica nele
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

            # Procura o campo de nome do produto, clica nele e insere o nome do produto mediante ao arquivo salvo e gerado pela IA na pasta de cada user_id específico
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

            # Procura o campo de descrição, clica nele e insere a descrição mediante ao arquivo salvo e gerado pela IA na pasta de cada user_id específico
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

            # Procura o campo de página de vendas, clica e insere a página de vendas
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

            # Procura o campo de preço, clica e insere o preço do produto
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

            # Procura o botão de criar o produto e clica nele
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

            # Procura o botão de categoria e clica nele
            while True:
                try:
                    categoria = driver.find_element(By.XPATH, '//*[@id="general"]/div[1]/div/div[2]/div/div/div[3]/div/select')
                    if categoria:
                        time.sleep(2)
                        categoria.click()
                        print("CLicando em categoria")
                        break
                except Exception as e:
                    print("Aguardando o campo 'categoria' antes de clicar...")
                    time.sleep(2)

            # aqui deve-se criar uma lógica para selecionar a categoria. pode ser perguntando ao chatgpt, salvando em um arquivo de texto, lendo o texto, procurando na div onde tem aquilo e clicar 
            while True:
                try:
                    teste = driver.find_element(By.XPATH, '')
                    if teste:
                        time.sleep(2)
                        teste.click()
                        print("Clicando em teste")
                        break
                except Exception as e:
                    print("Aguardando o botão de 'teste' antes de clicar...")
                    time.sleep(2)

            # Procura o botão de selecionar a imagem do produto e clica nele
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

            #criar uma logica para buscar a imagem do produto que vai ser gerada via IA para cada usuário na pasta do user_id específico
            while True:
                try:
                    teste = driver.find_element(By.XPATH, '')
                    if teste:
                        time.sleep(2)
                        teste.click()
                        print("Clicando em teste")
                        break
                except Exception as e:
                    print("Aguardando o botão de 'teste' antes de clicar...")
                    time.sleep(2)

            # Procura o campo de inserir o email de suporte, clica nele e insere o email de suporte
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

            # Procura o campo do nome do produtor, clica nele, lê o arquivo .txt salvo na pasta do usuário e insere aqui
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

            # Procura o botão de salvar e clica nele
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

            # Procura o botão de área de membros e clica nele
            while True:
                try:
                    area_membros = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[12]/div/div[1]/nav/div[2]/a')
                    if area_membros:
                        time.sleep(2)
                        area_membros.click()
                        print("CLicando em area_membros")
                        break
                except Exception as e:
                    print("Aguardando o botão 'area_membros' antes de clicar...")
                    time.sleep(2)

            # Procura o botão de adicionar e clica nele
            while True:
                try:
                    adicionar = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[7]/div[1]/div[1]/div[1]/div[2]/button')
                    if adicionar:
                        time.sleep(2)
                        adicionar.click()
                        print("CLicando em adicionar")
                        break
                except Exception as e:
                    print("Aguardando o botão 'adicionar' antes de clicar...")
                    time.sleep(2)

            # procura o campo do nome do módulo, clica nele e insere o nome do módulo
            while True:
                try:
                    nome_modulo = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/input')
                    if nome_modulo:
                        time.sleep(2)
                        nome_modulo.click()
                        print("CLicando em nome_modulo")
                        break
                except Exception as e:
                    print("Aguardando o campo 'nome_modulo' antes de clicar...")
                    time.sleep(2)

            # Procura o botão de adicionar o módulo e clica nele
            while True:
                try:
                    adicionar_modulo = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div/div[3]/button')
                    if adicionar_modulo:
                        time.sleep(2)
                        adicionar_modulo.click()
                        print("CLicando em adicionar_modulo")
                        break
                except Exception as e:
                    print("Aguardando o botão 'adicionar_modulo' antes de clicar...")
                    time.sleep(2)

            # Procura o símbolo de adicionar e clica nele
            while True:
                try:
                    simbolo_adicionar = driver.find_element(By.XPATH, '//*[@id="options-menu"]')
                    if simbolo_adicionar:
                        time.sleep(2)
                        simbolo_adicionar.click()
                        print("CLicando em simbolo_adicionar")
                        break
                except Exception as e:
                    print("Aguardando o botão 'simbolo_adicionar' antes de clicar...")
                    time.sleep(2)

            # Procura o campo de adicionar conteúdo e clica nele
            while True:
                try:
                    adicionar_conteudo = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[7]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/div[1]')
                    if adicionar_conteudo:
                        time.sleep(2)
                        adicionar_conteudo.click()
                        print("CLicando em adicionar_conteudo")
                        break
                except Exception as e:
                    print("Aguardando o botão 'adicionar_conteudo' antes de clicar...")
                    time.sleep(2)

            # Procura o campo do título, clica nele e insere o título
            while True:
                try:
                    titulo = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[7]/div[1]/div/div[4]/div[1]/div/div[2]/div/div/div[1]/div/input')
                    if titulo:
                        time.sleep(2)
                        titulo.click()
                        print("CLicando em titulo")
                        break
                except Exception as e:
                    print("Aguardando o botão 'titulo' antes de clicar...")
                    time.sleep(2)

            # Procura o botão de selecionar do computador, clica nele, e seleciona o ebook gerado na pasta específica de cada user_id
            while True:
                try:
                    selecione_computador = driver.find_element(By.XPATH, '//*[@id="attachment"]/div[1]/div/button/div/div/span')
                    if selecione_computador:
                        time.sleep(2)
                        selecione_computador.click()
                        print("CLicando em selecione_computador")
                        break
                except Exception as e:
                    print("Aguardando o botão 'selecione_computador' antes de clicar...")
                    time.sleep(2)

            # Procura o botão de criar e publicar e clica nele
            while True:
                try:
                    criar_publicar = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[7]/div[1]/div/div[5]/div[3]/div')
                    if criar_publicar:
                        time.sleep(2)
                        criar_publicar.click()
                        print("CLicando em criar_publicar")
                        break
                except Exception as e:
                    print("Aguardando o botão 'criar_publicar' antes de clicar...")
                    time.sleep(2)

            # Alternar de volta para a primeira aba
            driver.switch_to.window(driver.window_handles[0])
            print("Voltando para a primeira aba")

            # Procura o botão de salvar e clica nele
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

            # Procura o botão de afiliados e clica nele
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

            # Procura o botão de habilitar afiliados e clica nele
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

            # Procura o botão de habilitar o market place e clica nele
            while True:
                try:
                    habilitar_market_place = driver.find_element(By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[3]/div/span')
                    if habilitar_market_place:
                        time.sleep(2)
                        habilitar_market_place.click()
                        print("CLicando em habilitar_market_place")
                        break
                except Exception as e:
                    print("Aguardando o botão 'habilitar_market_place' antes de clicar...")
                    time.sleep(2)

            # Procura o botão de categoria e clica nele
            while True:
                try:
                    categoria_afiliados = driver.find_element(By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[4]/div/select')
                    if categoria_afiliados:
                        time.sleep(2)
                        categoria_afiliados.click()
                        print("CLicando em categoria_afiliados")
                        break
                except Exception as e:
                    print("Aguardando o botão 'categoria_afiliados' antes de clicar...")
                    time.sleep(2)
            
            # Criar uma lógica para selecionar a categoria. pode ser perguntando ao chatgpt, salvando em um arquivo de texto, lendo o texto, procurando na div onde tem aquilo e clicar
            while True:
                try:
                    teste = driver.find_element(By.XPATH, '')
                    if teste:
                        time.sleep(2)
                        teste.click()
                        print("Clicando em teste")
                        break
                except Exception as e:
                    print("Aguardando o botão de 'teste' antes de clicar...")
                    time.sleep(2)

            # Procura o campo de email de suporte de afiliados, clica nele e insere
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

            # Procura o campo de descrição de afiliados, clica nele e insere a descrição que foi gerada por IA na pasta específica de cada user_id
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

            # Procura o campo de duração de cookies, clica nele e seleciona a opção de eterno
            while True:
                try:
                    duracao_cookies = driver.find_element(By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[10]/div/select')
                    if duracao_cookies:
                        time.sleep(2)
                        duracao_cookies.click()
                        print("CLicando em duracao_cookies")
                        eterno = driver.find_element(By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[10]/div/select/option[1]')
                        if eterno:
                            time.sleep(2)
                            eterno.click()
                            print("Clicando em eterno")
                        break
                except Exception as e:
                    print("Aguardando o botão 'duracao_cookies' antes de clicar...")
                    time.sleep(2)

            # Procura o botão de salvar configuração de afiliados e clica nele
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

            # Procura o botão de copiar o link de afiliados e clica nele
            while True:
                try:
                    link_afiliado = driver.find_element(By.XPATH, '//*[@id="affiliates"]/div[3]/div/div[2]/div/div/div/div[2]/span/button')
                    if link_afiliado:
                        time.sleep(2)
                        link_afiliado.click()
                        print("CLicando em link_afiliado")
                        '''
                        usar o pyperclip para salvar o link em um arquivo de texto
                        '''
                        break
                except Exception as e:
                    print("Aguardando o botão 'link_afiliado' antes de clicar...")
                    time.sleep(2)

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
