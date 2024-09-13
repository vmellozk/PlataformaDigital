#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

#
load_dotenv()
KW_EMAIL_ADDRESS=os.getenv('KW_EMAIL_ADDRESS')
KW_EMAIL_PASSWORD=os.getenv('KW_EMAIL_PASSWORD')

#Detecta a url atual e comparada a com url passada, se for igual, ele vai fazer o login, abrindo o email para pegar o código, voltar para a aba e colar o código para logar
def login_kw(driver):
    #Clica no campo de email e insere o email
    while True:
        try:
            email_kw = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/main/div[1]/div/div[2]/form/div[1]/div[1]/input'))
            )
            if email_kw:
                time.sleep(2)
                email_kw.click()
                print("Campo de email_kw encontrado")
                email_kw.send_keys(KW_EMAIL_ADDRESS)
                break
        except Exception as e:
            print("Aguardando o campo de email antes de continuar...")
            time.sleep(2)

    #Clica no campo de senha e insere a senha
    while True:
        try:
            password_kw = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/main/div[1]/div/div[2]/form/div[2]/div/input'))
            )
            if password_kw:
                time.sleep(2)
                password_kw.click()
                print("Campo de senha encontrado")
                password_kw.send_keys(KW_EMAIL_PASSWORD)
                break
        except Exception as e:
            print("Aguardando o campo de senha antes de continuar...")
            time.sleep(2)

    #Clica no botão de login
    while True:
        try:
            login = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/main/div[1]/div/div[2]/form/div[4]/span/button'))
            )
            if login:
                time.sleep(2)
                login.click()
                print("Clicando em logar")
                time.sleep(5)
                break
        except Exception as e:
            print("Aguardando o botão de 'logar' antes de clicar...")
            time.sleep(2)

    # Verifica se vai aparecer a verificação de dois fatores
    while True:
        try:
            verificacao_dois_fatores = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div/main/div[2]/div/div/div[1]'))
            )
            if verificacao_dois_fatores:
                time.sleep(3)
                print("Verificacao de dois fatores apareceu")
                break
        except Exception as e:
            print("Aguardando se o campo de 'verificacao de dois' apareceu...")
            time.sleep(2)
