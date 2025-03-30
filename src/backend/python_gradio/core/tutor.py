from typing import Dict, Any, Optional, List
from rich.console import Console
from anthropic import Anthropic
from openai import OpenAI
import ollama
from config.settings import OPENAI_API_KEY, ANTHROPIC_API_KEY, MODEL_GPT, MODEL_LLAMA, MODEL_CLAUDE
from utils.helpers import handle_api_error, translate_text, text_to_speech
from core.tools import tools, handle_tool_calls, get_terraform_guide, get_github_trending_repos

console = Console()

# System Prompt
SYSTEM_PROMPT = """You are an expert tutor in technology and programming. 
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

class TechTutor:
    def __init__(self):
        self.tools = tools
        self.console = Console()
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        self.anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)

    def _get_terraform_guide(self, topic: str = "basic") -> str:
        """Get Terraform guide for a specific topic"""
        try:
            return get_terraform_guide()
        except Exception as e:
            error = handle_api_error(e, "Terraform Guide")
            return f"Error: {error['error']}\nDetails: {error['details']}"

    def _get_github_trending_repos(self, topic: str, days: int = 7, limit: int = 5) -> str:
        """Get trending GitHub repositories for a topic"""
        try:
            return get_github_trending_repos(topic, days, limit)
        except Exception as e:
            error = handle_api_error(e, "GitHub API")
            return f"Error: {error['error']}\nDetails: {error['details']}"

    def _user_prompt_for(self, query: str, is_code: bool = False, language: str = "a programming language") -> str:
        """Generate user prompt based on query type"""
        if is_code:
            return f"I will provide you with a {language} code snippet. Explain it in Markdown.\n```{language}\n{query}\n```"
        return f"**Question:** {query}\n\nPlease respond in Markdown format."

    def _messages_for(self, query: str, is_code: bool = False, language: str = "a programming language") -> List[Dict[str, str]]:
        """Generate messages for LLM"""
        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": self._user_prompt_for(query, is_code, language)}
        ]

    def process_query(
        self,
        query: str,
        model: str = "claude",
        target_language: Optional[str] = None,
        generate_audio: bool = False
    ) -> Dict[str, Any]:
        """Process a user query and return a response with optional audio"""
        try:
            # Determine if the query is about code
            is_code = any(keyword in query.lower() for keyword in ["code", "programming", "function", "class", "method", "variable"])
            language = "programming"  # Default language
            
            # Try to detect programming language if it's a code query
            if is_code:
                for lang in ["python", "javascript", "java", "c++", "c#", "ruby", "go", "rust", "swift", "kotlin"]:
                    if lang in query.lower():
                        language = lang
                        break
            
            # Generate explanation using the selected model
            response_text = self._generate_explanation(query, is_code, language, model)
            
            # Translate if requested
            if target_language and target_language != "English":
                response_text = translate_text(response_text, target_language, ANTHROPIC_API_KEY)
            
            # Generate audio if requested
            audio_path = None
            if generate_audio:
                audio_path = text_to_speech(response_text)
            
            return {
                "response": response_text,
                "audio_path": audio_path
            }
        except Exception as e:
            error = handle_api_error(e, "Query Processing")
            return {
                "response": f"Error: {error['error']}\nDetails: {error['details']}",
                "audio_path": None
            }

    def _generate_explanation(self, query: str, is_code: bool, language: str, model: str) -> str:
        """Generate an explanation using the specified model"""
        try:
            if model == "openai":
                return self._generate_openai_explanation(query, is_code, language)
            elif model == "claude":
                return self._generate_claude_explanation(query, is_code, language)
            elif model == "ollama":
                return self._generate_ollama_explanation(query, is_code, language)
            else:
                raise ValueError(f"Unsupported model: {model}")
        except Exception as e:
            error = handle_api_error(e, f"{model.title()} API")
            return f"Error: {error['error']}\nDetails: {error['details']}"

    def _generate_openai_explanation(self, query: str, is_code: bool, language: str) -> str:
        """Generate explanation using OpenAI"""
        response = self.openai_client.chat.completions.create(
            model=MODEL_GPT,
            messages=self._messages_for(query, is_code, language),
            tools=self.tools,
            tool_choice="auto",
            temperature=0.7,
            max_tokens=2000
        )
        
        # Handle tool calls if present
        message = response.choices[0].message
        if message.tool_calls:
            # Process tool calls
            tool_messages, result = handle_tool_calls(message.tool_calls)
            
            # Create a new message with the tool results
            messages = self._messages_for(query, is_code, language)
            messages.append({"role": "assistant", "content": None, "tool_calls": message.tool_calls})
            for tool_message in tool_messages:
                messages.append(tool_message)
            
            # Get final response
            final_response = self.openai_client.chat.completions.create(
                model=MODEL_GPT,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            return final_response.choices[0].message.content
        
        return message.content

    def _generate_claude_explanation(self, query: str, is_code: bool, language: str) -> str:
        """Generate explanation using Claude"""
        response = self.anthropic_client.messages.create(
            model=MODEL_CLAUDE,
            max_tokens=2000,
            temperature=0.7,
            messages=self._messages_for(query, is_code, language)
        )
        
        return response.content[0].text

    def _generate_ollama_explanation(self, query: str, is_code: bool, language: str) -> str:
        """Generate explanation using Ollama"""
        response = ollama.chat(
            model=MODEL_LLAMA,
            messages=self._messages_for(query, is_code, language)
        )
        
        return response['message']['content'] 