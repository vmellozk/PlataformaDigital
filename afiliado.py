#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import threading
from selenium.webdriver.support.ui import Select
import pyperclip

#
file_lock = threading.Lock()

#
def copiar_link_afiliado(driver, user_id):
    # Procura o botão de afiliados e clica nele
    while True:
        try:
            afiliados = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[12]/div/div[1]/nav/div[6]/a'))
            )
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
            habilitar_afiliados = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[1]/span/span'))
            )
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
            habilitar_market_place = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[3]/div/span'))
            )
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
            categoria_afiliados = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[4]/div/select'))
            )
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
            selecionar_categoria = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[4]/div/select'))
            )
            if selecionar_categoria:
                time.sleep(1)
                print("Selecionando a categoria")
                time.sleep(1)

                # Usa o lock para garantir que a leitura e escrita do arquivo não interfira com outra execução/threads.
                while file_lock:
                    user_folder_categoria = os.path.join("users", str(user_id))
                    file_path_categoria = os.path.join(user_folder_categoria, "categoria.txt")

                    # Verifica se o caminho existe antes de tentar ler e depois insere o nome no campo
                    if os.path.exists(file_path_categoria):
                        with open(file_path_categoria, "r", encoding="utf-8") as file:
                            categoria_read = file.read().strip()

                        #
                        select_element = Select(selecionar_categoria)
                        
                        #
                        try:
                            select_element.select_by_visible_text(categoria_read)
                            print(f"Categoria '{categoria_read}' selecionada para o user_id {user_id}")
                        except Exception as e:
                            print(f"Categoria '{categoria_read}' não encontrada para o user_id {user_id}")

                        break
                else:
                    print(f"Arquivo com a categoria não encontrado para o user_id {user_id}")

                break
        except Exception as e:
            print("Aguardando o botão de 'selecionar_categoria' antes de clicar...")
            time.sleep(2)

    # Procura o campo de email de suporte de afiliados, clica nele e insere
    while True:
        try:
            email_suporte_afiliados = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[5]/div/div/div/input'))
            )
            if email_suporte_afiliados:
                time.sleep(2)
                email_suporte_afiliados.click()
                print("CLicando em email_suporte_afiliados")
                time.sleep(2)
                email_suporte_afiliados.send_keys('contato.praticasenior@afiliados.com')
                time.sleep(1)
                break
        except Exception as e:
            print("Aguardando o campo 'email_suporte_afiliados' antes de clicar...")
            time.sleep(2)

    # Procura o campo de descrição de afiliados, clica nele e insere a descrição que foi gerada por IA na pasta específica de cada user_id
    while True:
        try:
            descricao_afiliados = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[6]/div[1]/textarea'))
            )
            if descricao_afiliados:
                time.sleep(2)
                descricao_afiliados.click()
                print("CLicando em descricao_afiliados")
                time.sleep(2)
                descricao_afiliados.send_keys('Teste Descrição Afiliados Teste Descrição Afiliados Teste Descrição Afiliados Teste Descrição Afiliados Teste Descrição Afiliados Teste Descrição Afiliados Teste Descrição Afiliados Teste Descrição Afiliados Teste Descrição Afiliados Teste Descrição Afiliados Teste Descrição Afiliados Teste Descrição Afiliados')
                break
        except Exception as e:
            print("Aguardando o campo 'descricao_afiliados' antes de clicar...")
            time.sleep(2)

    # Procura o campo de duração de cookies, clica nele e seleciona a opção de eterno
    while True:
        try:
            duracao_cookies = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[10]/div/select'))
            )
            if duracao_cookies:
                time.sleep(2)
                duracao_cookies.click()
                print("CLicando em duracao_cookies")
                eterno = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[10]/div/select/option[1]'))
            )
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
            salvar_config_afiliados = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[18]/div[2]/button'))
            )
            if salvar_config_afiliados:
                time.sleep(2)
                salvar_config_afiliados.click()
                print("CLicando em salvar_config_afiliados")
                time.sleep(3)
                break
        except Exception as e:
            print("Aguardando o  'salvar_config_afiliados' antes de clicar...")
            time.sleep(2)

    # Procura o botão de copiar o link de afiliados e clica nele
    while True:
        try:
            botao_copiar_link_afiliado = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[3]/div/div[2]/div/div/div/div[2]/span/button'))
            )
            if botao_copiar_link_afiliado:
                time.sleep(2)
                botao_copiar_link_afiliado.click()
                print("CLicando em botao_copiar_link_afiliado")
                time.sleep(3)
                botao_copiar_link_afiliado_copiado = pyperclip.paste()

                #
                with file_lock:
                    user_folder_link = os.path.join("users", str(user_id))
                    os.makedirs(user_folder_link, exist_ok=True)
                    file_path_link = os.path.join(user_folder_link, "botao_copiar_link_afiliado.txt")

                    #
                    with open(file_path_link, "w", encoding="utf-8") as file:
                        file.write(botao_copiar_link_afiliado_copiado)

                break
        except Exception as e:
            print("Aguardando o botão 'botao_copiar_link_afiliado' antes de clicar...")
            time.sleep(2)
