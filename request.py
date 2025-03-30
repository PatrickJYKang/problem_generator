import requests
import json
import sys
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access the API key
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("Missing API_KEY. Set it in the .env file.")

BASE_URL = "http://47.251.117.165/v1"

def upload_file(file_path, user):
    """ Uploads a file to the API and returns the file ID. """
    upload_url = f"{BASE_URL}/files/upload"
    headers = { "Authorization": f"Bearer {API_KEY}" }
    
    try:
        # print("Uploading file...")
        with open(file_path, 'rb') as file:
            files = { 'file': (file_path, file, 'text/plain') }
            data = { "user": user, "type": "document" }
            response = requests.post(upload_url, headers=headers, files=files, data=data)
            if response.status_code == 201:
                return response.json().get("id")
            else:
                print(f"File upload failed: {response.text}")
                return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def run_workflow(inputs, response_mode, user):
    """ Calls the workflow API. """
    url = f"{BASE_URL}/workflows/run"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "inputs": inputs,
        "response_mode": response_mode,
        "user": user
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json() if response.status_code == 200 else {"error": response.text}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing course or lesson"}))
        sys.exit(1)

    course = sys.argv[1]
    lesson = sys.argv[2]
    user = "testuser"
    file_path = "sololearn_intro_python.txt"

    file_id = upload_file(file_path, user)

    if file_id:
        inputs = {
            "Course": course,
            "CurrentLesson": lesson,
            "syllabus": {
                "transfer_method": "local_file",
                "upload_file_id": file_id,
                "type": "document"
            }
        }
        response = run_workflow(inputs, "blocking", user)
        print(json.dumps(response, indent=4))
    else:
        print(json.dumps({"error": "File upload failed"}))