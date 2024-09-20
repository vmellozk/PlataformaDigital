#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import threading
from selenium.webdriver.support.ui import Select

#
file_lock = threading.Lock()

#
def edit(driver, user_id):
    # Procura o botão de categoria e clica nele
    while True:
        try:
            categoria = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="general"]/div[1]/div/div[2]/div/div/div[3]/div/select'))
            )
            if categoria:
                time.sleep(2)
                categoria.click()
                print("Clicando em categoria")
                break
        except Exception as e:
            print("Aguardando o campo 'categoria' antes de clicar...")
            time.sleep(2)

    # aqui deve-se criar uma lógica para selecionar a categoria. pode ser perguntando ao chatgpt, salvando em um arquivo de texto, lendo o texto, procurando na div onde tem aquilo e clicar 
    while True:
        try:
            selecionar_categoria = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="general"]/div[1]/div/div[2]/div/div/div[3]/div/select'))
            )
            if selecionar_categoria:
                time.sleep(1)
                print("Selecionando a categoria")
                time.sleep(1)

                # Usa o lock para garantir que a leitura e escrita do arquivo não interfira com outra execução/threads.
                while file_lock:
                    user_folder_categoria = os.path.join("users", str(user_id))
                    file_path_categoria = os.path.join(user_folder_categoria, "categoria.txt")

                    # Verifica se o caminho existe antes de tentar ler e depois insere o nome no campo
                    if os.path.exists(file_path_categoria):
                        with open(file_path_categoria, "r", encoding="utf-8") as file:
                            categoria_read = file.read().strip()

                        #
                        select_element = Select(selecionar_categoria)
                        
                        #
                        try:
                            select_element.select_by_visible_text(categoria_read)
                            print(f"Categoria '{categoria_read}' selecionada para o user_id {user_id}")
                        except Exception as e:
                            print(f"Categoria '{categoria_read}' não encontrada para o user_id {user_id}")

                        break
                else:
                    print(f"Arquivo com a categoria não encontrado para o user_id {user_id}")

                break
        except Exception as e:
            print("Aguardando o botão de 'selecionar_categoria' antes de clicar...")
            time.sleep(2)

    # Procura o botão de selecionar a imagem do produto e clica nele
    while True:
        try:
            # Localiza o campo de input (tipo file)
            imagem_produto = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input.uppy-DragDrop-input'))
            )
            
            if imagem_produto:
                print("Encontrado campo de upload.")
                
                # Usa o lock para garantir que a leitura do arquivo não interfira com outra execução/threads
                with file_lock:
                    user_folder_images = os.path.join("users", str(user_id), "images")

                    # Verifica se a pasta existe
                    if os.path.exists(user_folder_images):
                        # Procura o arquivo de imagem na pasta
                        image_files = [f for f in os.listdir(user_folder_images) if f.endswith(('.jpg', '.jpeg', '.png'))]

                        if image_files:
                            # Converte o caminho relativo para caminho absoluto
                            image_path = os.path.abspath(os.path.join(user_folder_images, image_files[0]))

                            # Usa o send_keys para anexar o arquivo
                            imagem_produto.send_keys(image_path)
                            print(f"Anexando a imagem '{image_files[0]}' para o user_id {user_id}")
                        else:
                            print(f"Nenhuma imagem encontrada na pasta 'images' para o user_id {user_id}")
                    else:
                        print(f"Pasta 'images' não encontrada para o user_id {user_id}")

                break
        except Exception as e:
            print(f"Aguardando o campo de upload: {str(e)}")
            time.sleep(2)
    
    # espera aparecer o remover imagem para esperar carregar a imagem no site antes de seguir
    while True:
        try:
            remover_imagem = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="general"]/div[1]/div/div[2]/div/div/div[4]/div[1]'))
            )
            if remover_imagem:
                time.sleep(2)
                print("Texto remover_imagem foi encontrado, seguindo")
                break
        except Exception as e:
            print()
            time.sleep(2)

    # Procura o campo de inserir o email de suporte, clica nele e insere o email de suporte
    while True:
        try:
            email_suporte = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="general"]/div[3]/div/div[2]/div/div/div/div[2]/div/div/input'))
            )
            if email_suporte:
                time.sleep(2)
                email_suporte.click()
                print("CLicando em email suporte")
                time.sleep(1)
                email_suporte.send_keys('contato.praticasenior@gmail.com')
                time.sleep(1)
                break
        except Exception as e:
            print("Aguardando o campo 'email suporte' antes de clicar...")
            time.sleep(2)

    # Procura o campo do nome do produtor, clica nele e insere
    while True:
        try:
            nome_produtor = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="general"]/div[3]/div/div[2]/div/div/div/div[3]/div/div/input'))
            )
            if nome_produtor:
                time.sleep(2)
                nome_produtor.click()
                print("CLicando em nome produtor")
                print(1)
                nome_produtor.send_keys('Prática Sênior')
                time.sleep(1)
                break
        except Exception as e:
            print("Aguardando o campo 'nome produtor' antes de clicar...")
            time.sleep(2)

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

    # Procura o botão de área de membros e clica nele
    while True:
        try:
            area_membros = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[4]/div[3]/main/div[2]/div[2]/div/div[12]/div/div[1]/nav/div[2]/a'))
            )
            if area_membros:
                time.sleep(2)
                area_membros.click()
                print("CLicando em area_membros")
                time.sleep(5)
                break
        except Exception as e:
            print("Aguardando o botão 'area_membros' antes de clicar...")
            time.sleep(2)

    # Obter as abas abertas
    abas = driver.window_handles
    # Focar na última aba aberta (a mais recente)
    driver.switch_to.window(abas[-1])
