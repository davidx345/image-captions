"""
Configuration file for Image Captioning Project (using Gemini API)
"""

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data') # For storing any local images you want to caption
# RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw') # If you still plan to download images
# PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed') # Likely not needed for Gemini
NOTEBOOKS_DIR = os.path.join(PROJECT_ROOT, 'notebooks')

# Gemini API Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Image settings (if you want to standardize before sending to API, though Gemini is flexible)
IMAGE_MAX_SIZE = (1024, 1024) # Optional: resize images before sending

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
# os.makedirs(RAW_DATA_DIR, exist_ok=True)

# print(f"Project Root: {PROJECT_ROOT}") # Optional: for debugging
# if GEMINI_API_KEY:
#     print("Gemini API Key loaded successfully.") # Optional: for debugging
# else:
#     print("Error: Gemini API Key not found. Make sure it's set in your .env file.") # Optional: for debugging
