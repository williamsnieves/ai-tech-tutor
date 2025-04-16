import os
import gradio as gr
from typing import Dict, Any
from src.backend.synthetic_data.core.generator import DataGenerator
from src.backend.synthetic_data.config.settings import (
    DATA_TYPES,
    OUTPUT_FORMATS,
    MODEL_GPT,
    MODEL_CLAUDE,
    MODEL_LLAMA,
    MODEL_PHI3,
    MODEL_GEMMA,
    MODEL_DEEPSEEK,
    DEFAULT_NUM_SAMPLES,
    DEFAULT_MAX_TOKENS
)
import json
from datetime import datetime

# Initialize the data generator
generator = DataGenerator()

# Language options
LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German"
}

def process_query(
    data_type: str,
    model: str,
    num_samples: int,
    output_format: str,
    max_tokens: int,
    language: str
) -> tuple[str, str, str]:
    """Process the user query and generate synthetic data."""
    try:
        result = generator.generate(
            data_type=data_type,
            model=model,
            num_samples=num_samples,
            output_format=output_format,
            max_tokens=max_tokens,
            language=language
        )
        
        if result["status"] == "success":
            # Format the data for display
            formatted_data = json.dumps(result["data"], indent=2)
            return (
                f"✅ {result['message']}",
                formatted_data,
                result["filepath"]
            )
        else:
            return (
                f"❌ {result['message']}",
                "",
                ""
            )
            
    except Exception as e:
        return (
            f"❌ Error: {str(e)}",
            "",
            ""
        )

def create_interface() -> gr.Blocks:
    """Create the Gradio interface."""
    with gr.Blocks(title="Synthetic Data Generator") as interface:
        gr.Markdown("# 🎲 Synthetic Data Generator")
        gr.Markdown("Generate realistic synthetic data using various LLM models")
        
        with gr.Row():
            with gr.Column():
                data_type = gr.Dropdown(
                    choices=list(DATA_TYPES.keys()),
                    label="Data Type",
                    value=list(DATA_TYPES.keys())[0]
                )
                
                model = gr.Dropdown(
                    choices=[MODEL_GPT, MODEL_CLAUDE, MODEL_LLAMA, MODEL_PHI3, MODEL_GEMMA, MODEL_DEEPSEEK],
                    label="Model",
                    value=MODEL_GPT
                )
                
                language = gr.Dropdown(
                    choices=list(LANGUAGES.keys()),
                    label="Language",
                    value="en"
                )
                
                num_samples = gr.Number(
                    label="Number of Samples",
                    value=DEFAULT_NUM_SAMPLES,
                    minimum=1,
                    maximum=1000
                )
                
                output_format = gr.Dropdown(
                    choices=list(OUTPUT_FORMATS.keys()),
                    label="Output Format",
                    value="json"
                )
                
                max_tokens = gr.Number(
                    label="Max Tokens",
                    value=DEFAULT_MAX_TOKENS,
                    minimum=100,
                    maximum=4000
                )
                
                generate_btn = gr.Button("Generate Data")
            
            with gr.Column():
                status = gr.Textbox(label="Status", interactive=False)
                output = gr.Textbox(
                    label="Generated Data",
                    lines=20,
                    max_lines=20,
                    interactive=True
                )
                filepath = gr.Textbox(label="Saved File", interactive=False)
                
                # Add copy button with proper implementation
                copy_btn = gr.Button("Copy to Clipboard")
                copy_btn.click(
                    fn=lambda x: x,
                    inputs=[output],
                    outputs=[],
                    js="""
                    function(text) {
                        navigator.clipboard.writeText(text);
                        return [];
                    }
                    """
                )
        
        # Add examples
        gr.Examples(
            examples=[
                ["business", MODEL_GPT, 10, "json", 1000, "en"],
                ["health", MODEL_CLAUDE, 50, "csv", 2000, "es"],
                ["ecommerce", MODEL_LLAMA, 100, "parquet", 4000, "fr"],
                ["business", MODEL_DEEPSEEK, 10, "json", 1000, "en"]
            ],
            inputs=[data_type, model, num_samples, output_format, max_tokens, language],
            outputs=[status, output, filepath],
            fn=process_query,
            cache_examples=True
        )
        
        generate_btn.click(
            fn=process_query,
            inputs=[data_type, model, num_samples, output_format, max_tokens, language],
            outputs=[status, output, filepath]
        )
    
    return interface

def launch_app():
    """Launch the Gradio app."""
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", 7860)),
        share=True
    ) 