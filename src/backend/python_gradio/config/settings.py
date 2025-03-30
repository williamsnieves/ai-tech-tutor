import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Model configuration
MODEL_GPT = "gpt-4o-mini"
MODEL_LLAMA = "llama3.2"
MODEL_CLAUDE = "claude-3-5-sonnet-latest"

# Language options
LANGUAGES = ["English", "Spanish"]

if not OPENAI_API_KEY:
    raise ValueError("❌ Missing OPENAI_API_KEY in the .env file")

if not ANTHROPIC_API_KEY:
    raise ValueError("❌ Missing ANTHROPIC_API_KEY in the .env file") 