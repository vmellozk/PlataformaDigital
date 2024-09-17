#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#
def inserir_codigo_kw(driver):
    # Verifica se o campo de verificação de dois fatores está presente para poder seguir com o código
    while True:
        try:
            body = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            
            if "Autenticação" in body.text:
                print("Texto 'Autenticação de 2 fatores' encontrado")
                time.sleep(2)
                break
            else:
                print("Texto 'Autenticação de 2 fatores' não encontrado")
        except Exception as e:
            print("Aguardando o texto 'Autenticação de 2 fatores' aparecer...", e)
            time.sleep(2)

    # Procura onde está o campo para inserir o código, clica nele, lê o arquivo com o código e insere ele no campo
    while True:
        try:
            campo_inserir_codigo = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div/main/div[2]/div/div/div[2]/div[1]/input'))
            )
            if campo_inserir_codigo:
                time.sleep(2)
                campo_inserir_codigo.click()
                print("Clicando em campo_inserir_codigo")
                time.sleep(2)
                with open('codigo_kw.txt', 'r', encoding='utf-8') as file:
                    codigo_read = file.read()
                campo_inserir_codigo.send_keys(codigo_read)
                print(f"Código inserido: {codigo_read}")
                time.sleep(2)
                break
        except Exception as e:
            print("Aguardando o botão de 'campo_inserir_codigo' antes de clicar...")
            time.sleep(2)

    # Procura onde está o botão de verificar e clica
    while True:
        try:
            verificar = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div/main/div[2]/div/div/div[2]/div[2]/button'))
            )
            if verificar:
                time.sleep(2)
                verificar.click()
                print("Clicando em verificar")
                time.sleep(3)
                break
        except Exception as e:
            print("Aguardando o botão de 'verificar' antes de clicar...")
            time.sleep(2)

    # Verifica se o site carregou verificando o elemento.
    while True:
        try:
            barra_nav = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[5]/div[2]/div/div/div[2]/nav/div[1]'))
            )
            if barra_nav:
                print("Campo barra_nav encontrado")
                time.sleep(2)
                break
        except Exception as e:
            print("Aguardando o campo de 'barra_nav' antes de clicar...")
            time.sleep(2)
