import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

# Model names
GEMINI_PRO_MODEL = "gemini-2.5-flash-preview-05-20"
GEMINI_FLASH_MODEL = "gemini-2.5-flash-preview-05-20"

# Output folder for generated files
OUTPUT_FOLDER = os.path.join(os.getcwd(), "output")

# Testing mode - set to True to use mock responses instead of API calls
USE_MOCK_RESPONSES = os.getenv("USE_MOCK_RESPONSES", "False").lower() == "true"


