#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#
def inserir_codigo_kw(driver):
    while True:
        try:
            verificacao_dois_fatores = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div/main/div[2]/div/div/div[1]'))
            )
            if verificacao_dois_fatores:
                time.sleep(2)
                print("Campo verificacao_dois_fatores encontrado")
                time.sleep(2)
                break
        except Exception as e:
            print("Aguardando o campo de 'verificacao_dois_fatores' antes de clicar...")
            time.sleep(2)

    # Procura onde está o campo para inserir o código e clica
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
                #aqui adicionar um send_keys para ler o arquivo criado com o codigo capturado no email e inserir no campo
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
                time.sleep(5)
                break
        except Exception as e:
            print("Aguardando o botão de 'verificar' antes de clicar...")
            time.sleep(2)
