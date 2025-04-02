import requests
import json
import sys
import os
import tempfile
import re

# Define debug_print function globally
def debug_print(*args, **kwargs):
    """Print debug messages to stderr"""
    print(*args, file=sys.stderr, **kwargs)

# Read API key directly from .env file
def read_env_file():
    # Get the directory containing this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(base_dir, '.env')
    
    debug_print(f"Looking for .env file at: {env_path}")
    
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r') as f:
                env_content = f.read()
                debug_print(f".env file found and read successfully")
                
                # Extract API_KEY using regex
                match = re.search(r'API_KEY\s*=\s*([^\n\r]+)', env_content)
                if match:
                    api_key = match.group(1).strip()
                    debug_print(f"API_KEY found in .env file (length: {len(api_key)})")
                    return api_key
                else:
                    debug_print("API_KEY not found in .env file content")
        except Exception as e:
            debug_print(f"Error reading .env file: {str(e)}")
    else:
        debug_print(f".env file not found at {env_path}")
    
    # Check environment variable as fallback
    api_key = os.environ.get('API_KEY')
    if api_key:
        debug_print(f"API_KEY found in environment variables")
        return api_key
    
    debug_print("No API_KEY found in .env file or environment variables")
    return None

# Get API key
API_KEY = read_env_file()

if not API_KEY:
    raise ValueError("Missing API_KEY. Set it in the .env file or as an environment variable.")

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