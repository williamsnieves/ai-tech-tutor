import os
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from pathlib import Path
import openai
import anthropic
from huggingface_hub import InferenceClient
from src.backend.synthetic_data.config.settings import (
    MODEL_GPT, MODEL_CLAUDE, MODEL_LLAMA, MODEL_PHI3, MODEL_GEMMA, MODEL_DEEPSEEK,
    OPENAI_API_KEY, ANTHROPIC_API_KEY, HUGGINGFACE_API_KEY,
    DATA_TYPES, OUTPUT_FORMATS, DEFAULT_NUM_RECORDS,
    MAX_RECORDS_PER_REQUEST, MAX_RETRIES, RETRY_DELAY,
    ERROR_MESSAGES, DEFAULT_NUM_SAMPLES, DEFAULT_MAX_TOKENS, DEFAULT_OUTPUT_DIR,
    HUGGINGFACE_MODELS
)
from src.backend.synthetic_data.api.openai_client import OpenAIClient
from src.backend.synthetic_data.api.anthropic_client import AnthropicClient
from src.backend.synthetic_data.api.huggingface_client import HuggingFaceClient
from rich.console import Console
from datetime import datetime

console = Console()

class DataGenerator:
    """Clase principal para generar datos sintéticos usando diferentes modelos de LLM."""
    
    def __init__(self):
        """Inicializa los clientes de API necesarios."""
        self.openai_client = OpenAIClient()
        self.anthropic_client = AnthropicClient()
        self.huggingface_client = HuggingFaceClient()
        
    def _generate_prompt(self, data_type: str, num_samples: int, language: str = "en") -> str:
        """Generates a prompt for the LLM model."""
        if data_type not in DATA_TYPES:
            raise ValueError(f"Unsupported data type: {data_type}")
            
        data_info = DATA_TYPES[data_type]
        fields = ", ".join(data_info["fields"])
        
        # Map language to system message
        system_messages = {
            "en": "You are a synthetic data generator. Generate realistic and coherent data in JSON format. You MUST generate exactly the number of samples requested. Do not include any explanatory text, only the JSON array.",
            "es": "Eres un generador de datos sintéticos. Genera datos realistas y coherentes en formato JSON. DEBES generar exactamente el número de muestras solicitado. No incluyas texto explicativo, solo el array JSON.",
            "fr": "Vous êtes un générateur de données synthétiques. Générez des données réalistes et cohérentes au format JSON. Vous DEVEZ générer exactement le nombre d'échantillons demandé. N'incluez pas de texte explicatif, uniquement le tableau JSON.",
            "de": "Sie sind ein synthetischer Datengenerator. Generieren Sie realistische und kohärente Daten im JSON-Format. Sie MÜSSEN genau die angeforderte Anzahl von Proben generieren. Fügen Sie keinen erklärenden Text hinzu, nur das JSON-Array."
        }
        
        system_message = system_messages.get(language, system_messages["en"])
        
        return f"""
        {system_message}
        
        Generate EXACTLY {num_samples} examples of {data_type} data with the following fields:
        {fields}
        
        Requirements:
        1. Generate EXACTLY {num_samples} items in the JSON array
        2. Each item must contain all the specified fields
        3. The data must be realistic and coherent
        4. The output must be a valid JSON array
        5. Do not include any explanatory text, only the JSON array
        6. Do not include any markdown formatting
        7. Do not include any code block indicators
        8. The response must start with '[' and end with ']'
        
        Example format:
        [
            {{
                "field1": "value1",
                "field2": "value2"
            }},
            {{
                "field1": "value3",
                "field2": "value4"
            }}
        ]
        """
        
    def _save_data(self, data: List[Dict[str, Any]], output_format: str, output_dir: str) -> str:
        """Save the generated data to a file."""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"synthetic_data_{timestamp}.{output_format}"
        filepath = os.path.join(output_dir, filename)
        
        # Save data in the specified format
        if output_format == "json":
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        elif output_format == "csv":
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)
        elif output_format == "parquet":
            df = pd.DataFrame(data)
            df.to_parquet(filepath, index=False)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
            
        return filepath
        
    def generate(
        self,
        data_type: str,
        model: str,
        num_samples: int = DEFAULT_NUM_SAMPLES,
        output_format: str = "json",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        output_dir: str = DEFAULT_OUTPUT_DIR,
        language: str = "en"
    ) -> Dict[str, Any]:
        """Generates synthetic data using the specified model."""
        try:
            # Calculate batch size based on token limit
            # Assuming each sample uses roughly 100 tokens
            batch_size = min(20, num_samples)  # Default to 20 samples per batch
            total_batches = (num_samples + batch_size - 1) // batch_size
            all_data = []
            
            console.print(f"[yellow]Generating {num_samples} samples in {total_batches} batches...[/yellow]")
            
            for batch_num in range(total_batches):
                current_batch_size = min(batch_size, num_samples - len(all_data))
                console.print(f"[cyan]Processing batch {batch_num + 1}/{total_batches} ({current_batch_size} samples)...[/cyan]")
                
                prompt = self._generate_prompt(data_type, current_batch_size, language)
                
                if model == MODEL_GPT:
                    response = self.openai_client.generate(prompt, max_tokens=max_tokens)
                elif model == MODEL_CLAUDE:
                    response = self.anthropic_client.generate(prompt, max_tokens=max_tokens)
                elif model in [MODEL_LLAMA, MODEL_PHI3, MODEL_GEMMA, MODEL_DEEPSEEK]:
                    # Get the actual model ID from HUGGINGFACE_MODELS
                    model_id = HUGGINGFACE_MODELS[model]
                    response = self.huggingface_client.generate(prompt, model=model_id, max_tokens=max_tokens)
                else:
                    raise ValueError(f"Unsupported model: {model}")
                    
                # Try to parse the response as JSON
                try:
                    # Clean the response to ensure it's a valid JSON array
                    response = response.strip()
                    if response.startswith("```json"):
                        response = response[7:]
                    if response.endswith("```"):
                        response = response[:-3]
                    response = response.strip()
                    
                    data = json.loads(response)
                    
                    # Verify the number of samples in this batch
                    if not isinstance(data, list):
                        return {
                            "status": "error",
                            "message": "Response is not a JSON array",
                            "response": response
                        }
                        
                    if len(data) != current_batch_size:
                        return {
                            "status": "error",
                            "message": f"Generated {len(data)} samples instead of requested {current_batch_size} samples in batch {batch_num + 1}",
                            "response": response
                        }
                        
                    # Verify each item has all required fields
                    data_info = DATA_TYPES[data_type]
                    required_fields = set(data_info["fields"])
                    for i, item in enumerate(data):
                        item_fields = set(item.keys())
                        if not required_fields.issubset(item_fields):
                            missing_fields = required_fields - item_fields
                            return {
                                "status": "error",
                                "message": f"Item {i+1} in batch {batch_num + 1} is missing required fields: {missing_fields}",
                                "response": response
                            }
                            
                    all_data.extend(data)
                    
                except json.JSONDecodeError:
                    return {
                        "status": "error",
                        "message": "Response is not a valid JSON",
                        "response": response
                    }
                    
            # Save the complete dataset
            filepath = self._save_data(all_data, output_format, output_dir)
            
            return {
                "status": "success",
                "message": f"Successfully generated {len(all_data)} samples",
                "filepath": filepath,
                "data": all_data  # Include the data in the response
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating data: {str(e)}",
                "response": ""
            }

class SyntheticDataGenerator:
    def __init__(self, model: str):
        self.model = model
        self.console = Console()
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize API clients based on the selected model."""
        if self.model == "gpt":
            self.client = OpenAIClient()
        elif self.model == "claude":
            self.client = AnthropicClient()
        else:
            self.client = HuggingFaceClient()

    def _get_model_name(self) -> str:
        """Get the appropriate model name based on the selected model."""
        model_map = {
            "gpt": MODEL_GPT,
            "claude": MODEL_CLAUDE,
            "llama": MODEL_LLAMA,
            "phi3": MODEL_PHI3,
            "gemma": MODEL_GEMMA
        }
        return model_map.get(self.model)

    def _generate_prompt(self, data_type: str, fields: List[str], num_records: int) -> str:
        """Generate a prompt for the LLM based on the data type and fields."""
        return f"""
        Generate {num_records} synthetic {data_type} records with the following fields: {', '.join(fields)}.
        Each record should be realistic and follow the format:
        {{
            "field1": "value1",
            "field2": "value2",
            ...
        }}
        Return only the JSON array of records, no additional text.
        """

    def _validate_fields(self, data_type: str, fields: List[str]) -> bool:
        """Validate that the requested fields are valid for the data type."""
        valid_fields = DATA_TYPES.get(data_type, [])
        return all(field in valid_fields for field in fields)

    def _generate_data(self, data_type: str, fields: List[str], num_records: int) -> List[Dict[str, Any]]:
        """Generate synthetic data using the selected model."""
        if not self._validate_fields(data_type, fields):
            raise ValueError(ERROR_MESSAGES["invalid_data_type"].format(list(DATA_TYPES.keys())))

        prompt = self._generate_prompt(data_type, fields, num_records)
        model_name = self._get_model_name()

        for attempt in range(MAX_RETRIES):
            try:
                response = self.client.generate(
                    model=model_name,
                    prompt=prompt,
                    max_tokens=4000
                )
                data = json.loads(response)
                if isinstance(data, list) and len(data) == num_records:
                    return data
            except Exception as e:
                self.console.print(f"[red]Attempt {attempt + 1} failed: {str(e)}[/red]")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    raise ValueError(ERROR_MESSAGES["generation_failed"])

    def save_data(self, data: List[Dict[str, Any]], output_format: str, output_path: str):
        """Save the generated data in the specified format."""
        if output_format not in OUTPUT_FORMATS:
            raise ValueError(ERROR_MESSAGES["invalid_output_format"].format(list(OUTPUT_FORMATS.keys())))

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output_format == "json":
            with open(output_path, "w") as f:
                json.dump(data, f, indent=2)
        elif output_format == "csv":
            df = pd.DataFrame(data)
            df.to_csv(output_path, index=False)
        elif output_format == "parquet":
            df = pd.DataFrame(data)
            df.to_parquet(output_path, index=False)

    def generate(
        self,
        data_type: str,
        fields: List[str],
        num_records: int = DEFAULT_NUM_RECORDS,
        output_format: str = "json",
        output_path: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Main method to generate and save synthetic data."""
        if num_records > MAX_RECORDS_PER_REQUEST:
            self.console.print(f"[yellow]Warning: Number of records exceeds maximum per request. Generating {MAX_RECORDS_PER_REQUEST} records instead.[/yellow]")
            num_records = MAX_RECORDS_PER_REQUEST

        data = self._generate_data(data_type, fields, num_records)
        
        if output_path:
            self.save_data(data, output_format, output_path)
            self.console.print(f"[green]Data successfully saved to {output_path}[/green]")
        
        return data 