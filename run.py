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

    try:
        if language == "python":
            # Run Python code
            process = subprocess.run(
                ["python3", "-c", code], 
                input=stdin,
                capture_output=True, text=True, timeout=5
            )
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

        return jsonify({
            "stdout": process.stdout.strip(),
            "stderr": process.stderr.strip()
        })

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Execution timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# This is still used to run the Flask app
if __name__ == "__main__":
    from app import app
    app.run(port=5000, debug=True)
