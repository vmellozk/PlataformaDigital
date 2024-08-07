import time
import pyautogui
import os
import sys

# Verifica se a imagem `image_path` está na tela e clica na imagem `click_image_path` se encontrada.
def click_image_if_found(image_path, click_image_path):
    image_location = pyautogui.locateCenterOnScreen(image_path)
    if image_location:
        pyautogui.click(click_image_path)
        return True
    return False

# Detecta um erro usando `image_path`, atualiza a página e reinicia o script se necessário.
def handle_error(image_path, refresh_image_path, script_path):
    if pyautogui.locateCenterOnScreen(image_path):
        print(f"Erro detectado com a imagem {image_path}. Atualizando a página e reiniciando o script.")
        pyautogui.hotkey('ctrl', 'r')
        time.sleep(5)
        restart_script(script_path)

# Verifica se a imagem `image_path` está na tela. Tenta até `retry_limit` vezes antes de reiniciar o script.
def handle_missing_image(image_path, retry_limit, retry_interval, script_path):
    retries = 0
    while retries < retry_limit:
        if not pyautogui.locateCenterOnScreen(image_path):
            print(f"Imagem {image_path} não encontrada. Tentando novamente em {retry_interval} segundos.")
            time.sleep(retry_interval)
            retries += 1
        else:
            print(f"Imagem {image_path} encontrada.")
            return
    print(f"Imagem {image_path} ainda não encontrada após {retry_limit} tentativas. Reiniciando o script.")
    restart_script(script_path)

# Reinicia o script atual.
def restart_script(script_path):
    print(f"Reiniciando o script {script_path}...")
    python = sys.executable
    os.execl(python, python, script_path)

# Função principal de exemplo
def main():
    script_path = 'automation.py'

    # Exemplo 1: Verifica e clica em uma imagem
    click_image_if_found('static/images/thanks_for_use_error.png', 'static/images/continue_desconected.png')

    # Exemplo 2: Lida com erro e reinicia se necessário
    handle_error('static/images/imagem3.png', None, script_path)

    # Exemplo 3: Lida com ausência de imagem e reinicia se necessário
    handle_missing_image('static/images/imagem4.png', retry_limit=5, retry_interval=10, script_path=script_path)
