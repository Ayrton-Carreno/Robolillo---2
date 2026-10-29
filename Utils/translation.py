import json
import os

# ── Idiomas ─────────────────────────────────────────────
# Cada archivo Utils/lang/<código>.json es un idioma (es.json, en.json, pt.json...).
# Para agregar uno nuevo basta con copiar es.json, renombrarlo y traducir los textos.
CARPETA_IDIOMAS = os.path.join(os.path.dirname(__file__), "lang")
IDIOMA_DEFAULT = "es"

def cargar_idiomas() -> dict:
    textos = {}
    for archivo in sorted(os.listdir(CARPETA_IDIOMAS)):
        if archivo.endswith(".json"):
            codigo = archivo[:-5].lower()
            with open(os.path.join(CARPETA_IDIOMAS, archivo), encoding="utf-8") as f:
                textos[codigo] = json.load(f)
    return textos

TEXTOS = cargar_idiomas()

def idiomas_disponibles() -> dict:
    """{código: nombre} de todos los idiomas cargados."""
    return {codigo: textos.get("nombre_idioma", codigo) for codigo, textos in TEXTOS.items()}

def t(idioma: str, clave: str, **kwargs) -> str:
    """Obtiene el texto en el idioma indicado. Si falta la clave, usa el idioma por defecto."""
    texto = TEXTOS.get(idioma, {}).get(clave) or TEXTOS[IDIOMA_DEFAULT].get(clave, clave)
    return texto.format(**kwargs) if kwargs else texto
