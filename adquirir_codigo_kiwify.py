#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

#
def adq_codigo_kw(driver):
    #
    while True:
        try:
            pesquisar_email = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="gs_lc50"]/input[1]'))
            )
            if pesquisar_email:
                time.sleep(2)
                pesquisar_email.click()
                print("Clicando em pesquisar_email")
                time.sleep(1)
                pesquisar_email.send_keys('Kiwify codigo de verificação')
                #adicionar um enter para enviar
                time.sleep(3)
                break
        except Exception as e:
            print("Aguardando o campo de 'pesquisar_email' antes de clicar...")
            time.sleep(2)

    #
    while True:
        try:
            emails = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id=":aw"]/tbody'))
            )
            if emails:
                time.sleep(2)
                emails.click()
                print("Campo de emails apareceu")
                break
        except Exception as e:
            print("Aguardando o campo de 'emails' antes de clicar...")
            time.sleep(2)

    #
    while True:
        try:
            first_email = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id=":ax"]'))
            )
            if first_email:
                time.sleep(2)
                first_email.click()
                print("Clicando em first_email")
                break
        except Exception as e:
            print("Aguardando o campo de 'first_email' antes de clicar...")
            time.sleep(2)

    #
    while True:
        try:
            código_kw = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id=":oq"]/div[1]/center/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr/td/div/div[6]/span'))
            )
            if código_kw:
                time.sleep(2)
                #aqui dar um duplo clique rápido
                print("Clicando em código_kw")
                time.sleep(2)
                #aqui copiar o que foi selecionado com um ctrl c + ctrl v ou pyperclip e salvar num arquivo .txt dentro da pasta de cada user_id específico
                time.sleep(5)
                break
        except Exception as e:
            print("Aguardando o campo de 'código_kw' antes de clicar...")
            time.sleep(2)
