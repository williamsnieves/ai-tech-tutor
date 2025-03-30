import os
import json
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
from rich.console import Console
from anthropic import Anthropic
from openai import OpenAI
from config.settings import OPENAI_API_KEY, ANTHROPIC_API_KEY, MODEL_CLAUDE

console = Console()

def handle_api_error(e: Exception, context: str) -> Dict[str, Any]:
    """Handle API errors and return a formatted error response"""
    error_msg = str(e)
    details = ""
    
    if hasattr(e, 'response'):
        try:
            details = e.response.json()
        except:
            details = str(e.response)
    
    console.print(f"[red]Error in {context}:[/red] {error_msg}")
    if details:
        console.print(f"[yellow]Details:[/yellow] {details}")
    
    return {
        "error": error_msg,
        "details": details
    }

def translate_text(text: str, target_language: str, api_key: str) -> str:
    """Translate text to target language using Claude"""
    try:
        client = Anthropic(api_key=api_key)
        
        prompt = f"""Translate the following text to {target_language}. 
        Keep any code blocks, technical terms, or special characters unchanged.
        Only translate the explanatory text.
        
        Text to translate:
        {text}"""
        
        response = client.messages.create(
            model=MODEL_CLAUDE,
            max_tokens=2000,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.content[0].text
    except Exception as e:
        console.print(f"[red]Translation error:[/red] {str(e)}")
        return text

def text_to_speech(text: str, voice: str = "onyx") -> Optional[str]:
    """Convert text to speech using OpenAI's TTS API"""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Create audio directory if it doesn't exist
        audio_dir = "audio"
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
        
        # Truncate text to 4000 characters (leaving room for formatting)
        # Try to break at a sentence boundary
        if len(text) > 4000:
            truncated_text = text[:4000]
            last_period = truncated_text.rfind('.')
            if last_period > 0:
                truncated_text = truncated_text[:last_period + 1]
            text = truncated_text + "... (response truncated due to length)"
        
        # Generate unique filename
        filename = f"{audio_dir}/response_{voice}_{hash(text)}.mp3"
        
        # Generate speech
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        # Save the audio file
        response.stream_to_file(filename)
        return filename
    except Exception as e:
        console.print(f"[red]Audio generation error:[/red] {str(e)}")
        return None

def get_github_trending_repos(topic: str, days: int = 7, limit: int = 5) -> Dict[str, Any]:
    """Get trending GitHub repositories for a topic"""
    try:
        url = f"https://github.com/trending/{topic}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        repos = []
        
        for article in soup.select('article.Box-row')[:limit]:
            repo_info = article.select_one('h2.h3 a')
            if not repo_info:
                continue
                
            name = repo_info.get_text(strip=True).replace(' ', '')
            url = f"https://github.com{repo_info['href']}"
            
            description = article.select_one('p')
            description = description.get_text(strip=True) if description else "No description"
            
            stars = article.select_one('a.Link--muted')
            stars = stars.get_text(strip=True) if stars else "0"
            
            repos.append({
                "name": name,
                "url": url,
                "description": description,
                "stars": stars
            })
        
        return {
            "repos": repos,
            "topic": topic,
            "days": days
        }
    except Exception as e:
        return handle_api_error(e, "GitHub API") 