# imports
import ollama
import os
import requests
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI

from rich.markdown import Markdown
from rich.console import Console
import sys

console = Console()

# Constants
MODEL_GPT = 'gpt-4o-mini'
MODEL_LLAMA = 'llama3.2'

# Set up environment
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key) > 10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")

openai = OpenAI()

# System Prompt
system_prompt = """You are an expert tutor in technology and programming. 
Your role is to provide clear and structured explanations in Markdown format about:
- Programming concepts and best practices.
- Code snippets provided by the user, including their functionality and possible optimizations.
- General technology topics, including AI, software development, networking, hardware, and emerging technologies.
- Comparisons between technologies, frameworks, or programming paradigms.
- Recommendations on tools, best practices, and industry trends.
Your responses must be **structured, educational, and formatted in Markdown**. 
Use headings, bullet points, code blocks, and bold/italic text where appropriate."""

# User Prompt
def user_prompt_for(query, is_code=False, language="a programming language"):
    if is_code:
        user_prompt = f"I will provide you with a code snippet written in {language}. Your task is to explain it in detail in **Markdown format**, including what it does and why it works.\n\n"
        user_prompt += f"**Code:**\n```{language}\n{query}\n```\n\n"
        user_prompt += "Please provide a structured breakdown of its functionality and suggest any improvements if applicable. Also, explain key concepts that would help me understand the code better."
    else:
        user_prompt = f"I have a question about technology. Please provide your response in **Markdown format**.\n\n"
        user_prompt += f"**Question:** {query}\n\n"
        user_prompt += "Please structure your response clearly using **headings, bullet points, and examples** where appropriate."

    return user_prompt

# Messages
def messages_for(query, is_code=False, language="a programming language"):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(query, is_code, language)}
    ]

# Get GPT-4o-mini to answer, with streaming
def get_explanation(query, is_code, language):
    stream = openai.chat.completions.create(
        model=MODEL_GPT,
        messages=messages_for(query, is_code, language),
        stream=True
    )

    response = ""
    in_jupyter = "ipykernel" in sys.modules

    if in_jupyter:
        display_handle = display(Markdown(""), display_id=True)
    
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        response_cleaned = response.replace("```", "").replace("markdown", "").strip()
        if in_jupyter:
            update_display(Markdown(response_cleaned), display_id=display_handle.display_id)
        else:
            console.print(Markdown(response))

# Get Llama 3.2 to answer
def get_explanation_ollama(query, is_code, language):
    response = ollama.chat(model=MODEL_LLAMA, messages=messages_for(query, is_code, language))
    return display(Markdown(response['message']['content']))

# CLI Execution
def main():
    print("🤖 Welcome to the AI Tutor")
    query = input("Enter your question or code: ")
    
    is_code = input("Is it code? (y/n): ").strip().lower() == "y"
    language = input("Enter your language: ") if is_code else "english"

    model = input("Which model do you want to use? (gpt/llama): ").strip().lower()
    
    print("\n⏳ Generating response...\n")

    if model == "llama":
        get_explanation_ollama(query, is_code, language)
    else:
        get_explanation(query, is_code, language)

if __name__ == "__main__":
    main()
