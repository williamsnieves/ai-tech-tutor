import openai
import ollama
import anthropic
from config import MODEL_GPT, MODEL_LLAMA, MODEL_CLAUDE, OPENAI_API_KEY, ANTHROPIC_API_KEY
from utils import print_markdown_response
from tools import tools, handle_tool_calls

# Initialize API clients
openai.api_key = OPENAI_API_KEY
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# System Prompt
system_prompt = """You are an expert tutor in technology and programming. 
Your role is to provide clear and structured explanations in Markdown format about:
- Programming concepts and best practices.
- Code snippets provided by the user, including their functionality and possible optimizations.
- General technology topics, including AI, software development, networking, hardware, and emerging technologies.
- Comparisons between technologies, frameworks, or programming paradigms.
- Recommendations on tools, best practices, and industry trends.

You have access to various tools to help provide better assistance:
- get_terraform_guide: Get a comprehensive guide for Terraform setup and usage
- get_github_trending_repos: Get trending GitHub repositories for any technical topic, helping users discover popular and relevant projects

Your responses must be **structured, educational, and formatted in Markdown**. 
Use headings, bullet points, code blocks, and bold/italic text where appropriate."""

# Generate User Prompt
def user_prompt_for(query, is_code=False, language="a programming language"):
    if is_code:
        return f"I will provide you with a {language} code snippet. Explain it in Markdown.\n```{language}\n{query}\n```"
    return f"**Question:** {query}\n\nPlease respond in Markdown format."

# Generate Messages for OpenAI/Ollama
def messages_for(query, is_code=False, language="a programming language"):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(query, is_code, language)}
    ]

# Get OpenAI Response
def get_explanation_openai(query, is_code, language, model=MODEL_GPT):
    """Generates an explanation using OpenAI models."""
    response = openai.chat.completions.create(
        model=model,
        messages=messages_for(query, is_code, language),
        tools=tools,
        tool_choice="auto"
    )
    
    # Handle tool calls if any
    if response.choices[0].message.tool_calls:
        tool_messages, tool_result = handle_tool_calls(response.choices[0].message.tool_calls)
        
        # Add tool results to the conversation
        messages = messages_for(query, is_code, language)
        messages.append(response.choices[0].message)
        messages.extend(tool_messages)
        
        # Get final response
        final_response = openai.chat.completions.create(
            model=model,
            messages=messages
        )
        return final_response.choices[0].message.content
    
    return response.choices[0].message.content

# Get Llama Response
def get_explanation_ollama(query, is_code, language, model=MODEL_LLAMA):
    """Generates an explanation using the Llama model (Ollama)."""
    response = ollama.chat(model=model, messages=messages_for(query, is_code, language))
    return response['message']['content']

# Get Claude Response
def get_explanation_claude(query, is_code, language, model=MODEL_CLAUDE):
    """Generates an explanation using Anthropic Claude."""
    user_content = user_prompt_for(query, is_code, language)
    
    response = anthropic_client.messages.create(
        model=model,
        max_tokens=4000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_content}
        ]
    )
    
    return response.content[0].text

# Generate explanation based on selected model
def generate_explanation(query, is_code, language, model_choice):
    """
    Generate explanation based on the selected model
    
    Args:
        query (str): User query or code
        is_code (bool): Whether the query is code
        language (str): Programming language or natural language
        model_choice (str): Model to use (openai, ollama, claude)
        
    Returns:
        str: Generated explanation
    """
    if model_choice == "openai":
        return get_explanation_openai(query, is_code, language)
    elif model_choice == "ollama":
        return get_explanation_ollama(query, is_code, language)
    elif model_choice == "claude":
        return get_explanation_claude(query, is_code, language)
    else:
        raise ValueError(f"Unsupported model choice: {model_choice}") 