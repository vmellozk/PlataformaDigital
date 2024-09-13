#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#
def copiar_link_afiliado(driver):
    # Procura o botão de salvar e clica nele
    while True:
        try:
            salvar = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[17]/div[2]/button'))
            )
            if salvar:
                time.sleep(2)
                salvar.click()
                print("CLicando em salvar")
                break
        except Exception as e:
            print("Aguardando o botão 'salvar' antes de clicar...")
            time.sleep(2)

    # Procura o botão de afiliados e clica nele
    while True:
        try:
            afiliados = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[12]/div/div[1]/nav/div[6]/a'))
            )
            if afiliados:
                time.sleep(2)
                afiliados.click()
                print("CLicando em afiliados")
                break
        except Exception as e:
            print("Aguardando o botão 'afiliados' antes de clicar...")
            time.sleep(2)

    # Procura o botão de habilitar afiliados e clica nele
    while True:
        try:
            habilitar_afiliados = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[1]/span/span'))
            )
            if habilitar_afiliados:
                time.sleep(2)
                habilitar_afiliados.click()
                print("CLicando em habilitar afiliados")
                break
        except Exception as e:
            print("Aguardando o botão 'habilitar afiliados' antes de clicar...")
            time.sleep(2)

    # Procura o botão de habilitar o market place e clica nele
    while True:
        try:
            habilitar_market_place = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[3]/div/span'))
            )
            if habilitar_market_place:
                time.sleep(2)
                habilitar_market_place.click()
                print("CLicando em habilitar_market_place")
                break
        except Exception as e:
            print("Aguardando o botão 'habilitar_market_place' antes de clicar...")
            time.sleep(2)

    # Procura o botão de categoria e clica nele
    while True:
        try:
            categoria_afiliados = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[4]/div/select'))
            )
            if categoria_afiliados:
                time.sleep(2)
                categoria_afiliados.click()
                print("CLicando em categoria_afiliados")
                break
        except Exception as e:
            print("Aguardando o botão 'categoria_afiliados' antes de clicar...")
            time.sleep(2)
    
    # Criar uma lógica para selecionar a categoria. pode ser perguntando ao chatgpt, salvando em um arquivo de texto, lendo o texto, procurando na div onde tem aquilo e clicar
    while True:
        try:
            teste = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, ''))
            )
            if teste:
                time.sleep(2)
                teste.click()
                print("Clicando em teste")
                break
        except Exception as e:
            print("Aguardando o botão de 'teste' antes de clicar...")
            time.sleep(2)

    # Procura o campo de email de suporte de afiliados, clica nele e insere
    while True:
        try:
            email_suporte_afiliados = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[5]/div/div/div/input'))
            )
            if email_suporte_afiliados:
                time.sleep(2)
                email_suporte_afiliados.click()
                print("CLicando em email_suporte_afiliados")
                break
        except Exception as e:
            print("Aguardando o campo 'email_suporte_afiliados' antes de clicar...")
            time.sleep(2)

    # Procura o campo de descrição de afiliados, clica nele e insere a descrição que foi gerada por IA na pasta específica de cada user_id
    while True:
        try:
            descricao_afiliados = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[6]/div[1]/textarea'))
            )
            if descricao_afiliados:
                time.sleep(2)
                descricao_afiliados.click()
                print("CLicando em descricao_afiliados")
                break
        except Exception as e:
            print("Aguardando o campo 'descricao_afiliados' antes de clicar...")
            time.sleep(2)

    # Procura o campo de duração de cookies, clica nele e seleciona a opção de eterno
    while True:
        try:
            duracao_cookies = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[10]/div/select'))
            )
            if duracao_cookies:
                time.sleep(2)
                duracao_cookies.click()
                print("CLicando em duracao_cookies")
                eterno = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[2]/div/div[2]/div/div/div[2]/div[10]/div/select/option[1]'))
            )
                if eterno:
                    time.sleep(2)
                    eterno.click()
                    print("Clicando em eterno")
                break
        except Exception as e:
            print("Aguardando o botão 'duracao_cookies' antes de clicar...")
            time.sleep(2)

    # Procura o botão de salvar configuração de afiliados e clica nele
    while True:
        try:
            salvar_config_afiliados = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[18]/div[2]/button'))
            )
            if salvar_config_afiliados:
                time.sleep(2)
                salvar_config_afiliados.click()
                print("CLicando em salvar_config_afiliados")
                break
        except Exception as e:
            print("Aguardando o  'salvar_config_afiliados' antes de clicar...")
            time.sleep(2)

    # Procura o botão de copiar o link de afiliados e clica nele
    while True:
        try:
            link_afiliado = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="affiliates"]/div[3]/div/div[2]/div/div/div/div[2]/span/button'))
            )
            if link_afiliado:
                time.sleep(2)
                link_afiliado.click()
                print("CLicando em link_afiliado")
                '''
                usar o pyperclip para salvar o link em um arquivo de texto
                '''
                break
        except Exception as e:
            print("Aguardando o botão 'link_afiliado' antes de clicar...")
            time.sleep(2)
