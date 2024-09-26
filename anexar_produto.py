#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import threading

#
file_lock = threading.Lock()

# Variáveis para inserção nos campos
modulo = 'eBook'
titulo_modulo = 'Baixe ou Visualize o Produto'

#
def anexar_produto(driver, user_id):
    # Procura o botão de adicionar e clica nele
    while True:
        try:
            adicionar = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[7]/div[1]/div[1]/div[1]/div[2]/button'))
            )
            if adicionar:
                adicionar.click()
                print("CLicando em adicionar")
                break
        except Exception as e:
            print("Aguardando o botão 'adicionar' antes de clicar...")
            time.sleep(2)

    # procura o campo do nome do módulo, clica nele e insere o nome do módulo
    while True:
        try:
            nome_modulo = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/input'))
            )
            if nome_modulo:
                nome_modulo.click()
                print("CLicando em nome_modulo")
                time.sleep(1)
                nome_modulo.send_keys(modulo)
                break
        except Exception as e:
            print("Aguardando o campo 'nome_modulo' antes de clicar...")
            time.sleep(2)

    # Procura o botão de adicionar o módulo e clica nele
    while True:
        try:
            adicionar_modulo = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div/div[3]/button'))
            )
            if adicionar_modulo:
                adicionar_modulo.click()
                print("CLicando em adicionar_modulo")
                break
        except Exception as e:
            print("Aguardando o botão 'adicionar_modulo' antes de clicar...")
            time.sleep(2)

    # Procura o símbolo de adicionar e clica nele
    while True:
        try:
            simbolo_adicionar = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[7]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]'))
            )
            if simbolo_adicionar:
                simbolo_adicionar.click()
                print("CLicando em simbolo_adicionar")
                break
        except Exception as e:
            print("Aguardando o botão 'simbolo_adicionar' antes de clicar...")
            time.sleep(2)

    # Procura o campo de adicionar conteúdo e clica nele
    while True:
        try:
            adicionar_conteudo = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[7]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/div[1]'))
            )
            if adicionar_conteudo:
                adicionar_conteudo.click()
                print("CLicando em adicionar_conteudo")
                break
        except Exception as e:
            print("Aguardando o botão 'adicionar_conteudo' antes de clicar...")
            time.sleep(2)

    # Procura o campo do título, clica nele e insere o título
    while True:
        try:
            titulo = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[7]/div[1]/div/div[4]/div[1]/div/div[2]/div/div/div[1]/div/input'))
            )
            if titulo:
                titulo.click()
                print("CLicando em titulo")
                time.sleep(1)
                titulo.send_keys(titulo_modulo)
                break
        except Exception as e:
            print("Aguardando o botão 'titulo' antes de clicar...")
            time.sleep(2)

    # Procura o botão de selecionar do computador, clica nele, e seleciona o ebook gerado na pasta específica de cada user_id
    while True:
        try:
            selecione_computador = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input.uppy-DragDrop-input'))
            )
            if selecione_computador:
                print("Campo selecione_computador encontrado")
                time.sleep(1)

                # Usa o lock para garantir que a leitura do arquivo não interfira com outra execução/threads
                with file_lock:
                    user_folder_ebook = os.path.join("users", str(user_id), "ebook")
                    
                    # Verifica se a pasta existe
                    if os.path.exists(user_folder_ebook):
                        # Procura o arquivo de eBook na pasta (supondo que há um único arquivo com extensão .pdf)
                        ebook_files = [f for f in os.listdir(user_folder_ebook) if f.endswith('.pdf')]

                        if ebook_files:
                            ebook_path = os.path.abspath(os.path.join(user_folder_ebook, ebook_files[0]))

                            selecione_computador.send_keys(ebook_path)
                            print(f"Anexando o eBook '{ebook_files[0]}' para o user_id {user_id}")
                        else:
                            print(f"Nenhum eBook encontrado na pasta 'ebook' para o user_id {user_id}")

                    else:
                        print(f"Pasta 'ebook' não encontrada para o user_id {user_id}")

                break
        except Exception as e:
            print("Aguardando o botão 'selecione_computador' antes de clicar...")
            time.sleep(2)

    # espera aparecer o botão de excluir para esperar carregar o pdf no site antes de seguir
    while True:
        try:
            excluir_pdf = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[7]/div[1]/div/div[4]/div[3]/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/button'))
            )
            if excluir_pdf:
                print("Botão excluir_pdf foi encontrado, seguindo")
                break
        except Exception as e:
            print()
            time.sleep(2)

    # Procura o botão de criar e publicar e clica nele
    while True:
        try:
            criar_publicar = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[7]/div[1]/div/div[5]/div[3]/div'))
            )
            if criar_publicar:
                criar_publicar.click()
                print("CLicando em criar_publicar")
                time.sleep(5)
                driver.close()
                time.sleep(5)
                break
        except Exception as e:
            print("Aguardando o botão 'criar_publicar' antes de clicar...")
            time.sleep(2)

    # Obter as abas abertas
    abas = driver.window_handles
    # Focar na última aba aberta (a mais recente)
    driver.switch_to.window(abas[-1])

    # Procura o botão de salvar e clica nele
    while True:
        try:
            salvar = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/header/button[2]'))
            )
            if salvar:
                salvar.click()
                print("CLicando em salvar")
                time.sleep(3)
                break
        except Exception as e:
            print("Aguardando o botão 'salvar' antes de clicar...")
            time.sleep(2)
