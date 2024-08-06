import re

def clean_text(text):
    # Definindo que remove palavras específicas e caracteres especiais, além de remover caracteres não alfanuméricos e espaços
    words_to_remove = ['palavra1', 'palavra2']
    special_characters = r'[^\w\s]'

    # Remove palavras específicas
    for word in words_to_remove:
        text = re.sub(r'\b' + re.escape(word) + r'\b', '', text, flags=re.IGNORECASE)

    # Remove caracteres especiais
    text = re.sub(special_characters, '', text)

    return text
