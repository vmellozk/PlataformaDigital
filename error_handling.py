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
            time.sleep(1)
            click_location = pyautogui.locateCenterOnScreen(click_image_path, confidence=0.7)
            if click_location:
                pyautogui.click(click_location)
                time.sleep(1)
                return True
    except pyautogui.ImageNotFoundException:
        # adicionar um logging
        pass
    except Exception as e:
        # adicionar um logging
        pass
    return False
