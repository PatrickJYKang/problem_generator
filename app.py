from flask import Flask, request, jsonify, send_from_directory
import json
import os
import subprocess
import db  # Import the database module

app = Flask(__name__, static_folder='static')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/syllabi/<path:filename>')
def serve_syllabi(filename):
    """ Serves files from the syllabi directory """
    syllabi_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'syllabi')
    return send_from_directory(syllabi_dir, filename)

@app.route('/generate', methods=['POST'])
def generate():
    """ Handles problem generation and extracts test cases """
    data = request.get_json()
    course = data.get("course", "Learnpython.org")
    lesson = data.get("lesson", "")
    if not lesson:
        return jsonify({"error": "Lesson is required."}), 400

    try:
        print("Running request.py subprocess...")
        result = subprocess.run(["python3", "request.py", course, lesson], capture_output=True, text=True)
        
        print(f"Subprocess completed with return code: {result.returncode}")
        
        # Check if there was an error in the subprocess
        if result.returncode != 0:
            print(f"Subprocess error: {result.stderr}")
            return jsonify({"error": f"Error running request.py: {result.stderr}"}), 500
            
        # Print the raw output for debugging
        print("===== RAW SUBPROCESS OUTPUT START =====")
        print(result.stdout)
        print("===== RAW SUBPROCESS OUTPUT END =====")
        
        # Also print stderr if there's any
        if result.stderr:
            print("===== SUBPROCESS STDERR START =====")
            print(result.stderr)
            print("===== SUBPROCESS STDERR END =====")
            
        # Check if stdout is empty
        if not result.stdout.strip():
            print(f"Empty response from request.py. Stderr: {result.stderr}")
            return jsonify({"error": "No response from API"}), 500
            
        # Try to parse the JSON output
        print("CHECKPOINT 1: About to try parsing JSON")
        try:
            print("CHECKPOINT 2: Inside try block, before json.loads")
            # Try to clean the output before parsing
            cleaned_stdout = result.stdout.strip()
            # Check if the output starts with any non-JSON characters
            if not cleaned_stdout.startswith('{') and not cleaned_stdout.startswith('['):
                print("Output doesn't start with { or [, trying to find JSON start")
                # Try to find the start of JSON
                json_start = cleaned_stdout.find('{')
                if json_start == -1:
                    json_start = cleaned_stdout.find('[')
                
                if json_start != -1:
                    print(f"Found JSON start at position {json_start}")
                    cleaned_stdout = cleaned_stdout[json_start:]
            
            print(f"Cleaned stdout (first 100 chars): {cleaned_stdout[:100]}")
            output = json.loads(cleaned_stdout)
            print("CHECKPOINT 3: After json.loads, JSON parsed successfully")
            print(f"Successfully parsed JSON output. Keys: {list(output.keys()) if isinstance(output, dict) else 'Not a dict'}")

            # Extract test cases if they exist
            raw_testcases = output.get("data", {}).get("outputs", {}).get("Testcases", "").strip()
            print(f"Raw testcases: {raw_testcases[:200]}...") # Print first 200 chars to avoid huge logs
            
            if not raw_testcases:
                print("No test cases found in API response")
                return jsonify({"error": "Test cases not found in API response."}), 500
                
            # Parse the JSON test cases
            try:
                # Remove any markdown code block markers if present
                clean_testcases = raw_testcases.replace("```json", "").replace("```", "").strip()
                print(f"Clean testcases: {clean_testcases[:200]}...") # Print first 200 chars
                
                try:
                    # Parse the JSON string into a Python object
                    testcases_json = json.loads(clean_testcases)
                    print(f"Successfully parsed JSON test cases: {type(testcases_json)}")
                    
                    # Ensure we have a list of test cases
                    if not isinstance(testcases_json, list):
                        print(f"Parsed JSON is not a list but {type(testcases_json)}")
                        # Try to find a list in the parsed JSON
                        if isinstance(testcases_json, dict):
                            for key, value in testcases_json.items():
                                if isinstance(value, list):
                                    print(f"Found list under key: {key}")
                                    testcases_json = value
                                    break
                    
                    # Add the parsed test cases to the output
                    output["testcases"] = testcases_json
                    print(f"Added {len(testcases_json)} test cases to the output")
                    
                    # Store the problem in the database
                    try:
                        title = output.get("data", {}).get("outputs", {}).get("Title", "Untitled Problem")
                        problem_text = output.get("data", {}).get("outputs", {}).get("Problem", "")
                        problem_id = db.store_problem(title, problem_text, course, lesson, testcases_json)
                        output["problem_id"] = problem_id
                        print(f"Stored problem in database with ID: {problem_id}")
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
            print("CHECKPOINT 4: JSON decode error caught")
            print(f"JSON decode error: {e}")
            print(f"First 500 chars of stdout: {result.stdout[:500]}")
            print(f"Last 500 chars of stdout: {result.stdout[-500:] if len(result.stdout) > 500 else result.stdout}")
            return jsonify({"error": "Invalid JSON response", "message": str(e)}), 500
    except Exception as e:
        print("CHECKPOINT 5: Main exception caught")
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception in generate endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to generate", "message": str(e), "type": type(e).__name__}), 500

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
    language = data.get("language", "python")
    testcases = data.get("testcases", [])
    problem_id = data.get("problem_id", None)
    
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
def get_problems():
    """ Get problems for a specific course and lesson """
    course = request.args.get("course", "Learnpython.org")
    lesson = request.args.get("lesson", "")
    
    if not lesson:
        return jsonify({"error": "Lesson is required."}), 400
    
    try:
        problems = db.get_problems_by_lesson(course, lesson)
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)