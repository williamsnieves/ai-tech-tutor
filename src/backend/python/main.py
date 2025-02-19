from tutor import get_explanation, get_explanation_ollama

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
