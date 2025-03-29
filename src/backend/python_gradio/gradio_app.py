import gradio as gr
from tutor import generate_explanation
from utils import translate_text
from config import ANTHROPIC_API_KEY, LANGUAGES

def process_input(query, is_code, code_language, model_choice, output_language):
    """
    Process user input and generate response
    
    Args:
        query (str): User query or code
        is_code (bool): Whether the query is code
        code_language (str): Programming language if is_code is True
        model_choice (str): AI model to use
        output_language (str): Output language
        
    Returns:
        str: Generated response
    """
    language = code_language if is_code else "English"
    
    # Generate explanation using selected model
    response = generate_explanation(query, is_code, language, model_choice)
    
    # Translate if needed
    if output_language != "English":
        response = translate_text(
            response, 
            output_language, 
            api_key=ANTHROPIC_API_KEY
        )
    
    return response

# Create Gradio interface
def create_interface():
    with gr.Blocks(title="AI Tech Tutor", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🤖 AI Tech Tutor")
        gr.Markdown("Get AI-powered explanations for code and technical concepts")
        
        with gr.Row():
            with gr.Column(scale=2):
                # Input components
                query_input = gr.Textbox(
                    label="Question or Code",
                    placeholder="Enter your question or paste code here...",
                    lines=10
                )
                
                with gr.Row():
                    is_code_checkbox = gr.Checkbox(label="Is this code?", value=False)
                    code_language = gr.Dropdown(
                        label="Language",
                        choices=["Python", "JavaScript", "TypeScript", "Java", "C++", "Go", "Rust", "SQL", "HTML/CSS", "Other"],
                        value="Python",
                        interactive=True,
                        visible=False
                    )
                
                # Model selection
                model_choice = gr.Radio(
                    label="Select AI Model",
                    choices=["openai", "ollama", "claude"],
                    value="openai"
                )
                
                # Output language selection
                output_language = gr.Dropdown(
                    label="Output Language",
                    choices=LANGUAGES,
                    value="English"
                )
                
                submit_btn = gr.Button("Get Explanation", variant="primary")
            
            with gr.Column(scale=3):
                # Output component
                output = gr.Markdown(label="Explanation")
        
        # Set up interactions
        is_code_checkbox.change(
            fn=lambda x: gr.update(visible=x),
            inputs=is_code_checkbox,
            outputs=code_language
        )
        
        submit_btn.click(
            fn=process_input,
            inputs=[query_input, is_code_checkbox, code_language, model_choice, output_language],
            outputs=output
        )
        
        # Examples
        gr.Examples(
            [
                ["What is a closure in JavaScript?", False, "JavaScript", "openai", "English"],
                ["How does Docker work?", False, "Python", "claude", "English"],
                ["async function fetchData() {\n  try {\n    const response = await fetch('https://api.example.com/data');\n    const data = await response.json();\n    return data;\n  } catch (error) {\n    console.error('Error fetching data:', error);\n    return null;\n  }\n}", True, "JavaScript", "openai", "English"],
                ["def fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n        return fibonacci(n-1) + fibonacci(n-2)", True, "Python", "claude", "English"],
            ],
            inputs=[query_input, is_code_checkbox, code_language, model_choice, output_language]
        )
    
    return demo

# Run the app if executed directly
if __name__ == "__main__":
    demo = create_interface()
    demo.launch(share=True) 