import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(override=True)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("hi")
    print(f"Success: {response.text}")
except Exception as e:
    print(f"Error: {e}")
