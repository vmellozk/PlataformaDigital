#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#
def edit(driver):
    # Procura o botão de categoria e clica nele
    while True:
        try:
            categoria = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="general"]/div[1]/div/div[2]/div/div/div[3]/div/select'))
            )
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
            teste = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, ''))
            )
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
            imagem_produto = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="general"]/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div/button/div/div/span'))
            )
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
            teste = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, ''))
            )
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
            email_suporte = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="general"]/div[3]/div/div[2]/div/div/div/div[2]/div/div/input'))
            )
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
            nome_produtor = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="general"]/div[3]/div/div[2]/div/div/div/div[3]/div/div/input'))
            )
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
            salvar = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[17]/div[2]/button'))
            )
            if salvar:
                time.sleep(2)
                salvar.click()
                print("CLicando em salvar")
                break
        except Exception as e:
            print("Aguardando o botão 'salvar' antes de clicar...")
            time.sleep(2)