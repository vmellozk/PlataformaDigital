#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

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
                time.sleep(5)
                break
        except Exception as e:
            print("Aguardando o campo de 'pesquisar_email' antes de clicar...")
            time.sleep(2)

    # Espera o campo dos emails aparecer para seguir com a automação
    while True:
        try:
            # XPath para encontrar o div final que contém os emails
            emails_xpath = '//*[contains(@id, "44")]/div[2]/div[6]/div[1]'
            emails = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, emails_xpath))
            )
            
            if emails:
                time.sleep(2)
                print("Campo de emails apareceu")
                break
        except Exception as e:
            print(f"Erro: {e}")
            print("Aguardando o campo de 'emails' antes de aparecer...")
            time.sleep(2)

    # Localiza o primeiro email e entra nele
    while True:
        try:
            # XPath da div que contém todos os emails
            emails_xpath = '//*[contains(@id, "44")]/div[2]/div[6]/div[1]'
            # XPath para o primeiro email dentro dessa div
            first_email_xpath = f'{emails_xpath}/descendant::div[contains(@id, ":")][1]'
            # Espera até que o primeiro email esteja presente
            first_email = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, first_email_xpath))
            )
            
            if first_email:
                time.sleep(2)
                # Clica no primeiro email para expandir o conteúdo
                first_email.click()
                print("Clicando no primeiro email")
                # XPath para o elemento 'td[4]' que contém o nome "Kiwify"
                kiwify_td_xpath = f'{first_email_xpath}/ancestor::tr/td[4]'
                # Espera até que o elemento td[4] esteja presente
                kiwify_td = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, kiwify_td_xpath))
                )
                
                if kiwify_td:
                    time.sleep(2)
                    kiwify_td.click()  # Clica no elemento para acessar o corpo do email
                    print("Clicando no 'td[4]' do primeiro email")
                    break
        except Exception as e:
            print(f"Erro: {e}")
            print("Aguardando o campo de 'first_email' antes de clicar...")
            time.sleep(2)

    # Localiza onde está localizado o campo do código, clica nele duas vezes para selecionar, copia o código e salva num arquivo .txt para depois ser lido e colocado na confirmação de dois fatores
    while True:
        try:
            # XPath do elemento com o texto a ser copiado
            xpath_element = '//*[contains(@id, ":")]/div[1]/center/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr/td/div/div[6]/span/strong'

            # Espera o elemento estar presente
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, xpath_element))
            )

            # Executa JavaScript para pegar o texto do elemento
            codigo_kw = driver.execute_script("return arguments[0].textContent;", element)

            # Imprime o texto copiado
            print("Texto copiado:", codigo_kw)

            # Salva o texto em um arquivo .txt
            with open('codigo_kw.txt', 'w') as file:
                file.write(codigo_kw)
                print("Código salvo no arquivo .txt")

            # Aguarda antes de sair do loop
            time.sleep(2)
            break

        except Exception as e:
            print("Aguardando o campo de 'codigo_kw' antes de clicar...", e)
            time.sleep(2)
