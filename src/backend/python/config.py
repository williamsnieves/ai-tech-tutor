import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model configuration
MODEL_GPT = "gpt-4o-mini"
MODEL_LLAMA = "llama3.2"

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ Missing OPENAI_API_KEY in the .env file")
