#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#
def criar_produto_kw(driver):
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
            continuar = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[2]/button'))
            )
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
            nome_produto = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[1]/div[2]/div/input'))
            )
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
            descricao = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[1]/div[3]/div/textarea'))
            )
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
            pagina_vendas = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[1]/div[4]/div[2]/input'))
            )
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
            preco = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[1]/div[5]/fieldset/div/input'))
            )
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
            criar_produto_final = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div/div/div[2]/button'))
            )
            if criar_produto_final:
                time.sleep(2)
                criar_produto_final.click()
                print("CLicando em criar produto final")
                break
        except Exception as e:
            print("Aguardando o botão 'criar produto final' antes de clicar...")
            time.sleep(2)