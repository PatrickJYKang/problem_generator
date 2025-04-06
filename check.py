import subprocess
import json
from flask import jsonify

def check_code(code, testcases, language):
    """
    Checks user code against test cases and returns the results.
    
    Args:
        code (str): The user's code to check
        testcases (list): List of test case objects with 'input' and 'output' fields
        language (str): Programming language (python, java, cpp)
        
    Returns:
        Flask response with test results
    """
    if not code.strip():
        return jsonify({"error": "No code provided"}), 400
    
    # Validate testcases format
    if not isinstance(testcases, list) or not testcases:
        return jsonify({"error": "No valid testcases found."}), 400
    
    # Convert testcases to list format if it's a JSON string
    if isinstance(testcases, str):
        try:
            testcases = json.loads(testcases)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON format for testcases"}), 400
            
    # Ensure language is set
    if not language:
        language = "python"  # Default to Python if not specified
        
    # Extract inputs and expected outputs from JSON testcases
    inputs = []
    expected_outputs = []
    
    for tc in testcases:
        # Handle various input formats
        if isinstance(tc, dict):
            if "input" in tc:
                inputs.append(tc.get("input", ""))
            else:
                inputs.append("")  # Empty input if not provided
                
            # Handle different field names for expected output
            if "expected_output" in tc:
                expected_outputs.append(tc.get("expected_output", ""))
            else:
                expected_outputs.append(tc.get("output", ""))
        else:
            # Handle simple string test cases
            try:
                inputs.append(str(tc))
                expected_outputs.append("")
            except:
                inputs.append("")
                expected_outputs.append("")
    
    results = []
    for i, testcase in enumerate(inputs):
        expected_output = expected_outputs[i] if i < len(expected_outputs) else "MISSING"

        # Run user's code based on language
        try:
            if language == "python":
                # Create a wrapper script that redirects input() prompts to stderr
                import tempfile
                import os
                
                # Create a temporary file for the wrapper code
                wrapper_fd, wrapper_path = tempfile.mkstemp(suffix='.py')
                
                try:
                    # Build the wrapper code as separate strings to avoid any escaping issues
                    wrapper_parts = [
                        "import builtins",
                        "import sys",
                        "original_input = builtins.input",
                        "",
                        "# Completely silence the input function - ignore all prompts",
                        "def input_wrapper(prompt=''):",
                        "    # Completely ignore the prompt - no printing at all",
                        "    # This ensures nothing interferes with the stdout that we check",
                        "    line = sys.stdin.readline()",
                        "    # Remove trailing newline if present",
                        "    if line and line[-1] == chr(10):",
                        "        line = line[:-1]", 
                        "    return line",
                        "",
                        "builtins.input = input_wrapper",
                        "",
                        "# User code begins here",
                        code
                    ]
                    
                    # Join with newlines and write to file
                    wrapper_code = "\n".join(wrapper_parts)
                    with os.fdopen(wrapper_fd, 'w') as f:
                        f.write(wrapper_code)
                    
                    # Run the code with the wrapper
                    result = subprocess.run(
                        ["python3", wrapper_path],
                        input=testcase,
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    user_output = result.stdout.strip()
                    error_output = result.stderr.strip()
                finally:
                    # Always clean up the temporary file
                    if os.path.exists(wrapper_path):
                        os.unlink(wrapper_path)
            elif language == "java":
                # Create a temporary Java file from the user code
                import tempfile
                import os
                temp_dir = tempfile.mkdtemp()
                
                # Extract the class name from the code
                import re
                class_match = re.search(r'public\s+class\s+(\w+)', code)
                
                # Default class name if not found
                if not class_match:
                    class_name = "Main"
                else:
                    class_name = class_match.group(1)
                
                # Write the code to a temporary file
                file_path = os.path.join(temp_dir, f"{class_name}.java")
                with open(file_path, 'w') as f:
                    f.write(code)
                
                try:
                    # Compile the code
                    compile_result = subprocess.run(
                        ["javac", file_path],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if compile_result.returncode != 0:
                        # Compilation error
                        error_output = compile_result.stderr.strip()
                        return jsonify({
                            "results": [{
                                "input": "N/A",
                                "expected_output": "N/A",
                                "user_output": error_output,
                                "status": "❌",
                                "error": f"Compilation error: {error_output}"
                            }],
                            "passed": 0,
                            "total": 1,
                            "success_rate": "0/1"
                        })
                    
                    # Execute the compiled code with the test case input
                    result = subprocess.run(
                        ["java", "-cp", temp_dir, class_name],
                        input=testcase,
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    user_output = result.stdout.strip()
                    error_output = result.stderr.strip()
                    
                    # Clean up the temporary directory
                    import shutil
                    shutil.rmtree(temp_dir)
                    
                except Exception as e:
                    user_output = ""
                    error_output = str(e)
            
            elif language == "cpp":
                # Create a temporary C++ file from the user code
                import tempfile
                import os
                temp_dir = tempfile.mkdtemp()
                file_path = os.path.join(temp_dir, "solution.cpp")
                executable_path = os.path.join(temp_dir, "solution")
                
                # Write the code to a temporary file
                with open(file_path, 'w') as f:
                    f.write(code)
                
                try:
                    # Compile the code with C++17 standard
                    compile_result = subprocess.run(
                        ["g++", "-std=c++17", file_path, "-o", executable_path],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if compile_result.returncode != 0:
                        # Compilation error
                        error_output = compile_result.stderr.strip()
                        return jsonify({
                            "results": [{
                                "input": "N/A",
                                "expected_output": "N/A",
                                "user_output": error_output,
                                "status": "❌",
                                "error": f"Compilation error: {error_output}"
                            }],
                            "passed": 0,
                            "total": 1,
                            "success_rate": "0/1"
                        })
                    
                    # Execute the compiled code with the test case input
                    result = subprocess.run(
                        [executable_path],
                        input=testcase,
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    user_output = result.stdout.strip()
                    error_output = result.stderr.strip()
                    
                    # Clean up the temporary directory
                    import shutil
                    shutil.rmtree(temp_dir)
                    
                except Exception as e:
                    user_output = ""
                    error_output = str(e)
            else:
                return jsonify({"error": f"Unsupported language: {language}"}), 400

            # Normalize expected and user output for comparison
            def normalize_output(output):
                if output is None:
                    return ""
                # Standardize line endings and remove trailing whitespace from each line
                lines = [line.rstrip() for line in output.strip().splitlines()]
                # Remove empty lines at start and end
                while lines and not lines[0]:
                    lines.pop(0)
                while lines and not lines[-1]:
                    lines.pop()
                return "\n".join(lines)
                
            normalized_expected = normalize_output(expected_output)
            normalized_user = normalize_output(user_output)
            
            # Determine status
            if error_output:
                status = "Runtime Error"
                results.append({
                    "input": testcase, 
                    "expected_output": expected_output, 
                    "user_output": error_output, 
                    "status": "❌",
                    "error": error_output
                })
            elif normalized_user == normalized_expected:
                status = "Correct"
                results.append({
                    "input": testcase, 
                    "expected_output": expected_output, 
                    "user_output": user_output, 
                    "status": "✅"
                })
            else:
                status = "Incorrect"
                results.append({
                    "input": testcase, 
                    "expected_output": expected_output, 
                    "user_output": user_output, 
                    "status": "❌",
                    "diff": f"Expected:\n{normalized_expected}\n\nGot:\n{normalized_user}"
                })
                
        except subprocess.TimeoutExpired:
            results.append({
                "input": testcase, 
                "expected_output": expected_output, 
                "user_output": "Execution timed out", 
                "status": "⌛",
                "error": "Code execution timed out (limit: 2 seconds)"
            })
        except Exception as e:
            results.append({
                "input": testcase, 
                "expected_output": expected_output, 
                "user_output": f"Error: {str(e)}", 
                "status": "❗",
                "error": str(e)
            })
    
    # Count passed testcases
    passed_count = sum(1 for r in results if r.get("status") == "✅")
    total_count = len(results)
    
    response_data = {
        "results": results,
        "passed": passed_count,
        "total": total_count,
        "success_rate": f"{passed_count}/{total_count}"
    }
    
    # Add success flag for easier frontend handling
    if passed_count == total_count and total_count > 0:
        response_data["success"] = True
    else:
        response_data["success"] = False
        
    return jsonify(response_data)
