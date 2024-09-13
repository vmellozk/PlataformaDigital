#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#
def anexar_produto(driver):
    # Procura o botão de área de membros e clica nele
    while True:
        try:
            area_membros = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[12]/div/div[1]/nav/div[2]/a'))
            )
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
            adicionar = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[7]/div[1]/div[1]/div[1]/div[2]/button'))
            )
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
            nome_modulo = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/input'))
            )
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
            adicionar_modulo = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div/div[3]/button'))
            )
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
            simbolo_adicionar = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="options-menu"]'))
            )
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
            adicionar_conteudo = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[7]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/div[1]'))
            )
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
            titulo = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[7]/div[1]/div/div[4]/div[1]/div/div[2]/div/div/div[1]/div/input'))
            )
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
            selecione_computador = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="attachment"]/div[1]/div/button/div/div/span'))
            )
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
            criar_publicar = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[7]/div[1]/div/div[5]/div[3]/div'))
            )
            if criar_publicar:
                time.sleep(2)
                criar_publicar.click()
                print("CLicando em criar_publicar")
                time.sleep(1)
                driver.close()
                time.sleep(2)
                break
        except Exception as e:
            print("Aguardando o botão 'criar_publicar' antes de clicar...")
            time.sleep(2)
