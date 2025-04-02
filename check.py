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
    expected_outputs = [tc.get("output", "") for tc in testcases]
    
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
            elif user_output == expected_output:
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
                    "status": "❌"
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
