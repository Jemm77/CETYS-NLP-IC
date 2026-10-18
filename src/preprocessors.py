import re


#Normalizador belico algo bien que rollo eta bien chido omg 
# si se normaliza menos y se tokeniza con palabras en mayusculas y caracteres especiales puede ser de ayuda para mejorar la accuracy del modelo pero ya tiene buena entonces hay que ver que rollo
def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text

#xd
