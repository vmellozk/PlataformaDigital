#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import threading

#
file_lock = threading.Lock()

# Variáveis para inserir nos campos
site = 'www.praticasenior.com'
preco = 'R$47,90'

#
def criar_produto_kw(driver, user_id):
    # Procura o botão de produtos e clica nele
    while True:
        try:
            produtos = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[2]/div/div/div[2]/nav/div[1]/a[2]'))
            )
            if produtos:
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
                criar_produto.click()
                print("Botão de criar produto encontrado")
                break
        except Exception as e:
            print("Aguardando botão de 'criar produto' antes de continuar...")
            time.sleep(2)

    # Procura o botão de continuar e clica nele
    while True:
        try:
            continuar = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[2]/button'))
            )
            if continuar:
                continuar.click()
                print("Clicando em continuar")
                break
        except Exception as e:
            print("Aguardando o botão de 'continuar' antes de clicar...")
            time.sleep(2)

    # Procura o campo de nome do produto, clica nele e insere o nome do produto mediante ao arquivo salvo e gerado pela IA na pasta de cada user_id específico
    while True:
        try:
            nome_produto = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[1]/div[2]/div/input'))
            )
            if nome_produto:
                nome_produto.click()
                print("Clicando em nome do produto")
                time.sleep(1)

                # Usa o lock para garantir que a leitura e escrita do arquivo não interfira com outra execução/threads. 
                with file_lock:
                    user_folder_name = os.path.join("users", str(user_id))
                    file_path_name = os.path.join(user_folder_name, "name_product.txt")

                    # Verifica se o caminho existe antes de tentar ler e depois insere o nome no campo
                    if os.path.exists(file_path_name):
                        with open(file_path_name, "r", encoding="utf-8") as file:
                            product_name = file.read().strip()
                        nome_produto.send_keys(product_name)
                        print(f"Nome do produto {product_name} inserindo para o user_id {user_id}")
                    else:
                        print(f"Arquivo 'name_product.txt' não encontrado para o user_id {user_id}")

                break
        except Exception as e:
            print("Aguardando o campo de 'nome do produto' antes de clicar...")
            time.sleep(2)

    # Procura o campo de descrição, clica nele e insere a descrição mediante ao arquivo salvo e gerado pela IA na pasta de cada user_id específico
    while True:
        try:
            descricao = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[1]/div[3]/div/textarea'))
            )
            if descricao:
                descricao.click()
                print("Clicando em descrição")
                time.sleep(1)

                # Usa o lock para garantir que a leitura e escrita do arquivo não interfira com outra execução/threads
                with file_lock:
                    user_folder_descricao = os.path.join("users", str(user_id))
                    file_path_descricao = os.path.join(user_folder_descricao, "descricao_product.txt")

                    # verifica se o caminho existe antes de tentar ler e depois insere o nome no campo
                    if os.path.exists(file_path_descricao):
                        with open(file_path_descricao, "r", encoding="utf-8") as file:
                            product_descricao = file.read().strip()
                        descricao.send_keys(product_descricao)
                        print(f"Descrição do produto inserida para o user_id {user_id}")
                    else:
                        print(f"Arquivo de descrição do produto não encontrado para o user_id {user_id}")

                break
        except Exception as e:
            print("Aguardando o campo de 'descrição' antes de clicar...")
            time.sleep(2)

    # Procura o campo de página de vendas, clica e insere a página de vendas
    while True:
        try:
            pagina_vendas = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[1]/div[4]/div[2]/input'))
            )
            if pagina_vendas:
                pagina_vendas.click()
                print("Clicando em pagina de vendas")
                time.sleep(1)
                pagina_vendas.send_keys(site)
                break
        except Exception as e:
            print("Aguardando o campo de 'página de vendas' antes de clicar...")
            time.sleep(2)

    # Procura o campo de preço, clica e insere o preço do produto
    while True:
        try:
            preco_produto = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[1]/div[5]/fieldset/div/input'))
            )
            if preco_produto:
                preco_produto.click()
                print("Clicando em preço")
                time.sleep(1)
                preco_produto.send_keys(preco)
                break
        except Exception as e:
            print("Aguardando o campo de 'preço' antes de clicar...")
            time.sleep(2)

    # Procura o botão de criar o produto e clica nele
    while True:
        try:
            criar_produto_final = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[2]/button'))
            )
            if criar_produto_final:
                criar_produto_final.click()
                print("Clicando em criar produto final")
                time.sleep(2)  # Aguarda 2 segundos após clicar
                try:
                    # Verifica se o XPath de erro não aparece
                    WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/header/h3'))
                    )
                    print("Erro ao continuar a criação do produto, tentando de novo")
                    continue
                except:
                    print("Produto criado com sucesso ou erro não encontrado.")

                break

        except Exception as e:
            print("Aguardando o botão 'criar produto final' antes de clicar...")
            time.sleep(2)
