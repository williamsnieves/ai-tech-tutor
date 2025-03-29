from rich.markdown import Markdown
from rich.console import Console
import anthropic
import openai
from config import MODEL_CLAUDE

console = Console()

def print_markdown_response(text):
    """Print formatted markdown response."""
    md = Markdown(text)
    console.print(md)

def translate_text(text, target_language, model=MODEL_CLAUDE, api_key=None):
    """
    Translate text to target language using Claude
    
    Args:
        text (str): Text to translate
        target_language (str): Target language (e.g., "Spanish")
        model (str): Model name to use
        api_key (str): Anthropic API key
    
    Returns:
        str: Translated text
    """
    if not api_key:
        raise ValueError("Missing API key for translation")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    system_prompt = f"You are a skilled translator. Translate the following text to {target_language}."
    
    response = client.messages.create(
        model=model,
        max_tokens=4000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": text}
        ]
    )
    
    return response.content[0].text 