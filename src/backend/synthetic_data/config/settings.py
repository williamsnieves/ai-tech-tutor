import os
from dotenv import load_dotenv
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Model IDs
MODEL_GPT = "gpt-4o-mini"
MODEL_CLAUDE = "claude-3-5-sonnet-latest"
MODEL_LLAMA = "meta-llama/Llama-3.2-1B"

# Mapping of model names to their full IDs
HUGGINGFACE_MODELS = {
    "llama": MODEL_LLAMA
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
DEFAULT_SAMPLE_SIZE = 10  # Added for consistency with generator.py

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

if not OPENAI_API_KEY:
    raise ValueError("❌ Missing OPENAI_API_KEY in the .env file")

if not ANTHROPIC_API_KEY:
    raise ValueError("❌ Missing ANTHROPIC_API_KEY in the .env file")

if not HUGGINGFACE_API_KEY:
    raise ValueError("❌ Missing HUGGINGFACE_API_KEY in the .env file") 