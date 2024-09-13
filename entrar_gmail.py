#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

#
load_dotenv()
GM_EMAIL_PASSWORD=os.getenv('GM_EMAIL_PASSWORD')

# Detecta a url atual, verifica com a url passada, se for igual, vai clicar em fazer login, selecionar o email, se aparecer o campo de senha vai clicar em senha e clicar em logar para abrir o email  
def entrar_gm(driver):        
    # Procura o botão de fazer login e clica
    while True:
        try:
            fazer_login_gmail = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/header/div/div/div/a[2]'))
            )
            if fazer_login_gmail:
                time.sleep(2)
                fazer_login_gmail.click()
                print("Clicando em fazer_login_gmail")
                break
        except Exception as e:
            print("Aguardando o botão de 'fazer_login_gmail' antes de clicar...")
            time.sleep(2)

    # Procura o campo do primeiro email e clica
    while True:
        try:
            email_clicar = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/form/span/section/div/div/div/div/ul/li[1]/div'))
            )
            if email_clicar:
                time.sleep(2)
                email_clicar.click()
                print("Clicando em email_clicar")
                break
        except Exception as e:
            print("Aguardando o campo de 'email_clicar' antes de clicar...")
            time.sleep(2)

    #Criar uma lógica para que se aparecer o campo de inserir a senha, é para inserir a lógica passada abaixo
    # Procura o campo de senha, clica e insere a senha
    while True:
        try:
            password_gm = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))
            )
            if password_gm:
                time.sleep(2)
                password_gm.click()
                print("Clicando em password_gm")
                password_gm.send_keys(GM_EMAIL_PASSWORD)
                break
        except Exception as e:
            print("Aguardando o botão de 'password_gm' antes de clicar...")
            time.sleep(2)

    # Procura o botão de próximo e clica
    while True:
        try:
            teste = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="passwordNext"]/div/button'))
            )
            if teste:
                time.sleep(2)
                teste.click()
                print("Clicando em teste")
                break
        except Exception as e:
            print("Aguardando o botão de 'teste' antes de clicar...")
            time.sleep(2)
