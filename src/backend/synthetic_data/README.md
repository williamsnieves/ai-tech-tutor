# Synthetic Data Generator with LLMs

This project implements a synthetic data generator using different language models (LLMs) such as GPT, Claude, and Llama. It allows generating realistic data in various formats (JSON, CSV, Parquet) for different domains like business, healthcare, and e-commerce.

## Features

- 🎯 Generation of realistic synthetic data
- 🤖 Support for multiple LLM models:
  - OpenAI GPT
  - Anthropic Claude
  - Meta Llama
- 📊 Output formats:
  - JSON
  - CSV
  - Parquet
- 🏗️ Supported data types:
  - Business data
  - Healthcare data
  - E-commerce data
- 🎨 Intuitive graphical interface with Gradio

## Project Structure

```
synthetic_data/
├── api/                 # API clients for different LLMs
├── config/             # Configuration and constants
├── core/               # Core generator logic
├── ui/                 # Gradio user interface
├── utils/              # Utilities and helper functions
├── main.py            # Application entry point
├── requirements.txt   # Project dependencies
└── README.md          # Documentation
```

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone [REPOSITORY_URL]
cd synthetic_data
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python main.py
```

2. Access the web interface:
- The application will be available at `http://localhost:7860`
- Select the type of data to generate
- Choose the LLM model
- Configure the number of samples and tokens
- Select the output format
- Click "Generate Data"

## Configuration

The `config/settings.py` file contains the main configurations:
- Available models
- Supported data types
- Output formats
- Default values

## Contributing

Contributions are welcome. Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 