import time
import os
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Função para obter o contador de tentativas a partir de uma variável de ambiente
def get_attempt_counter(user_id):
    env_var_name = f"ATTEMPT_COUNTER_{user_id}"
    return int(os.environ.get(env_var_name, 0))

# Função para incrementar o contador de tentativas e salvar na variável de ambiente
def increment_attempt_counter(user_id):
    env_var_name = f"ATTEMPT_COUNTER_{user_id}"
    current_count = get_attempt_counter(user_id)
    new_count = current_count + 1
    os.environ[env_var_name] = str(new_count)
    return new_count

# Configura o limite de tentativas
MAX_ATTEMPTS = 3

def kill_chrome_processes():
    try:
        os.system("taskkill /im chrome.exe /f")
        os.system("taskkill /im chromedriver.exe /f")
    except Exception as e:
        print(f"Erro ao encerrar os processos do Chrome: {e}")

# Apaga arquivos específicos
def delete_files(file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)

# Verifica se a imagem 'image_path' está na tela e clica na imagem 'click_image_path' se encontrada
def click_element_if_found(driver):
    try:
        # Espera até que o elemento div esteja presente
        div_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.flex-grow.overflow-y-auto'))
        )
        if div_element:
            print("Elemento HTML 'div' encontrado.")
            
            # Agora, tenta encontrar e clicar no link 'Permanecer desconectado'
            link_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Permanecer desconectado"))
            )
            if link_element:
                time.sleep(1)
                link_element.click()
                print("Link 'Permanecer desconectado' encontrado e clicado.")
                time.sleep(1)
                return True

        return False
    except Exception as e:
        pass
    return False

# Atualiza a página e chama a função de envio de prompts
def handle_error(driver, responses_file, output_file, tittle_file, name, user_id):
    from generate_Ebook import generate_ebook
    attempt_counter = get_attempt_counter(user_id)
    try:
        # Aguarda até que o elemento SVG esteja presente
        svg_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".flex.max-w-full.flex-col.flex-grow .text-token-text-error svg.icon-lg"))
        )
        if svg_element:
            print("Elemento SVG encontrado.")
            time.sleep(1)
            
            # Apaga os arquivos gerados
            files_to_delete = [responses_file, output_file, tittle_file]
            delete_files(files_to_delete)
            print("Arquivos temporários apagados.")

            # Tenta encerrar o driver e matar os processos do Chrome
            try:
                driver.quit()
                print("Driver encerrado com sucesso.")
            except Exception as e:
                print(f"Erro ao encerrar o driver: {e}")
            kill_chrome_processes()
            time.sleep(1)
            
            # Incrementa o contador de tentativas e chama a função generate_ebook() para reiniciar o processo
            attempt_counter = increment_attempt_counter(user_id)
            if attempt_counter < MAX_ATTEMPTS:
                print(f"Tentativa {attempt_counter}/{MAX_ATTEMPTS}. Reiniciando o processo...")
                generate_ebook(user_id)
            else:
                print(f"Limite de tentativas {MAX_ATTEMPTS} alcançado. Abortando...")

    except Exception as e:
        pass
