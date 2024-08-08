import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from error_handling import click_image_if_found, handle_error
from send_prompt import send_prompts
import threading

# Declara a variável global para as threads de verificação
image_check_thread = None
error_check_thread = None

def chatgpt_response(responses_file, output_file, tittle_file, name):
    global image_check_thread, error_check_thread
    driver = uc.Chrome(version_main=126)

    try:
        driver.maximize_window()
        driver.get('https://chat.openai.com')
        time.sleep(2)

        input_field = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
        time.sleep(1)
        input_field.click()
        time.sleep(1)

        # Inicia a verificação contínua em threads separadas
        image_check_thread = threading.Thread(target=continuously_check_images, daemon=True)
        image_check_thread.start()
        error_check_thread = threading.Thread(target=continuously_check_errors, args=(driver, input_field, responses_file, tittle_file, name), daemon=True)
        error_check_thread.start()

        # Envia os prompts
        send_prompts(input_field, responses_file, tittle_file, name)

    finally:
        if image_check_thread is not None:
            image_check_thread.join(timeout=3)
        if error_check_thread is not None:
            error_check_thread.join(timeout=3)
        try:
            driver.quit()
        except Exception as e:
            print(f"Erro ao encerrar o driver: {e}")

# Verifica continuamente se a imagem está presente e clica na imagem especificada
def continuously_check_images():
    while True:
        try:
            found = click_image_if_found('static/error/thanks_for_use_error.png', 'static/error/continue_desconected.png')
            if found:
                pass
        except Exception as e:
            pass
        time.sleep(2)

# Verifica continuamente se a imagem de erro está presente e atualiza a página se necessário
def continuously_check_errors(driver, input_field, responses_file, tittle_file, name):
    while True:
        try:
            handle_error(driver, input_field, responses_file, tittle_file, name)
            time.sleep(2)
        except Exception as e:
            pass
        time.sleep(2)
