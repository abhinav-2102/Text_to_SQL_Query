import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: API Key not found. Check your .env file.")
else:
    genai.configure(api_key=api_key)

    print("Checking available models for your API key...")
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
                available_models.append(m.name)
        
        if not available_models:
            print("\nCRITICAL: No models found. Please enable 'Generative Language API' in Google Cloud Console.")
    except Exception as e:
        print(f"Error connecting to Google: {e}")