"""
Gemini LLM Integration
 
This module is responsible for communicating with the
Google Gemini model and generating answers.
"""
 
import google.generativeai as genai
from app.config import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini Model
model = genai.GenerativeModel("gemini-flash-latest")

 
def ask_gemini(prompt: str) -> str:
    """
    Send prompt to Gemini and return response text.
 
    Parameters:
        prompt : Prompt containing context and user question
 
    Returns:
        Generated answer
    """
 
    response = model.generate_content(prompt)
 
    return response.text