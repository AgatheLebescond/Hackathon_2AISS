import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # supprime espaces multiples
    text = re.sub(r'[\r\n\t]+', ' ', text)  # nettoie sauts de ligne, tabulations
    text = re.sub(r'\s([?.!,";:])', r'\1', text)  # supprime espace avant ponctuation
    return text.strip()
