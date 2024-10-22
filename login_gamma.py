import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from dotenv import load_dotenv

#
load_dotenv()
GAMMA_EMAIL = os.getenv('GAMMA_EMAIL')
GAMMA_PASSWORD = os.getenv('GAMMA_PASSWORD')

# Verifica e interage com a div de 'Sign Up'
def login_gamma(driver):
    while True:
        try:
            sign_up = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div[1]/div/div/div/a'))
            )
            if sign_up:
                print("sign_up encontrado")
                time.sleep(2)
                sign_up.click()
                time.sleep(1)
                break
            else:
                print("sign_up não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrar o sign_up")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o sign_up: {e}")
            time.sleep(1)

    # Verifica e interage com a classe de 'Sign_in'
    while True:
        try:
            sign_in = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div/div/div/div/div/form/div/div[2]/div/p/a'))
            )
            if sign_in:
                print("sign_in encontrado")
                time.sleep(2)
                sign_in.click()
                time.sleep(1)
                break
            else:
                print("sign_in não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o input de sign_in")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o input de sign_in")
            time.sleep(1)

    # Verifica e interage com o input de 'Email'
    while True:
        try:
            email = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))
            )
            if email:
                print("email encontrado")
                time.sleep(2)
                email.click()
                time.sleep(1)
                email.send_keys(GAMMA_EMAIL)
                time.sleep(1)
                break
            else:
                print("email não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrar o input de email")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o input de email: {e}")
            time.sleep(1)

    # Verifica e interage com a div de 'password'
    while True:
        try:
            password = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
            )
            if password:
                print("password encontrado")
                time.sleep(2)
                password.click()
                time.sleep(1)
                password.send_keys(GAMMA_PASSWORD)
                time.sleep(1)
                break
            else:
                print("password não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrar o botão de password")
        except Exception as e:
            print(f"Erro ao encontrar o botão de password: {e}")

    # Verifica e interage com a div de 'Login Sign In'
    while True:
        try:
            login_sign_in = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div/div/div/div/div/form/div/div[5]'))
            )
            if login_sign_in:
                print("login_sign_in encontrado")
                time.sleep(2)
                login_sign_in.click()
                time.sleep(1)
                break
            else:
                print("login_sign_in não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o input de login_sign_in")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o input de login_sign_in")
            time.sleep(1)
