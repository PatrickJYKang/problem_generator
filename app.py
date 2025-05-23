from flask import Flask, request, jsonify, send_from_directory
import json
import os
import subprocess
import db  # Import the database module
from github_utils import GitHubFetcher  # Import GitHub fetcher
from dotenv import load_dotenv
import chatbot  # Import the chatbot module
from style_check import check_style, format_cpp_code, format_java_code  # Import the style checking module

# Load environment variables from .env file
load_dotenv()

# Get API keys and URLs from environment variables
PROBLEM_GENERATOR_API_KEY = os.getenv('PROBLEM_GENERATOR_API_KEY', 'app-NxALjP6yItovyBLW2UZJIxcJ')
PROBLEM_GENERATOR_API_URL = os.getenv('PROBLEM_GENERATOR_API_URL', 'http://47.251.117.165/v1/workflows/run')

app = Flask(__name__, static_folder='static')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/syllabi/<path:filename>')
def serve_syllabi(filename):
    """ 
    Fetches syllabus files from GitHub repository or local filesystem.
    This endpoint now acts as a proxy to GitHub content or serves local files for CSA.
    """
    try:
        # Parse the requested path
        path_parts = filename.split('/')
        language = path_parts[0] if len(path_parts) > 0 else 'learnpython.org'
        
        # Special handling for AP CSA course - read from local filesystem
        if language == "csa":
            # Build local filesystem path
            local_path = os.path.join('syllabi', filename)
            
            # Check if the file exists
            if not os.path.exists(local_path):
                print(f"CSA file not found at: {local_path}")
                return jsonify({"error": f"File {filename} not found"}), 404
                
            # Serve the file based on its extension
            if filename.endswith('.json'):
                with open(local_path, 'r') as f:
                    content = json.load(f)
                return jsonify(content)
            elif filename.endswith('.md'):
                with open(local_path, 'r') as f:
                    content = f.read()
                return content, 200, {'Content-Type': 'text/markdown'}
            else:
                return send_from_directory('syllabi', filename)
        
        # For non-CSA courses, use GitHub fetcher
        github_fetcher = GitHubFetcher()
        
        # Handle index.json separately as it's needed for lesson navigation
        if path_parts[-1] == 'index.json':
            # Determine language and locale from path
            lang = path_parts[1] if len(path_parts) > 1 else 'en'
            repo_path = f"tutorials/{language}/{lang}/index.json"
            
            try:
                content = github_fetcher.get_file_content(repo_path)
                return jsonify(json.loads(content))
            except Exception as e:
                print(f"Error fetching index.json: {str(e)}")
                return jsonify({"error": "Failed to fetch index.json"}), 404
        
        # For all other files, get the full path in the repo
        try:
            # Construct repository path
            repo_path = f"tutorials/{filename}"
            content = github_fetcher.get_file_content(repo_path)
            
            # Determine content type based on file extension
            if filename.endswith('.json'):
                return jsonify(json.loads(content))
            elif filename.endswith('.md'):
                return content, 200, {'Content-Type': 'text/markdown'}
            else:
                return content
        except Exception as e:
            print(f"Error fetching file {filename}: {str(e)}")
            return jsonify({"error": f"Failed to fetch {filename}"}), 404
    except Exception as e:
        print(f"General error in serve_syllabi: {str(e)}")
        return jsonify({"error": "An error occurred"}), 500

@app.route('/github/lessons', methods=['GET'])
def get_lessons():
    """ 
    Gets the list of available lessons from GitHub repository or local filesystem.
    This helps the frontend to populate the lesson dropdown.
    """
    try:
        language = request.args.get('language', 'learnpython.org')
        lang = request.args.get('lang', 'en')
        
        print(f"Request for lessons: language={language}, lang={lang}")
        
        # Special handling for AP CSA course - read from local filesystem
        if language == "csa":
            # Path to local csa index.json
            csa_index_path = os.path.join('syllabi', 'csa', 'index.json')
            try:
                if os.path.exists(csa_index_path):
                    print(f"Loading CSA lessons from local file: {csa_index_path}")
                    with open(csa_index_path, 'r') as f:
                        lessons = json.load(f)
                    print(f"Returning CSA lessons with units: {list(lessons.keys())}")
                    return jsonify(lessons)
                else:
                    print(f"CSA index file not found at: {csa_index_path}")
                    return jsonify({"error": "CSA course content not found"}), 404
            except Exception as e:
                print(f"Error reading CSA index file: {str(e)}")
                return jsonify({"error": f"Failed to read CSA index: {str(e)}"}), 500
        
        # For other courses, use GitHub fetcher
        github_fetcher = GitHubFetcher()
        lessons = github_fetcher.get_lessons(language, lang)
        
        print(f"Returning lessons with categories: {list(lessons.keys())}")
        return jsonify(lessons)
    except Exception as e:
        import traceback
        print(f"Error fetching lessons: {str(e)}")
        traceback.print_exc()
        
        # Return a fallback structure with basic lessons
        fallback = {
            "basics": {
                "Hello, World!": "Hello, World!",
                "Variables and Types": "Variables and Types",
                "Lists": "Lists",
                "Basic Operators": "Basic Operators",
                "Conditions": "Conditions"
            },
            "advanced": {
                "Functions": "Functions",
                "Classes and Objects": "Classes and Objects",
                "Dictionaries": "Dictionaries"
            }
        }
        
        # Return fallback structure but with a 200 status to allow frontend to continue
        return jsonify(fallback)

@app.route('/generate', methods=['POST'])
def generate():
    """ Handles problem generation and extracts test cases """
    data = request.get_json()
    course = data.get("course", "learnpython.org")
    lesson = data.get("lesson", "")
    # Get the language parameter, defaulting to None so request.py can set the appropriate default
    language = data.get("language", None)
    
    if not lesson:
        return jsonify({"error": "Lesson is required."}), 400

    try:
        # Run the request.py subprocess to generate a problem, passing language as additional argument
        cmd = ["python3", "request.py", course, lesson]
        if language:
            cmd.append(language)
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check if there was an error in the subprocess
        if result.returncode != 0:
            print(f"Subprocess error: {result.stderr}")
            return jsonify({"error": f"Error running request.py: {result.stderr}"}), 500
            
        # Check if stdout is empty
        if not result.stdout.strip():
            print(f"Empty response from request.py")
            return jsonify({"error": "No response from API"}), 500
        try:
            # Try to clean the output before parsing
            cleaned_stdout = result.stdout.strip()
            
            # Check if the output starts with any non-JSON characters
            if not cleaned_stdout.startswith('{') and not cleaned_stdout.startswith('['): 
                # Try to find the start of JSON
                json_start = cleaned_stdout.find('{')
                if json_start == -1:
                    json_start = cleaned_stdout.find('[')
                
                if json_start != -1:
                    cleaned_stdout = cleaned_stdout[json_start:]
            
            output = json.loads(cleaned_stdout)

            # Extract test cases if they exist
            raw_testcases = output.get("data", {}).get("outputs", {}).get("Testcases", "").strip()
            
            if not raw_testcases:
                print("No test cases found in API response")
                return jsonify({"error": "Test cases not found in API response."}), 500
                
            # Parse the JSON test cases
            try:
                # Remove any markdown code block markers if present
                clean_testcases = raw_testcases.replace("```json", "").replace("```", "").strip()
                
                try:
                    # Parse the JSON string into a Python object
                    testcases_json = json.loads(clean_testcases)
                    
                    # Ensure we have a list of test cases
                    if not isinstance(testcases_json, list):
                        # Try to find a list in the parsed JSON
                        if isinstance(testcases_json, dict):
                            for key, value in testcases_json.items():
                                if isinstance(value, list):
                                    testcases_json = value
                                    break
                    
                    # Add the parsed test cases to the output
                    output["testcases"] = testcases_json
                    
                    # Store the problem in the database
                    try:
                        title = output.get("data", {}).get("outputs", {}).get("Title", "Untitled Problem")
                        problem_text = output.get("data", {}).get("outputs", {}).get("Problem", "")
                        problem_id = db.store_problem(title, problem_text, course, lesson, testcases_json)
                        output["problem_id"] = problem_id
                    except Exception as e:
                        print(f"Error storing problem in database: {str(e)}")
                        # Continue even if database storage fails
                    
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    # If we can't parse as JSON, return the raw string (for backward compatibility)
                    print("Falling back to raw string format")
                    output["testcases"] = raw_testcases
            except Exception as e:
                print(f"Error processing test cases: {str(e)}")
                # If all else fails, return the raw test cases
                output["testcases"] = raw_testcases
            return jsonify(output)

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return jsonify({"error": "Invalid JSON response", "message": str(e)}), 500
    except Exception as e:
        print(f"Exception in generate endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to generate", "message": str(e)}), 500

@app.route('/run_code', methods=['POST'])
def run_code_endpoint():
    """ Endpoint that runs user-submitted code in the specified language """
    data = request.get_json()
    code = data.get("code", "")
    stdin = data.get("stdin", "")
    language = data.get("language", "python")
    
    # Import the run_code function from run.py
    from run import run_code
    return run_code(code, stdin, language)

# The old parsing functions have been removed as they're no longer needed with JSON test cases

@app.route("/check_code", methods=["POST"])
def check_code_endpoint():
    """ Endpoint that checks user code against test cases """
    data = request.get_json()
    user_code = data.get("code", "").strip()
    client_language = data.get("language", "python")  # Language from the client (editor)
    testcases = data.get("testcases", [])
    problem_id = data.get("problem_id", None)
    
    # When problem_id is provided, we should use the language from the problem
    language = client_language  # Default to language from client
    if problem_id:
        try:
            problem = db.get_problem_by_id(problem_id)
            if problem and problem.get('language'):
                language = problem['language']
                print(f"Using language '{language}' from problem instead of '{client_language}' from editor")
        except Exception as e:
            print(f"Error fetching problem language: {str(e)}")
    
    # Import the check_code function from check.py
    from check import check_code
    result = check_code(user_code, testcases, language)
    
    # Store the solution in the database if problem_id is provided
    if problem_id:
        try:
            # Parse the result to get passed/total testcases
            result_data = json.loads(result.get_data(as_text=True))
            passed = result_data.get("passed", 0)
            total = result_data.get("total", len(testcases))
            
            # Store the solution
            db.store_solution(problem_id, language, user_code, passed, total)
            print(f"Stored solution for problem {problem_id}")
        except Exception as e:
            print(f"Error storing solution in database: {str(e)}")
    
    return result

@app.route("/problems", methods=["GET"])
def get_problems_endpoint():
    """ Get all problems or filter by course/lesson """
    course = request.args.get("course", None)
    lesson = request.args.get("lesson", None)
    
    try:
        # If course and lesson are provided, filter by them
        if course and lesson:
            problems = db.get_problems_by_lesson(course, lesson)
        else:
            # Otherwise get all problems
            limit = request.args.get("limit", 50, type=int)
            problems = db.get_problems(limit)
            
        return jsonify({"problems": problems})
    except Exception as e:
        print(f"Error retrieving problems: {str(e)}")
        return jsonify({"error": "Failed to retrieve problems", "message": str(e)}), 500

@app.route("/problems/<int:problem_id>", methods=["GET"])
def get_problem(problem_id):
    """ Get a specific problem by ID """
    try:
        problem = db.get_problem_by_id(problem_id)
        
        if not problem:
            return jsonify({"error": "Problem not found"}), 404
            
        return jsonify({"problem": problem})
    except Exception as e:
        print(f"Error retrieving problem: {str(e)}")
        return jsonify({"error": "Failed to retrieve problem", "message": str(e)}), 500

@app.route("/problems/<int:problem_id>/solutions", methods=["GET"])
def get_solutions(problem_id):
    """ Get solutions for a specific problem """
    try:
        solutions = db.get_solutions_for_problem(problem_id)
        return jsonify({"solutions": solutions})
    except Exception as e:
        print(f"Error retrieving solutions: {str(e)}")
        return jsonify({"error": "Failed to retrieve solutions", "message": str(e)}), 500

@app.route('/problems/<int:problem_id>', methods=['DELETE'])
def delete_problem(problem_id):
    """ Delete a problem and all associated data """
    try:
        # Call the database function to delete the problem
        success = db.delete_problem(problem_id)
        if success:
            return jsonify({"success": True, "message": f"Problem {problem_id} deleted successfully"})
        else:
            return jsonify({"success": False, "message": "Problem not found or could not be deleted"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

@app.route('/chatbot', methods=['POST'])
def chatbot_endpoint():
    """ Handle chatbot requests through Dify API """
    # This route now uses the dedicated chatbot module
    return chatbot.handle_chatbot_request()

@app.route('/check_style', methods=['POST'])
def style_check_route():
    # Get the code and language from the request
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    code = data.get('code', '')
    language = data.get('language', 'python')
    
    # Debug for diagnosing style check issues
    print(f"[APP] Received style check request for {language}")
    print(f"[APP] Code preview (first 100 chars): {code[:100]}...")
    print(f"[APP] Code length: {len(code)} characters")
    
    # Check the style
    result = check_style(code, language)
    print(f"[APP] Style check complete, sending response")
    return result

@app.route('/format_code', methods=['POST'])
def format_code_route():
    # Get the code and language from the request
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    code = data.get('code', '')
    language = data.get('language', 'cpp')  # Default to C++
    
    print(f"[APP] Received code formatting request for {language}")
    print(f"[APP] Code length: {len(code)} characters")
    
    # Format based on language
    if language == "cpp":
        result = format_cpp_code(code)
    elif language == "java":
        result = format_java_code(code)
    else:
        return jsonify({"error": f"Formatting not supported for {language}"}), 400
    
    print(f"[APP] Code formatting complete, sending response")
    return result

if __name__ == '__main__':
    app.run(port=5000, debug=True)