from synthetic_data.api.huggingface_client import HuggingFaceClient
from synthetic_data.config.settings import HUGGINGFACE_MODELS, MODEL_LLAMA

def test_llama_model():
    """Test the Llama model with a simple greeting."""
    client = HuggingFaceClient()
    
    try:
        print(f"\n=== Testing Llama model: {MODEL_LLAMA} ===")
        response = client.test_model("llama")  # Use the key from HUGGINGFACE_MODELS
        print(f"Response from Llama: {response}")
    except Exception as e:
        print(f"Failed to test Llama model: {str(e)}")
        import traceback
        print(f"Traceback:\n{traceback.format_exc()}")

def test_all_models():
    """Test all available open-source models with a simple greeting."""
    client = HuggingFaceClient()
    
    print("\nAvailable models:", list(HUGGINGFACE_MODELS.keys()))
    
    for model_name in HUGGINGFACE_MODELS.keys():
        try:
            print(f"\n=== Testing model: {model_name} ===")
            print(f"Model ID: {HUGGINGFACE_MODELS[model_name]}")
            response = client.test_model(model_name)
            print(f"Response from {model_name}: {response}")
        except Exception as e:
            print(f"Failed to test {model_name}: {str(e)}")
            import traceback
            print(f"Traceback:\n{traceback.format_exc()}")
            continue

if __name__ == "__main__":
    # First test Llama specifically
    test_llama_model()
    
    # Then test all models
    test_all_models() 