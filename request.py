import requests
import json
import sys
import os
import tempfile
from dotenv import load_dotenv
from github_utils import GitHubFetcher

# Define debug_print function globally
def debug_print(*args, **kwargs):
    """Print debug messages to stderr"""
    print(*args, file=sys.stderr, **kwargs)

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
        debug_print(f"Uploading file: {file_path}")
        if not os.path.exists(file_path):
            debug_print(f"Error: File not found: {file_path}")
            return None
            
        with open(file_path, 'rb') as file:
            files = { 'file': (os.path.basename(file_path), file, 'text/plain') }
            data = { "user": user, "type": "document" }
            
            debug_print(f"Making API request to: {upload_url}")
            response = requests.post(upload_url, headers=headers, files=files, data=data)
            
            debug_print(f"Response status: {response.status_code}")
            if response.status_code == 201:
                file_id = response.json().get("id")
                debug_print(f"File uploaded successfully, ID: {file_id}")
                return file_id
            else:
                debug_print(f"File upload failed: {response.text}")
                return None
    except Exception as e:
        debug_print(f"Error during file upload: {str(e)}")
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
        debug_print(f"Making workflow API request to: {url}")
        debug_print(f"Request data: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, headers=headers, json=data)
        
        debug_print(f"Workflow response status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            debug_print("Workflow API call successful")
            return result
        else:
            error_msg = f"Workflow API error: {response.text}"
            debug_print(error_msg)
            return {"error": response.text}
    except Exception as e:
        error_msg = f"Exception during workflow API call: {str(e)}"
        debug_print(error_msg)
        return {"error": error_msg}

def build_syllabus(lesson, language="learnpython.org", lang="en"):
    """ Builds a syllabus from GitHub markdown files up to and including the current lesson. """
    try:
        debug_print(f"Fetching syllabus from GitHub for lesson: {lesson}")
        github_fetcher = GitHubFetcher()
        
        # Build the syllabus using the GitHub fetcher
        syllabus_path = github_fetcher.build_syllabus(lesson, language, lang)
        
        if not syllabus_path:
            print(json.dumps({"error": "Failed to build syllabus from GitHub"}), file=sys.stderr)
            return None
            
        debug_print(f"Successfully built syllabus from GitHub: {syllabus_path}")
        return syllabus_path
    except Exception as e:
        print(json.dumps({"error": f"Failed to build syllabus: {str(e)}"}), file=sys.stderr)
        return None

if __name__ == "__main__":
    # Use stderr for debug messages so they don't interfere with JSON output
    import sys
    
    def debug_print(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
    
    debug_print("Starting request.py script")
    
    if len(sys.argv) < 3:
        error_msg = {"error": "Missing course or lesson"}
        print(json.dumps(error_msg))
        sys.exit(1)

    course = sys.argv[1]
    lesson = sys.argv[2]
    user = "testuser"
    
    debug_print(f"Course: {course}, Lesson: {lesson}")
    
    # Build a dynamic syllabus based on the current lesson
    debug_print("Building dynamic syllabus...")
    file_path = build_syllabus(lesson)
    if not file_path:
        error_msg = {"error": "Failed to build syllabus"}
        print(json.dumps(error_msg))
        sys.exit(1)
    
    debug_print(f"Syllabus built successfully: {file_path}")
    
    # Upload the syllabus file
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
        
        debug_print("Calling workflow API...")
        response = run_workflow(inputs, "blocking", user)
        
        # Check for errors in the response
        if "error" in response:
            debug_print(f"Error in workflow response: {response['error']}")
            print(json.dumps({"error": f"Workflow API error: {response['error']}"})) 
        else:
            debug_print("Workflow completed successfully")
            # Only print the JSON response to stdout, with no other text
            print(json.dumps(response))
    else:
        error_msg = {"error": "File upload failed"}
        print(json.dumps(error_msg))
    
    # Clean up the temporary file
    if file_path and os.path.exists(file_path):
        try:
            debug_print(f"Cleaning up temporary file: {file_path}")
            os.unlink(file_path)
            debug_print("Temporary file deleted successfully")
        except Exception as e:
            debug_print(f"Failed to delete temporary file: {str(e)}")