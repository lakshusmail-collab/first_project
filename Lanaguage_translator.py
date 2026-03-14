import google.generativeai as genai

# 1. Setup API Key
# Replace with your actual key or use an environment variable
genai.configure(api_key="AIzaSyCFPPK7Ky0wJ2Y4xhPe9BLc8S5fiDf3NLc")

def translate_to_malayalam():
    # Initialize the Gemini 2.5 Flash model
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    print("--- 🌍 Gemini English-to-Malayalam Translator ---")
    english_text = input("Enter the English sentence to translate: ")

    # System-style prompt for better accuracy
    prompt = f"""
    You are a professional translator. 
    Translate the following English text into natural, spoken Malayalam.
    Use the Malayalam script (മലയാളം).
    
    English: "{english_text}"
    Malayalam:"""

    try:
        response = model.generate_content(prompt)
        print("\n" + "="*30)
        print(f"Original: {english_text}")
        print(f"Malayalam: {response.text.strip()}")
        print("="*30)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    translate_to_malayalam()