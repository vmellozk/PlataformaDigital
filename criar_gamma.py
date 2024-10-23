import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os

def  criar_gamma(driver, user_id):
    # Define a pasta de downloads específica para cada usuário
    user_folder_downloads = os.path.join("users", str(user_id), "downloads")
    os.makedirs(user_folder_downloads, exist_ok=True)  # Cria a pasta se não existir

    # Verifica e interage com o botão de 'Criar Novo'
    while True:
        try:
            criar_novo_ia = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/button[1]'))
            )
            if criar_novo_ia:
                print("criar_novo_ia encontrado")
                time.sleep(2)
                criar_novo_ia.click()
                time.sleep(1)
                break
            else:
                print("criar_novo_ia não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de criar_novo_ia")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de criar_novo_ia")
            time.sleep(1)

    # Verifica e interage com o botão de 'Colar no texto'
    while True:
        try:
            colar_texto = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[2]/div/div/div/div[1]'))
            )
            if colar_texto:
                print("colar_texto encontrado")
                time.sleep(2)
                colar_texto.click()
                time.sleep(1)
                break
            else:
                print("colar_texto não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de colar_texto")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de colar_texto")
            time.sleep(1)

    # Verifica e interage com o input de 'cole_aqui'
    while True:
        try:
            cole_aqui = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[2]/div/div/div[1]/div/div/div/div[1]/div/div/p'))
            )
            if cole_aqui:
                print("cole_aqui encontrado")
                time.sleep(2)
                cole_aqui.click()
                time.sleep(1)
                break
            else:
                print("cole_aqui não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o input de cole_aqui")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o input de cole_aqui")
            time.sleep(1)

    # Verifica e interage com a div de 'documento'
    while True:
        try:
            documento = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]'))
            )
            if documento:
                print("documento encontrado")
                time.sleep(2)
                documento.click()
                time.sleep(1)
                break
            else:
                print("documento não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada a div de documento")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar a div de documento")
            time.sleep(1)

    # Verifica e interage com o botão de 'continuar'
    while True:
        try:
            continuar = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[2]/div/div/div[3]'))
            )
            if continuar:
                print("continuar encontrado")
                time.sleep(2)
                continuar.click()
                time.sleep(1)
                break
            else:
                print("continuar não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de continuar")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de continuar")
            time.sleep(1)

    # Verifica e interage com o input de 'texto_detalhado'
    while True:
        try:
            texto_detalhado = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="accordion-panel-:rd3:"]/div/div[2]/div/button[3]'))
            )
            if texto_detalhado:
                print("texto_detalhado encontrado")
                time.sleep(2)
                texto_detalhado.click()
                time.sleep(1)
                break
            else:
                print("texto_detalhado não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o input de texto_detalhado")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o input de texto_detalhado")
            time.sleep(1)

    # Verifica e interage com o botão de 'adicionar_cartoes'
    while True:
        try:
            adicionar_cartoes = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div/div[2]/div/div[1]/button[3]'))
            )
            if adicionar_cartoes:
                print("adicionar_cartoes encontrado")
                time.sleep(2)
                adicionar_cartoes.click()
                time.sleep(1)
                adicionar_cartoes.click()
                break
            else:
                print("adicionar_cartoes não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de adicionar_cartoes")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de adicionar_cartoes")
            time.sleep(1)

    # Verifica e interage com o botão de 'continuar_e_gerar'
    while True:
        try:
            continuar_e_gerar = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/div/div[2]/div[2]/div[2]'))
            )
            if continuar_e_gerar:
                print("continuar_e_gerar encontrado")
                time.sleep(2)
                continuar_e_gerar.click()
                time.sleep(1)
                break
            else:
                print("continuar_e_gerar não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de continuar_e_gerar")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de continuar_e_gerar")
            time.sleep(1)

    # Verifica e interage com o botão de 'embaralhar'
    while True:
        try:
            embaralhar = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/button[2]'))
            )
            if embaralhar:
                print("embaralhar encontrado")
                time.sleep(2)
                embaralhar.click()
                time.sleep(1)
                break
            else:
                print("embaralhar não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de embaralhar")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de embaralhar")
            time.sleep(1)

    # Verifica e interage com o botão de 'gerar'
    while True:
        try:
            gerar = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/button[1]'))
            )
            if gerar:
                print("gerar encontrado")
                time.sleep(2)
                gerar.click()
                time.sleep(1)
                break
            else:
                print("gerar não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de gerar")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de gerar")
            time.sleep(1)

    # Verifica e interage com o botão de 'compartilhar'
    while True:
        try:
            compartilhar = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div/div[1]/div[2]/span/button'))
            )
            if compartilhar:
                print("compartilhar encontrado")
                time.sleep(2)
                compartilhar.click()
                time.sleep(1)
                break
            else:
                print("compartilhar não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de compartilhar")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de compartilhar")
            time.sleep(1)

    # Verifica e interage com o botão de 'exportar'
    while True:
        try:
            exportar = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="chakra-modal--body-:r3d3:"]/div[1]/div[1]/ul/li[3]'))
            )
            if exportar:
                print("exportar encontrado")
                time.sleep(2)
                exportar.click()
                time.sleep(1)
                break
            else:
                print("exportar não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de exportar")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de exportar")
            time.sleep(1)

    # Verifica e interage com o botão de 'exportar_pdf'
    while True:
        try:
            exportar_pdf = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="chakra-modal--body-:r3d3:"]/div[2]/div[1]/button[1]'))
            )
            if exportar_pdf:
                print("exportar_pdf encontrado")
                time.sleep(2)
                exportar_pdf.click()
                time.sleep(1)
                break
            else:
                print("exportar_pdf não encontrado")
        except TimeoutException:
            print("Tempo limite esgotado para encontrada o botão de exportar_pdf")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao encontrar o botão de exportar_pdf")
            time.sleep(1)

    #
    while True:
        try:
            # Localiza o botão 'Exportar para PDF' e clica para iniciar o download
            exportar_botao = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.css-104fw47'))
            )
            exportar_botao.click()
            print(f"Iniciando download do PDF para o user_id {user_id}")

            # Aguarda alguns segundos para o download ser concluído
            time.sleep(10)

            # Verifica se algum arquivo foi baixado na pasta
            arquivos_baixados = os.listdir(user_folder_downloads)
            if arquivos_baixados:
                print(f"Download concluído: {arquivos_baixados[0]}")
            else:
                print(f"Nenhum arquivo encontrado para o user_id {user_id}")

        except Exception as e:
            print(f"Erro ao baixar PDF: {e}")
