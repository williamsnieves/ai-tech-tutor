from abc import ABC, abstractmethod
from typing import Optional

class BaseClient(ABC):
    """Base interface for all model clients."""
    
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 1000, **kwargs) -> str:
        """Generate text using the model.
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum number of tokens to generate
            **kwargs: Additional model-specific parameters
            
        Returns:
            Generated text
        """
        pass
    
    @abstractmethod
    def test_model(self, model: Optional[str] = None) -> str:
        """Test if the model is working.
        
        Args:
            model: Optional model identifier to test
            
        Returns:
            Test response
        """
        pass 