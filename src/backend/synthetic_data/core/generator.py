import os
import json
from typing import Dict, List, Any
from datetime import datetime
from src.backend.synthetic_data.config.settings import (
    MODEL_GPT,
    MODEL_CLAUDE,
    HUGGINGFACE_MODELS,
    DEFAULT_NUM_SAMPLES,
    DEFAULT_MAX_TOKENS,
    DATA_TYPES
)
from src.backend.synthetic_data.api.huggingface_client import HuggingFaceClient
from src.backend.synthetic_data.api.openai_client import OpenAIClient
from src.backend.synthetic_data.api.anthropic_client import AnthropicClient

class DataGenerator:
    """Class for generating synthetic data using LLM models."""
    
    def __init__(self):
        """Initialize the data generator."""
        self.huggingface_client = HuggingFaceClient()
        self.openai_client = OpenAIClient()
        self.anthropic_client = AnthropicClient()

    def generate_data(
        self,
        data_type: str,
        model: str,
        sample_size: int = DEFAULT_NUM_SAMPLES,
        max_tokens: int = DEFAULT_MAX_TOKENS
    ) -> Dict[str, Any]:
        """
        Generate synthetic data using the specified model.
        
        Args:
            data_type: Type of data to generate
            model: Model to use for generation
            sample_size: Number of samples to generate
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Dictionary containing the generated data or error information
        """
        try:
            # Generate prompt
            prompt = self._create_prompt(data_type, sample_size)
            print(f"\n=== Generating with model: {model} ===")
            print(f"Prompt: {prompt}")
            
            # Select the appropriate client based on the model
            if model == MODEL_GPT:
                response = self.openai_client.generate(prompt, max_tokens=max_tokens)
            elif model == MODEL_CLAUDE:
                response = self.anthropic_client.generate(prompt, max_tokens=max_tokens)
            elif model in HUGGINGFACE_MODELS:
                response = self.huggingface_client.generate(
                    prompt=prompt,
                    model=model,
                    max_tokens=max_tokens
                )
            else:
                return {
                    "error": True,
                    "message": f"Model {model} not supported. Available models: {[MODEL_GPT, MODEL_CLAUDE] + list(HUGGINGFACE_MODELS.keys())}"
                }
            
            print(f"\nRaw response: {response}")
            
            # Parse response
            try:
                # Clean the response for Llama model
                if model in HUGGINGFACE_MODELS:
                    # Remove any markdown formatting
                    response = response.replace("```json", "").replace("```", "").strip()
                    # Remove any Llama-specific formatting
                    response = response.replace("<s>", "").replace("</s>", "").strip()
                    # Try to find the JSON array
                    start_idx = response.find('[')
                    end_idx = response.rfind(']')
                    if start_idx != -1 and end_idx != -1:
                        response = response[start_idx:end_idx+1]
                
                print(f"\nCleaned response: {response}")
                
                data = json.loads(response)
                
                # Validate the data structure
                if not isinstance(data, list):
                    return {
                        "error": True,
                        "message": "Response is not a JSON array",
                        "raw_response": response
                    }
                
                if len(data) != sample_size:
                    print(f"\nWarning: Generated {len(data)} samples instead of requested {sample_size}")
                    # Try to fix the data by repeating the last sample if needed
                    if len(data) < sample_size:
                        last_sample = data[-1] if data else {}
                        while len(data) < sample_size:
                            new_sample = last_sample.copy()
                            # Modify some fields to make it unique
                            for key in new_sample:
                                if isinstance(new_sample[key], str):
                                    new_sample[key] = f"{new_sample[key]}_{len(data)}"
                                elif isinstance(new_sample[key], (int, float)):
                                    new_sample[key] = new_sample[key] + len(data)
                            data.append(new_sample)
                        print(f"Fixed data by adding samples to reach {sample_size}")
                    else:
                        data = data[:sample_size]
                        print(f"Fixed data by truncating to {sample_size}")
                
                # Save the data to a file
                output_dir = "output"
                filepath = self._save_data(data, "json", output_dir)
                
                return {
                    "error": False,
                    "data": data,
                    "filepath": filepath
                }
            except json.JSONDecodeError as e:
                print(f"\nJSON Decode Error: {str(e)}")
                return {
                    "error": True,
                    "message": f"Failed to parse model response as JSON: {str(e)}",
                    "raw_response": response
                }
                
        except Exception as e:
            print(f"\nError: {str(e)}")
            return {
                "error": True,
                "message": str(e)
            }
    
    def _create_prompt(self, data_type: str, sample_size: int) -> str:
        """Create a prompt for data generation."""
        if data_type == "health":
            schema = """{
                "patient_id": "string",
                "age": "integer",
                "gender": "string",
                "diagnosis": "string",
                "treatment": "string",
                "admission_date": "string",
                "discharge_date": "string"
            }"""
            example = """[
    {
        "patient_id": "PAT001",
        "age": 45,
        "gender": "Female",
        "diagnosis": "Hypertension",
        "treatment": "Lisinopril 10mg daily",
        "admission_date": "2023-05-15",
        "discharge_date": "2023-05-17"
    },
    {
        "patient_id": "PAT002",
        "age": 32,
        "gender": "Male",
        "diagnosis": "Type 2 Diabetes",
        "treatment": "Metformin 500mg twice daily",
        "admission_date": "2023-06-01",
        "discharge_date": "2023-06-03"
    }
]"""
        elif data_type == "business":
            schema = """{
                "company_id": "string",
                "name": "string",
                "industry": "string",
                "revenue": "float",
                "employees": "integer",
                "location": "string",
                "founded_year": "integer"
            }"""
            example = """[
    {
        "company_id": "COMP001",
        "name": "TechCorp Solutions",
        "industry": "Technology",
        "revenue": 1500000.00,
        "employees": 50,
        "location": "San Francisco, CA",
        "founded_year": 2015
    },
    {
        "company_id": "COMP002",
        "name": "GreenEnergy Systems",
        "industry": "Renewable Energy",
        "revenue": 2500000.00,
        "employees": 75,
        "location": "Austin, TX",
        "founded_year": 2018
    }
]"""
        else:  # e-commerce
            schema = """{
                "order_id": "string",
                "customer_id": "string",
                "product": "string",
                "quantity": "integer",
                "price": "float",
                "order_date": "string",
                "shipping_address": "string"
            }"""
            example = """[
    {
        "order_id": "ORD001",
        "customer_id": "CUST001",
        "product": "Wireless Headphones",
        "quantity": 1,
        "price": 99.99,
        "order_date": "2023-07-15",
        "shipping_address": "123 Main St, New York, NY 10001"
    },
    {
        "order_id": "ORD002",
        "customer_id": "CUST002",
        "product": "Smart Watch",
        "quantity": 2,
        "price": 199.99,
        "order_date": "2023-07-16",
        "shipping_address": "456 Oak Ave, Los Angeles, CA 90001"
    }
]"""

        return f"""Generate EXACTLY {sample_size} synthetic {data_type} records in JSON format.
Each record should be realistic and follow this schema:
{schema}

IMPORTANT:
1. You MUST generate EXACTLY {sample_size} records
2. Return ONLY a JSON array containing exactly {sample_size} objects
3. Do not include any additional text, markdown, or formatting
4. Each object in the array must follow the schema exactly
5. Generate realistic data that matches the {data_type} domain
6. Each record should be unique and different from the others

Here is an example of the expected format with realistic {data_type} data:
{example}

Now generate {sample_size} new, unique records following the same format but with different realistic data."""

    def _save_data(self, data: List[Dict[str, Any]], output_format: str, output_dir: str) -> str:
        """Save the generated data to a file."""
        try:
            # Create the output directory if it doesn't exist
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            data_dir = os.path.join(project_root, "src", "backend", "synthetic_data", "data")
            os.makedirs(data_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"synthetic_{timestamp}.{output_format}"
            filepath = os.path.join(data_dir, filename)
            
            # Save the data
            if output_format == "json":
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=2)
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
            
            print(f"\nData saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"\nError saving data: {str(e)}")
            raise
        
    def generate(
        self,
        data_type: str,
        model: str,
        num_samples: int = DEFAULT_NUM_SAMPLES,
        output_format: str = "json",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        language: str = "en"
    ) -> Dict[str, Any]:
        """Generates synthetic data using the specified model."""
        try:
            # Calculate batch size based on token limit
            batch_size = min(10, num_samples)  # Reduced batch size for open-source models
            total_batches = (num_samples + batch_size - 1) // batch_size
            all_data = []
            
            print(f"Generating {num_samples} samples in {total_batches} batches...")
            
            for batch_num in range(total_batches):
                current_batch_size = min(batch_size, num_samples - len(all_data))
                print(f"Processing batch {batch_num + 1}/{total_batches} ({current_batch_size} samples)...")
                
                prompt = self._create_prompt(data_type, current_batch_size)
                
                response = self.huggingface_client.generate(
                    prompt=prompt,
                    model=model,
                    max_tokens=max_tokens
                )
                
                # Try to parse the response as JSON
                try:
                    # Clean the response to ensure it's a valid JSON array
                    response = response.strip()
                    if response.startswith("```json"):
                        response = response[7:]
                    if response.endswith("```"):
                        response = response[:-3]
                    response = response.strip()
                    
                    # Try to find the JSON array in the response
                    start_idx = response.find('[')
                    end_idx = response.rfind(']')
                    if start_idx != -1 and end_idx != -1:
                        response = response[start_idx:end_idx+1]
                    
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
                    
                except json.JSONDecodeError as e:
                    print(f"JSON Decode Error: {str(e)}")
                    print(f"Response: {response}")
                    return {
                        "status": "error",
                        "message": f"Response is not a valid JSON: {str(e)}",
                        "response": response
                    }
                    
            return {
                "status": "success",
                "message": f"Successfully generated {len(all_data)} samples",
                "data": all_data
            }
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return {
                "status": "error",
                "message": f"Error generating data: {str(e)}",
                "response": ""
            } 