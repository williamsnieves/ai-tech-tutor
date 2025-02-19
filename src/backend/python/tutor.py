import openai
import ollama
from config import MODEL_GPT, MODEL_LLAMA, OPENAI_API_KEY
from utils import print_markdown_response

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY

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

# Generate User Prompt
def user_prompt_for(query, is_code=False, language="a programming language"):
    if is_code:
        return f"I will provide you with a {language} code snippet. Explain it in Markdown.\n```{language}\n{query}\n```"
    return f"**Question:** {query}\n\nPlease respond in Markdown format."

# Generate Messages
def messages_for(query, is_code=False, language="a programming language"):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(query, is_code, language)}
    ]

# Get GPT-4o-mini Response
def get_explanation(query, is_code, language):
    """Generates an explanation using OpenAI GPT model."""
    stream = openai.chat.completions.create(
        model=MODEL_GPT,
        messages=messages_for(query, is_code, language),
        stream=True
    )

    response = ""
    
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        response_cleaned = response.replace("```", "").replace("markdown", "").strip()
        print_markdown_response(response_cleaned)

# Get Llama Response
def get_explanation_ollama(query, is_code, language):
    """Generates an explanation using the Llama model (Ollama)."""
    response = ollama.chat(model=MODEL_LLAMA, messages=messages_for(query, is_code, language))
    print_markdown_response(response['message']['content'])
