import subprocess
import tempfile
import os
import re
import json
from flask import jsonify

def run_code(code, stdin, language):
    """ Runs user-submitted code in the specified language and returns the output. """
    if not code.strip():
        return jsonify({"error": "No code provided"}), 400

    # Create a response object to track program state
    result = {
        "stdout": "",
        "stderr": "",
        "requires_input": False,  # Set to true if the program is waiting for input
        "prompt": ""            # Any text the program displayed before waiting for input
    }

    try:
        if language == "python":
            # For Python, create a temp file rather than using -c
            # This provides better error messages with line numbers
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
                temp_path = temp.name
                temp.write(code.encode('utf-8'))
                
            # Run the python file
            process = subprocess.run(
                ["python3", temp_path], 
                input=stdin,
                capture_output=True, text=True, timeout=10
            )
            
            # Check if the program might be waiting for input
            # Look for common input patterns in the output
            output = process.stdout
            if output and not stdin and process.returncode == 0:
                # Common input prompts that might indicate waiting for input
                input_patterns = [
                    'input(', 'raw_input(', 
                    '= input', '= raw_input',
                    'Enter ', 'enter ', 'input:',
                    'Please ', 'please ',
                    '?'
                ]
                
                # If the output ends with a potential input prompt
                last_line = output.strip().split('\n')[-1] if '\n' in output else output.strip()
                if any(pattern in last_line for pattern in input_patterns) and not last_line.endswith(':'):
                    result["requires_input"] = True
                    result["prompt"] = last_line
            
            # Clean up the temp file
            os.unlink(temp_path)
        elif language == "java":
            # For Java, we need to create temporary files
            # Create a temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Determine the class name (assuming public class)
                class_match = re.search(r'public\s+class\s+(\w+)', code)
                
                if not class_match:
                    return jsonify({"error": "Could not find a public class in your Java code."}), 400
                
                class_name = class_match.group(1)
                java_file_path = os.path.join(temp_dir, f"{class_name}.java")
                
                # Write the code to a temporary Java file
                with open(java_file_path, 'w') as java_file:
                    java_file.write(code)
                
                # Compile the Java code
                compile_process = subprocess.run(
                    ["javac", java_file_path],
                    capture_output=True, text=True
                )
                
                if compile_process.returncode != 0:
                    # Compilation error
                    return jsonify({
                        "stdout": "",
                        "stderr": f"Compilation error:\n{compile_process.stderr}"
                    })
                
                # Run the compiled Java code
                process = subprocess.run(
                    ["java", "-cp", temp_dir, class_name],
                    input=stdin,
                    capture_output=True, text=True, timeout=5
                )
        elif language == "cpp":
            # For C++, we need to create temporary files
            # Create a temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create a temporary C++ file
                cpp_file_path = os.path.join(temp_dir, "main.cpp")
                executable_path = os.path.join(temp_dir, "program")
                
                # Write the code to a temporary C++ file
                with open(cpp_file_path, 'w') as cpp_file:
                    cpp_file.write(code)
                
                # Compile the C++ code
                compile_process = subprocess.run(
                    ["g++", "-std=c++17", cpp_file_path, "-o", executable_path],
                    capture_output=True, text=True
                )
                
                if compile_process.returncode != 0:
                    # Compilation error
                    return jsonify({
                        "stdout": "",
                        "stderr": f"Compilation error:\n{compile_process.stderr}"
                    })
                
                # Run the compiled C++ code
                process = subprocess.run(
                    [executable_path],
                    input=stdin,
                    capture_output=True, text=True, timeout=5
                )
        else:
            return jsonify({"error": f"Unsupported language: {language}"}), 400

        # Set result values
        result["stdout"] = process.stdout.strip()
        result["stderr"] = process.stderr.strip()
        return jsonify(result)

    except subprocess.TimeoutExpired:
        result["stderr"] = "Execution timed out. Your program took too long to run."
        return jsonify(result)
    except Exception as e:
        result["stderr"] = f"Error: {str(e)}"
        return jsonify(result)

# This is still used to run the Flask app
if __name__ == "__main__":
    from app import app
    app.run(port=5000, debug=True)
