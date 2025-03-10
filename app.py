from flask import Flask, request, jsonify, send_from_directory
import subprocess
import json

app = Flask(__name__, static_folder='static')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """ Handles problem generation and extracts test cases """
    data = request.get_json()
    course = data.get("course", "Sololearn Introduction to Python")
    lesson = data.get("lesson", "")

    if not lesson:
        return jsonify({"error": "Lesson is required."}), 400

    result = subprocess.run(["python", "request.py", course, lesson], capture_output=True, text=True)

    try:
        output = json.loads(result.stdout)

        # Extract test cases if they exist
        raw_testcases = output.get("data", {}).get("outputs", {}).get("Testcases", "").strip()
        if not raw_testcases:
            return jsonify({"error": "Test cases not found in API response."}), 500

        # Return extracted test cases along with the original output
        output["testcases"] = raw_testcases
        return jsonify(output)

    except Exception as e:
        return jsonify({"error": "failed to generate", "message": str(e)}), 500

@app.route('/run_code', methods=['POST'])
def run_code():
    """ Runs user-submitted Python code and returns the output. """
    data = request.get_json()
    code = data.get("code", "")
    stdin = data.get("stdin", "")

    if not code.strip():
        return jsonify({"error": "No code provided"}), 400

    try:
        process = subprocess.run(
            ["python3", "-c", code], 
            input=stdin,
            capture_output=True, text=True, timeout=5
        )

        return jsonify({
            "stdout": process.stdout.strip(),
            "stderr": process.stderr.strip()
        })

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Execution timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def clean_testcase_output(output):
    """
    Cleans test case outputs by stripping markdown artifacts (` ``` `),
    trimming spaces, and ensuring proper formatting.
    """
    return output.strip().replace("```", "").strip()

def process_testcases(testcases):
    """
    Parses test cases from the provided format, separating inputs and expected outputs.
    Test cases are assumed to be formatted like:

        in
        1
        2
        3
        out
        4
        5
        6
    """
    lines = testcases.strip().split("\n")
    inputs, expected_outputs = [], []
    
    collecting_input = True
    for line in lines:
        if line.strip().lower() == "out":
            collecting_input = False
            continue

        if collecting_input:
            inputs.append(line.strip())
        else:
            expected_outputs.append(clean_testcase_output(line))

    return inputs, expected_outputs

import re

def parse_testcases(raw_testcases):
    """Extracts input-output pairs from testcases."""
    lines = raw_testcases.strip().split("\n")

    # Remove markdown fences (` ``` `)
    if lines[0].strip() == "```":
        lines.pop(0)
    if lines[-1].strip() == "```":
        lines.pop(-1)

    # Find "in" and "out" markers
    try:
        in_index = lines.index("in") + 1  # Start after "in"
        out_index = lines.index("out") + 1  # Start after "out"
    except ValueError:
        return [], []  # If markers are missing, return empty lists

    inputs = lines[in_index:out_index-1]  # Everything between "in" and "out"
    outputs = lines[out_index:]  # Everything after "out"

    return inputs, outputs

@app.route("/check_code", methods=["POST"])
def check_code():
    data = request.get_json()
    user_code = data.get("code", "").strip()
    raw_testcases = data.get("testcases", "")

    inputs, expected_outputs = parse_testcases(raw_testcases)

    if not inputs or not expected_outputs:
        return jsonify({"error": "No valid testcases found."})

    results = []
    for i, testcase in enumerate(inputs):
        expected_output = expected_outputs[i] if i < len(expected_outputs) else "MISSING"

        # Run user's code
        try:
            result = subprocess.run(
                ["python3", "-c", user_code],
                input=testcase,
                capture_output=True,
                text=True,
                timeout=2
            )
            user_output = result.stdout.strip()
            error_output = result.stderr.strip()

            # Determine status
            if error_output:
                status = "Runtime Error"
                results.append({"input": testcase, "expected_output": expected_output, "user_output": error_output, "status": "❌"})
            else:
                status = "✅" if user_output == expected_output else "❌"
                results.append({"input": testcase, "expected_output": expected_output, "user_output": user_output, "status": status})

        except subprocess.TimeoutExpired:
            results.append({"input": testcase, "expected_output": expected_output, "user_output": "Timeout", "status": "❌"})

    return jsonify({"results": results})
if __name__ == '__main__':
    app.run(port=5000, debug=True)