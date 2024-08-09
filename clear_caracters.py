import re

def clean_text(text):
    # Definindo palavras específicas para remover e a expressão regular para caracteres especiais que devem ser removidos, excluindo os que queremos manter
    words_to_remove = ['Capa', 'Título: ', 'Autor: ', '**Título:**', '**Autor:**']
    allowed_characters = r'[^A-Za-z0-9\s.,?!:;()+=/<>-áàâãéèêíìîóòôõúùûç]'

    # Remove palavras específicas e remove caracteres especiais não permitidos
    for word in words_to_remove:
        text = re.sub(r'\b' + re.escape(word) + r'\b', '', text, flags=re.IGNORECASE)
    text = re.sub(allowed_characters, '', text)
    return text
