import os
import gradio as gr
from src.backend.synthetic_data.core.generator import DataGenerator
from src.backend.synthetic_data.config.settings import (
    MODEL_GPT,
    MODEL_CLAUDE,
    HUGGINGFACE_MODELS,
    DEFAULT_NUM_SAMPLES,
    DEFAULT_MAX_TOKENS
)
import json
import pyperclip

def process_query(
    data_type: str,
    model: str,
    sample_size: int,
    max_tokens: int
) -> tuple[str, str, str]:
    """Process the query and generate synthetic data."""
    try:
        generator = DataGenerator()
        result = generator.generate_data(
            data_type=data_type,
            model=model,
            sample_size=sample_size,
            max_tokens=max_tokens
        )
        
        if result["error"]:
            return f"❌ Error: {result['message']}", "", ""
        
        # Format the data for display
        formatted_data = json.dumps(result["data"], indent=2)
        
        # Get the file path
        filepath = result.get("filepath", "")
        if filepath and os.path.exists(filepath):
            return "✅ Success", formatted_data, filepath
        else:
            return "✅ Success", formatted_data, "No file was saved"
            
    except Exception as e:
        return f"❌ Error: {str(e)}", "", ""

def copy_to_clipboard(text: str) -> str:
    """Copy text to clipboard and return a message."""
    try:
        pyperclip.copy(text)
        return "✅ Copied to clipboard!"
    except Exception as e:
        return f"❌ Failed to copy: {str(e)}"

def main():
    """Run the Gradio interface."""
    # Define available models
    available_models = [MODEL_GPT, MODEL_CLAUDE] + list(HUGGINGFACE_MODELS.keys())
    
    # Create the interface
    with gr.Blocks(title="Synthetic Data Generator") as app:
        gr.Markdown("# 🎲 Synthetic Data Generator")
        gr.Markdown("Generate realistic synthetic data using various LLM models")
        
        with gr.Row():
            with gr.Column():
                data_type = gr.Dropdown(
                    choices=["business", "health", "e-commerce"],
                    label="Data Type",
                    value="business"
                )
                model = gr.Dropdown(
                    choices=available_models,
                    label="Model",
                    value=MODEL_GPT
                )
                sample_size = gr.Slider(
                    minimum=1,
                    maximum=100,
                    value=DEFAULT_NUM_SAMPLES,
                    step=1,
                    label="Sample Size"
                )
                max_tokens = gr.Slider(
                    minimum=100,
                    maximum=4000,
                    value=DEFAULT_MAX_TOKENS,
                    step=100,
                    label="Max Tokens"
                )
                generate_btn = gr.Button("Generate Data")
            
            with gr.Column():
                status = gr.Textbox(label="Status", interactive=False)
                output = gr.Textbox(
                    label="Generated Data",
                    lines=10,
                    interactive=False
                )
                filepath = gr.Textbox(
                    label="File Path",
                    interactive=False
                )
                copy_btn = gr.Button("📋 Copy Generated Data", variant="primary")
        
        # Set up the event handlers
        generate_btn.click(
            fn=process_query,
            inputs=[data_type, model, sample_size, max_tokens],
            outputs=[status, output, filepath]
        )
        
        copy_btn.click(
            fn=copy_to_clipboard,
            inputs=[output],
            outputs=[status]
        )
    
    # Launch the app
    app.launch(share=True)

if __name__ == "__main__":
    main() 