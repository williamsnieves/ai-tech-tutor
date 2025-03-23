# 🤖 AI Tech Tutor (Gradio UI)

This is a Gradio-based web interface for the AI Tech Tutor, providing explanations for programming concepts and code snippets.

## ✨ Features

- **Gradio-based UI** for easy interaction
- **Multiple AI model support**:
  - OpenAI (GPT-4o-mini)
  - Ollama (Llama 3.2)
  - Anthropic (Claude 3.5 Sonnet)
- **Translation support** for Spanish (using Claude 3.5 Sonnet)
- **Code explanation** with syntax highlighting
- **Example queries** for quick testing

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key
- Anthropic API key
- Ollama running locally (for Llama model)

### Setup

1. **Create and activate a virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Add your API keys to the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ANTHROPIC_API_KEY=your_anthropic_api_key_here
     ```

### Running the App

Run the Gradio app:
```sh
python gradio_app.py
```

This will start a local web server, typically at http://127.0.0.1:7860/

## 🧠 Usage

1. **Enter a question or code snippet** in the input box
2. If entering code, **check "Is this code?"** and select the programming language
3. **Choose an AI model** (OpenAI, Ollama, or Claude)
4. **Select output language** (English or Spanish)
5. Click **"Get Explanation"**

## 📝 Example Queries

- "What is a closure in JavaScript?"
- "Explain how Docker containers work"
- "How does async/await work in Python?"
- Paste code snippets for detailed explanations 