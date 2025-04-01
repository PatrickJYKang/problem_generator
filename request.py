import requests
import json
import sys
import os
import tempfile
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

def build_syllabus(lesson):
    """ Builds a syllabus from markdown files up to and including the current lesson. """
    # Path to the index.json file
    index_path = os.path.join("syllabi", "python", "index.json")
    
    # Path to the markdown files directory
    md_dir = os.path.join("syllabi", "python")
    
    # Load the index.json file
    try:
        with open(index_path, 'r') as f:
            index = json.load(f)
    except Exception as e:
        print(json.dumps({"error": f"Failed to load index.json: {str(e)}"}), file=sys.stderr)
        return None
    
    # Find all lessons in order (combine basics and advanced)
    all_lessons = []
    for category in ["basics", "advanced"]:
        if category in index:
            all_lessons.extend(list(index[category].keys()))
    
    # Find the position of the current lesson
    try:
        lesson_index = all_lessons.index(lesson)
    except ValueError:
        print(json.dumps({"error": f"Lesson '{lesson}' not found in index.json"}), file=sys.stderr)
        return None
    
    # Get all lessons up to and including the current lesson
    lessons_to_include = all_lessons[:lesson_index + 1]
    
    # Create a temporary file to store the concatenated markdown
    temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.md')
    
    try:
        # Add a welcome message at the beginning if it exists
        welcome_path = os.path.join(md_dir, "Welcome.md")
        if os.path.exists(welcome_path):
            with open(welcome_path, 'r') as f:
                temp_file.write(f.read() + "\n\n")
        
        # Concatenate all markdown files in order
        for lesson_name in lessons_to_include:
            md_path = os.path.join(md_dir, f"{lesson_name}.md")
            if os.path.exists(md_path):
                with open(md_path, 'r') as f:
                    temp_file.write(f"# {lesson_name}\n\n")
                    temp_file.write(f.read() + "\n\n")
            else:
                print(json.dumps({"warning": f"Markdown file for lesson '{lesson_name}' not found"}), file=sys.stderr)
        
        temp_file.close()
        return temp_file.name
    except Exception as e:
        print(json.dumps({"error": f"Failed to build syllabus: {str(e)}"}), file=sys.stderr)
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing course or lesson"}))
        sys.exit(1)

    course = sys.argv[1]
    lesson = sys.argv[2]
    user = "testuser"
    
    # Build a dynamic syllabus based on the current lesson
    file_path = build_syllabus(lesson)
    if not file_path:
        print(json.dumps({"error": "Failed to build syllabus"}))
        sys.exit(1)
    
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
    
    # Clean up the temporary file
    if file_path and os.path.exists(file_path):
        try:
            os.unlink(file_path)
        except Exception as e:
            print(json.dumps({"warning": f"Failed to delete temporary file: {str(e)}"}), file=sys.stderr)