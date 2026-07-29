"""
Application configuration
"""

APP_NAME = "Enterprise RAG Chatbot"

APP_VERSION = "1.0.0"

import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

EMBEDDING_MODEL = "text-embedding-004"

LLM_MODEL = "gemini-2.5-flash"