import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de los modelos
MODEL_GPT = "gpt-4o-mini"
MODEL_LLAMA = "llama3.2"

# Claves API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Falta la clave OPENAI_API_KEY en el archivo .env")