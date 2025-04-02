# Load environment variables first - before importing the app
import os
import sys
from dotenv import load_dotenv

# Get the absolute path to the directory containing this file
base_dir = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env file
env_path = os.path.join(base_dir, '.env')
load_dotenv(env_path)

# Check if the API key is loaded
api_key = os.environ.get('API_KEY')
if not api_key:
    print(f"WARNING: API_KEY not found in environment variables after loading {env_path}", file=sys.stderr)
    # Try to read the file directly and set the environment variable
    try:
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.strip().startswith('API_KEY='):
                        key = line.strip().split('=', 1)[1].strip()
                        if key:
                            os.environ['API_KEY'] = key
                            print(f"API_KEY manually set from .env file", file=sys.stderr)
    except Exception as e:
        print(f"Error manually loading API_KEY: {str(e)}", file=sys.stderr)

# Now import the app after environment variables are set
from app import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
