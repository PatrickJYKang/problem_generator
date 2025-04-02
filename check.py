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
        
    # Extract inputs and expected outputs from JSON testcases
    inputs = [tc.get("input", "") for tc in testcases]
    
    # Handle different field names for expected output
    expected_outputs = []
    for tc in testcases:
        if "expected_output" in tc:
            expected_outputs.append(tc.get("expected_output", ""))
        else:
            expected_outputs.append(tc.get("output", ""))
    
    results = []
    for i, testcase in enumerate(inputs):
        expected_output = expected_outputs[i] if i < len(expected_outputs) else "MISSING"

        # Run user's code based on language
        try:
            if language == "python":
                result = subprocess.run(
                    ["python3", "-c", code],
                    input=testcase,
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                user_output = result.stdout.strip()
                error_output = result.stderr.strip()
            elif language == "java" or language == "cpp":
                # For compiled languages, we need to use the same approach as in run_code
                # This is a simplified version that just returns an error for now
                return jsonify({"error": f"Checking {language} code against test cases is not yet implemented."}), 501
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
    
    return jsonify({
        "results": results,
        "passed": passed_count,
        "total": total_count,
        "success_rate": f"{passed_count}/{total_count}"
    })
