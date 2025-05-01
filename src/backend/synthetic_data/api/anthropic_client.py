import os
from typing import Optional
import anthropic
from ..config.settings import ANTHROPIC_API_KEY, MODEL_CLAUDE

class AnthropicClient:
    """Cliente para interactuar con la API de Anthropic."""
    
    def __init__(self):
        """Inicializa el cliente de Anthropic con la API key."""
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Genera texto usando el modelo de Claude.
        
        Args:
            prompt: El prompt para la generación
            max_tokens: Número máximo de tokens a generar
            
        Returns:
            str: El texto generado
        """
        try:
            response = self.client.messages.create(
                model=MODEL_CLAUDE,
                max_tokens=max_tokens,
                temperature=0.7,
                system="You are a synthetic data generator. Generate realistic and coherent data in JSON format.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            raise Exception(f"Error generating with Anthropic: {str(e)}") 