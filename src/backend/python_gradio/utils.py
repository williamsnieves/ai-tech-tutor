from rich.markdown import Markdown
from rich.console import Console
import anthropic
import openai
from config import MODEL_CLAUDE
import base64
from io import BytesIO
from PIL import Image
import os
import tempfile

console = Console()

def print_markdown_response(text):
    """Print formatted markdown response."""
    md = Markdown(text)
    console.print(md)

def text_to_speech(text, voice="onyx"):
    """
    Convert text to speech using OpenAI's TTS API
    
    Args:
        text (str): Text to convert to speech
        voice (str): Voice to use (onyx, alloy, echo, fable, shimmer, nova)
        
    Returns:
        str: Path to the generated audio file
    """
    try:
        response = openai.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        # Create a temporary file to store the audio
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, "output_audio.mp3")
        
        # Save the audio content to the file
        with open(output_path, "wb") as f:
            f.write(response.content)
            
        return output_path
    except Exception as e:
        error_msg = f"Error generating speech: {str(e)}"
        console.print(f"[red]{error_msg}[/red]")
        return None

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