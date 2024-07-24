import time
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pyperclip

def chatgpt_response():
    driver = uc.Chrome(version_main=126)
    driver.get('https://chat.openai.com')
    time.sleep(5)
    
    try:
        #Achando o elemento
        input_field = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
        time.sleep(5)
        
        #Prompt
        full_prompt = 'Responda em plaintext, como se fosse um código. Crie um eBook com base nas respostas do formulário abaixo. O eBook deve seguir a estrutura abaixo: 1. **Capa**:  - Título: "Insights do Formulário" - Autor: qualquer 2. **Introdução**: - Apresente o propósito do eBook e o que será coberto. 3. **Sumário**: - Liste as principais seções e tópicos que serão abordados. 4. **Conteúdo Principal**: - Divida o conteúdo em 5 seções, com base nas respostas do formulário. - Cada seção deve cobrir um conjunto específico de respostas e ser apresentada de forma clara e concisa. - Disserte também sobre a área comentada na resposta e abrança falando do mercado atual e futuro, contando as evoluções e afins. 5. **Conclusão**: - Resuma os principais pontos discutidos e forneça uma visão geral das conclusões. Certifique-se de que o eBook seja informativo e fácil de ler, com uma formatação limpa e organizada. Cada seção deve ser bem estruturada e os pontos principais destacados. Mantenha o conteúdo relevante e focado nos insights extraídos das respostas do formulário.'

        # Envia o texto do prompt
        actions = ActionChains(driver)
        input_field.send_keys(full_prompt)
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(60)
        print("Texto do prompt enviado:")

        # Localiza o botão de copiar e clica nele
        try:
            copy_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Copiar código')]")
            copy_button.click()
            time.sleep(2)

            copied_text = pyperclip.paste()
            with open("output.txt", "w", encoding="utf-8") as file:
                file.write(copied_text)

            print("Texto copiado e salvo em output.txt.")

        except Exception as e:
            print("Erro ao copiar o texto:", e)
            
    finally:
        driver.quit()

if __name__ == '__main__':
    chatgpt_response()
