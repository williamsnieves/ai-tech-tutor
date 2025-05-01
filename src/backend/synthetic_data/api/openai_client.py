import os
from typing import Optional
from openai import OpenAI
from ..config.settings import OPENAI_API_KEY, MODEL_GPT

class OpenAIClient:
    """Cliente para interactuar con la API de OpenAI."""
    
    def __init__(self):
        """Inicializa el cliente de OpenAI con la API key."""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Genera texto usando el modelo de OpenAI.
        
        Args:
            prompt: El prompt para la generación
            max_tokens: Número máximo de tokens a generar
            
        Returns:
            str: El texto generado
        """
        try:
            response = self.client.chat.completions.create(
                model=MODEL_GPT,
                messages=[
                    {"role": "system", "content": "You are a synthetic data generator. Generate realistic and coherent data in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error generating with OpenAI: {str(e)}") 