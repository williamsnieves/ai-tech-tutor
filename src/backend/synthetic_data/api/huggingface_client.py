import os
import platform
from typing import Dict, Any, Optional
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from huggingface_hub import login
from ..config.settings import (
    HUGGINGFACE_API_KEY,
    MODEL_LLAMA,
    MODEL_PHI3,
    MODEL_GEMMA,
    MODEL_DEEPSEEK,
    HUGGINGFACE_MODELS
)
import time
from functools import lru_cache

class HuggingFaceClient:
    """Client for interacting with Hugging Face models."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Hugging Face client."""
        self.api_key = api_key or HUGGINGFACE_API_KEY
        self._model_cache = {}
        self._tokenizer_cache = {}
        self._pipeline_cache = {}
        
        self.is_macos = platform.system() == "Darwin"
        print(f"Running on macOS: {self.is_macos}")
        print("Using HuggingFace API with CPU inference")
        
        # Login to Hugging Face
        try:
            login(token=self.api_key, add_to_git_credential=True)
            print("Successfully logged in to Hugging Face")
        except Exception as e:
            raise Exception(f"Failed to login to Hugging Face: {str(e)}")
        
        # Initialize model and tokenizer as None, will be loaded on first use
        self.model = None
        self.tokenizer = None
        self.current_model_id = None

    @lru_cache(maxsize=4)  # Cache up to 4 different models
    def _get_model(self, model_id: str):
        """Get cached model instance"""
        if model_id not in self._model_cache:
            print(f"Loading model {model_id}...")
            start_time = time.time()
            
            # Special optimizations for Llama 3.2-1B
            if "Llama-3.2-1B" in model_id:
                model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    token=self.api_key,
                    torch_dtype=torch.float32,
                    device_map="cpu",
                    low_cpu_mem_usage=True,
                    use_cache=True,
                    use_safetensors=True,
                    trust_remote_code=True  # Required for Llama models
                )
            else:
                model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    token=self.api_key,
                    torch_dtype=torch.float32,
                    device_map="cpu",
                    low_cpu_mem_usage=True,
                    use_cache=True,
                    use_safetensors=True
                )
            
            # Optimize model for inference
            model.eval()
            torch.set_grad_enabled(False)
            
            # Cache the model
            self._model_cache[model_id] = model
            print(f"Model loaded in {time.time() - start_time:.2f} seconds")
            
        return self._model_cache[model_id]
    
    @lru_cache(maxsize=4)  # Cache up to 4 different tokenizers
    def _get_tokenizer(self, model_id: str):
        """Get cached tokenizer instance"""
        if model_id not in self._tokenizer_cache:
            print(f"Loading tokenizer {model_id}...")
            start_time = time.time()
            
            # Special optimizations for Llama 3.2-1B
            if "Llama-3.2-1B" in model_id:
                tokenizer = AutoTokenizer.from_pretrained(
                    model_id,
                    token=self.api_key,
                    trust_remote_code=True  # Required for Llama models
                )
            else:
                tokenizer = AutoTokenizer.from_pretrained(model_id, token=self.api_key)
                
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
                
            # Cache the tokenizer
            self._tokenizer_cache[model_id] = tokenizer
            print(f"Tokenizer loaded in {time.time() - start_time:.2f} seconds")
            
        return self._tokenizer_cache[model_id]

    @lru_cache(maxsize=1)  # Cache only one pipeline since we're only using Llama
    def _get_pipeline(self, model_id: str):
        """Get cached pipeline instance"""
        if model_id not in self._pipeline_cache:
            print(f"Initializing pipeline for model {model_id}...")
            start_time = time.time()
            
            # Initialize the text generation pipeline
            pipe = pipeline(
                "text-generation",
                model=model_id,
                token=self.api_key,
                device_map="cpu",
                torch_dtype=torch.float32,
                trust_remote_code=True
            )
            
            # Cache the pipeline
            self._pipeline_cache[model_id] = pipe
            print(f"Pipeline initialized in {time.time() - start_time:.2f} seconds")
            
        return self._pipeline_cache[model_id]

    def test_model(self, model: str) -> str:
        """
        Test if a model is working by generating a simple greeting.
        
        Args:
            model: The model identifier to test
            
        Returns:
            A simple greeting response
        """
        try:
            print(f"\n=== Testing model: {model} ===")
            
            # Simple test prompt
            test_prompt = "Generate a simple greeting in English."
            
            # Use the existing generate method with a small max_tokens
            response = self.generate(
                prompt=test_prompt,
                model=model,
                max_tokens=50  # Small number of tokens for quick test
            )
            
            print(f"Test successful! Model response: {response}")
            return response
            
        except Exception as e:
            print(f"\nTest failed for model {model}:")
            print(f"Error: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            print(f"Traceback:\n{traceback.format_exc()}")
            raise

    def generate(self, prompt: str, model: str, max_tokens: int = 1000) -> str:
        """Generate text using the specified model."""
        try:
            # Get the model ID from the settings
            model_id = HUGGINGFACE_MODELS.get(model)
            if not model_id:
                raise ValueError(f"Model {model} not found in settings")
            
            print(f"\n=== Starting generation with model: {model_id} ===")
            print(f"Prompt: {prompt}")
            
            # Get the pipeline
            pipe = self._get_pipeline(model_id)
            
            # Generate text using the pipeline
            print("Generating response...")
            response = pipe(
                prompt,
                max_new_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                return_full_text=False,
                pad_token_id=pipe.tokenizer.pad_token_id,
                eos_token_id=pipe.tokenizer.eos_token_id
            )
            
            print(f"\nRaw pipeline response: {response}")
            
            # Extract the generated text
            if isinstance(response, list) and len(response) > 0:
                generated_text = response[0].get('generated_text', '')
                if not generated_text:
                    print("Warning: Generated text is empty")
                    # Try generating again with different parameters
                    response = pipe(
                        prompt,
                        max_new_tokens=max_tokens,
                        temperature=0.9,  # Increased temperature
                        top_p=0.95,      # Increased top_p
                        do_sample=True,
                        return_full_text=False,
                        pad_token_id=pipe.tokenizer.pad_token_id,
                        eos_token_id=pipe.tokenizer.eos_token_id
                    )
                    print(f"Second attempt response: {response}")
                    if isinstance(response, list) and len(response) > 0:
                        generated_text = response[0].get('generated_text', '')
                
                print(f"\nGenerated text: {generated_text}")
                return generated_text
            else:
                print(f"\nUnexpected response format: {response}")
                raise ValueError("Empty or invalid response from model")
                
        except Exception as e:
            print(f"\nError in generate: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            print(f"Traceback:\n{traceback.format_exc()}")
            raise 