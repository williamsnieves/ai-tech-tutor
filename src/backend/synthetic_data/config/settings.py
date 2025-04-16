import os
from dotenv import load_dotenv
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Models
MODEL_GPT = "gpt-4o-mini"
MODEL_CLAUDE = "claude-3-5-sonnet-latest"
MODEL_LLAMA = "meta-llama/Llama-2-7b-chat-hf"
MODEL_PHI3 = "microsoft/phi-3-mini-4k-instruct"
MODEL_GEMMA = "google/gemma-2-2b-it"
MODEL_DEEPSEEK = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"

# Model Mappings (for Hugging Face)
HUGGINGFACE_MODELS = {
    MODEL_LLAMA: "meta-llama/Llama-2-7b-chat-hf",
    MODEL_PHI3: "microsoft/phi-3-mini-4k-instruct",
    MODEL_GEMMA: "google/gemma-2-2b-it",
    MODEL_DEEPSEEK: "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
}

# Data Types
DATA_TYPES = {
    "business": {
        "fields": ["transactions", "employee_records", "inventory"],
        "description": "Business data including transactions, employee records, and inventory"
    },
    "health": {
        "fields": ["patient_records", "diagnoses", "treatments"],
        "description": "Healthcare data including patient records, diagnoses, and treatments"
    },
    "ecommerce": {
        "fields": ["orders", "customers", "products"],
        "description": "E-commerce data including orders, customers, and products"
    }
}

# Output Formats
OUTPUT_FORMATS = {
    "json": "JSON",
    "csv": "CSV",
    "parquet": "Parquet"
}

# Default Values
DEFAULT_NUM_SAMPLES = 10
DEFAULT_MAX_TOKENS = 1000

# Get the directory of the current file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Set the output directory to be inside the synthetic_data folder
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "data")

# Generation Parameters
DEFAULT_NUM_RECORDS = 10
MAX_RECORDS_PER_REQUEST = 50
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Error Messages
ERROR_MESSAGES = {
    "api_key_missing": "API key is missing. Please set the appropriate environment variable.",
    "model_not_found": "Model not found. Please check the model name.",
    "generation_failed": "Failed to generate data. Please try again.",
    "invalid_data_type": "Invalid data type. Please choose from: {}",
    "invalid_output_format": "Invalid output format. Please choose from: {}"
}

# Model configuration
MODEL_PHI4 = "microsoft/Phi-4-mini-instruct"
MODEL_GEMMA = "google/gemma-2-2b-it"

# Data Types
DATA_TYPES = {
    "business": {
        "name": "Business Data",
        "description": "Generate synthetic business data (finance, HR, sales, etc.)",
        "fields": ["transactions", "employee_records", "inventory"]
    },
    "health": {
        "name": "Clinical Data",
        "description": "Generate synthetic medical records and health data",
        "fields": ["patient_records", "diagnoses", "treatments"]
    },
    "ecommerce": {
        "name": "E-commerce Data",
        "description": "Generate user behavior and e-commerce data",
        "fields": ["user_sessions", "clickstream", "shopping_carts"]
    },
    "nlp": {
        "name": "Natural Language",
        "description": "Generate synthetic conversations and text",
        "fields": ["chat_logs", "emails", "reviews"]
    },
    "vision": {
        "name": "Computer Vision",
        "description": "Generate synthetic images",
        "fields": ["faces", "objects", "scenes"]
    },
    "traffic": {
        "name": "Traffic Data",
        "description": "Generate traffic and spatial data",
        "fields": ["vehicle_trajectories", "pedestrian_movement"]
    },
    "audio": {
        "name": "Audio Data",
        "description": "Generate synthetic audio and voice data",
        "fields": ["voice_commands", "conversations"]
    },
    "iot": {
        "name": "IoT Data",
        "description": "Generate industrial and IoT sensor data",
        "fields": ["sensor_readings", "machine_data"]
    },
    "documents": {
        "name": "Documents",
        "description": "Generate synthetic documents and forms",
        "fields": ["invoices", "contracts", "ids"]
    },
    "simulation": {
        "name": "3D/Simulation",
        "description": "Generate 3D and simulation data",
        "fields": ["3d_models", "simulation_data"]
    }
}

# Output Formats
OUTPUT_FORMATS = {
    "csv": "Comma-Separated Values",
    "json": "JavaScript Object Notation",
    "xml": "Extensible Markup Language",
    "parquet": "Apache Parquet",
    "sql": "SQL Database",
    "text": "Plain Text",
    "image": "Image Files",
    "audio": "Audio Files",
    "3d": "3D Model Files"
}

# Language options
LANGUAGES = ["English", "Spanish", "French", "German", "Chinese", "Japanese"]

# Voice options
VOICES = {
    "openai": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
    "elevenlabs": ["Rachel", "Domi", "Bella", "Antoni", "Josh", "Elli"]
}

if not OPENAI_API_KEY:
    raise ValueError("❌ Missing OPENAI_API_KEY in the .env file")

if not ANTHROPIC_API_KEY:
    raise ValueError("❌ Missing ANTHROPIC_API_KEY in the .env file")

if not HUGGINGFACE_API_KEY:
    raise ValueError("❌ Missing HUGGINGFACE_API_KEY in the .env file") 