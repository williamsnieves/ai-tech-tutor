# 🐍 AI Tech Tutor - Python Backend

This is the **Python backend** for AI Tech Tutor, built with **OpenAI API, Ollama, and Flask** (CLI-based for now).

## 🚀 Getting Started

### 1️⃣ Install Dependencies
```bash
cd src/backend/python
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  (Windows)

```bash
pip install -r requirements.txt
```

### 2️⃣ Set Up API Keys
OPENAI_API_KEY=your-openai-key-here


### 3️⃣ Run the Tutor (CLI)

```bash
python main.py
```

### 📂 Project Structure

python/
│── main.py          # CLI entry point
│── tutor.py         # AI logic
│── config.py        # Environment config
│── utils.py         # Helper functions
│── requirements.txt
│── .env.example     # Sample environment file
