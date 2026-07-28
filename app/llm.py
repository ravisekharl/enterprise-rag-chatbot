"""
Gemini LLM Integration
 
This module is responsible for communicating with the
Google Gemini model and generating answers.
"""
 
import os
import google.generativeai as genai
from app.config import GEMINI_API_KEY
 
# Configure Gemini only once
genai.configure(api_key=GEMINI_API_KEY)
 
# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")
 
 
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