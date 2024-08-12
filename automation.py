import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from send_prompt import send_prompts

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

        # Envia os prompts
        send_prompts(input_field, responses_file, tittle_file, name)

    finally:
        if image_check_thread is not None:
            image_check_thread.join(timeout=5)
        if error_check_thread is not None:
            error_check_thread.join(timeout=5)
        try:
            driver.quit()
        except Exception as e:
            print(f"Erro ao encerrar o driver: {e}")
