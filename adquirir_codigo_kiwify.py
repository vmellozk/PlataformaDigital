#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip

#
def adq_codigo_kw(driver):
    # Localiza o campo de pesquisar email, clica, insere o prompt passado e clica em ENTER
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
                pesquisar_email.send_keys('Kiwify codigo de verificação' + Keys.ENTER)
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
            codigo_kw = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id=":oq"]/div[1]/center/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr/td/div/div[6]/span'))
            )
            if codigo_kw:
                action = ActionChains(driver)
                time.sleep(2)
                action.double_click(codigo_kw).perform()
                print("Clicando em codigo_kw")
                time.sleep(2)
                action.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
                print("Texto copiado para a área de transferência")
                time.sleep(2)
                codigo = pyperclip.paste()
                with open('codigo_kw.txt', 'w') as file:
                    file.write(codigo)
                    print("codigo salvo no arquivo .txt")
                time.sleep(2)
                break
        except Exception as e:
            print("Aguardando o campo de 'codigo_kw' antes de clicar...")
            time.sleep(2)
