import os
from typing import Dict, Any, Optional
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
from ..config.settings import (
    HUGGINGFACE_API_KEY,
    MODEL_LLAMA,
    MODEL_PHI3,
    MODEL_GEMMA,
    MODEL_DEEPSEEK,
    HUGGINGFACE_MODELS
)

class HuggingFaceClient:
    """Client for interacting with Hugging Face models."""
    
    def __init__(self):
        """Initialize the Hugging Face client."""
        self.api_key = HUGGINGFACE_API_KEY
        if not self.api_key:
            raise ValueError("Hugging Face API key is required")
        
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

    def _load_model(self, model_id: str) -> None:
        """Load model and tokenizer if not already loaded or if model changed."""
        if self.current_model_id != model_id:
            print(f"Loading model: {model_id}")
            try:
                # First try to load tokenizer
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_id,
                    trust_remote_code=True,
                    token=self.api_key
                )
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
                # Then load model for CPU
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    trust_remote_code=True,
                    token=self.api_key,
                    low_cpu_mem_usage=True
                )
                # Move model to CPU explicitly
                self.model = self.model.to("cpu")
                self.current_model_id = model_id
            except Exception as e:
                raise Exception(f"Error loading model {model_id}: {str(e)}")

    def generate(self, prompt: str, model: str, max_tokens: int = 1000) -> str:
        """
        Generate text using the specified model.
        
        Args:
            prompt: The input prompt
            model: The model identifier
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated text
        """
        try:
            if model not in HUGGINGFACE_MODELS:
                raise ValueError(f"Model {model} not supported. Available models: {list(HUGGINGFACE_MODELS.keys())}")
            
            model_id = HUGGINGFACE_MODELS[model]
            self._load_model(model_id)
            
            # Prepare chat messages
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
            
            # Apply chat template and prepare inputs
            inputs = self.tokenizer.apply_chat_template(
                messages,
                return_tensors="pt"
            )
            
            # Generate with specific parameters
            outputs = self.model.generate(
                inputs,
                max_new_tokens=max_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
                use_cache=True,
                max_length=max_tokens + inputs.shape[1]  # Add input length to max_length
            )
            
            # Decode and return
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
        except Exception as e:
            raise Exception(f"Error generating with Hugging Face: {str(e)}") 