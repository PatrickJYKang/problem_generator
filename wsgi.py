from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Make sure API_KEY is available
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("Missing API_KEY environment variable. Check your .env file.")

# Import app after loading environment variables
from app import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
