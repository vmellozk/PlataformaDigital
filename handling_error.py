import time
import pyautogui
import os
import sys
import time

# Verifica se a imagem 'image_path' está na tela e clica na imagem 'click_image_path' se encontrada
def click_image_if_found(image_path, click_image_path):
    try:
        image_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.7)
        if image_location:
            click_location = pyautogui.locateCenterOnScreen(click_image_path, confidence=0.7)
            if click_location:
                pyautogui.click(click_location)
                return True
    except pyautogui.ImageNotFoundException:
        pass  # Não faz nada se a imagem não for encontrada
    except Exception as e:
        pass  # Trata exceções sem imprimir mensagens
    return False
