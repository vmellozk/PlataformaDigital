#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

#
load_dotenv()
GM_EMAIL_ADDRESS=os.getenv('GM_EMAIL_ADDRESS')
GM_EMAIL_PASSWORD=os.getenv('GM_EMAIL_PASSWORD')

#Detecta a url atual e verifica com a url passada, se for igual, ele vai logar, fornecendo a senha se for preciso e entrando no email
def login_gm(driver):
    #Procura onde está o campo de email, clica e insere o email
    while True:
        try:
            email_gm = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]'))
            )
            if email_gm:
                time.sleep(2)
                email_gm.click()
                print("Clicando em email_gm")
                email_gm.send_keys(GM_EMAIL_ADDRESS)
                break
        except Exception as e:
            print("Aguardando o campo de 'email_gm' antes de clicar...")
            time.sleep(2)

    #Procura onde está o botão de próximo e clica
    while True:
        try:
            email_proximo = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="identifierNext"]/div/button'))
            )
            if email_proximo:
                time.sleep(2)
                email_proximo.click()
                print("Clicando em email_proximo")
                break
        except Exception as e:
            print("Aguardando o botão de 'email_proximo' antes de clicar...")
            time.sleep(2)
    
    # Procura o campo de senha, clica e insere a senha
    while True:
        try:
            password_gm = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))
            )
            if password_gm:
                time.sleep(2)
                password_gm.click()
                print("Clicando em password")
                password_gm.send_keys(GM_EMAIL_PASSWORD)
                break
        except Exception as e:
            print("Aguardando o campo de 'password' antes de clicar...")
            time.sleep(2)

    # Procura onde está o botão de próximo e clica
    while True:
        try:
            password_proximo = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="passwordNext"]/div/button'))
            )
            if password_proximo:
                time.sleep(2)
                password_proximo.click()
                print("Clicando em password_proximo")
                time.sleep(5)
                break
        except Exception as e:
            print("Aguardando o botão de 'password_proximo' antes de clicar...")
            time.sleep(2)

    # Procura onde está o campo de identificação do gmail e passa
    while True:
        try:
            simbolo_gmail = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="gb"]/div[2]/div[1]/div[4]/div'))
            )
            if simbolo_gmail:
                time.sleep(2)
                print("Campo simbolo_gmail encontrado")
                time.sleep(5)
                break
        except Exception as e:
            print("Aguardando o campo de 'simbolo_gmail' antes de passar...")
            time.sleep(2)
