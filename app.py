from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit, join_room
import json
import os
import subprocess
import db  # Import the database module
import pty
import select
import shlex
import struct
import fcntl
import termios
import signal
from threading import Thread

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'problem_generator_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Dictionary to track active terminal sessions
terminals = {}

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
        # Run the request.py subprocess to generate a problem
        result = subprocess.run(["python3", "request.py", course, lesson], capture_output=True, text=True)
        
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

@app.route("/execute_command", methods=["POST"])
def execute_command():
    """ Execute a shell command and return the output """
    data = request.get_json()
    command = data.get("command", "").strip()
    cwd = data.get("cwd", None)  # Optional working directory
    
    if not command:
        return jsonify({"error": "No command provided"}), 400
    
    # Safety checks - limit which commands can be executed
    # This is important for security!
    allowed_commands = ["python", "python3", "javac", "java", "g++", "ls", "cat", "echo"]
    
    # Check if the command starts with an allowed command
    command_parts = command.split()
    if not command_parts or command_parts[0] not in allowed_commands:
        return jsonify({"error": f"Command not allowed: {command_parts[0]}"}), 403
    
    try:
        # Execute the command and capture output
        process = subprocess.run(
            command_parts,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10  # Timeout to prevent long-running commands
        )
        
        return jsonify({
            "stdout": process.stdout,
            "stderr": process.stderr,
            "returncode": process.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Command execution timed out"}), 408
    except Exception as e:
        return jsonify({"error": f"Error executing command: {str(e)}"}), 500

# Terminal class for real terminal functionality
class Terminal:
    def __init__(self, socket, sid):
        self.socket = socket
        self.sid = sid
        self.fd = None
        self.pid = None
        self.process = None

    def start(self, shell='/bin/bash'):
        """Start a new terminal with the specified shell."""
        # Create a new pseudo-terminal
        self.pid, self.fd = pty.fork()
        
        if self.pid == 0:  # Child process
            # Execute shell in child process
            os.execvp(shell, [shell])
        else:  # Parent process
            # Set up a thread to read data from the terminal
            Thread(target=self._read_output).start()
            return True

    def start_command(self, command):
        """Start a specific command in a new terminal."""
        # Create command parts
        command_parts = shlex.split(command)
        
        # Create a new pseudo-terminal
        self.pid, self.fd = pty.fork()
        
        if self.pid == 0:  # Child process
            # Execute command in child process
            os.execvp(command_parts[0], command_parts)
        else:  # Parent process
            # Set up a thread to read data from the terminal
            Thread(target=self._read_output).start()
            return True

    def _read_output(self):
        """Read output from the terminal and send it to the client."""
        max_read_bytes = 1024 * 20
        
        while True:
            try:
                ready_to_read, _, _ = select.select([self.fd], [], [], 0.1)
                if not ready_to_read:
                    continue
                    
                output = os.read(self.fd, max_read_bytes).decode('utf-8', errors='replace')
                if output:
                    # Send output to the client
                    self.socket.emit('terminal_output', {'output': output}, room=self.sid)
                else:
                    # EOF - process terminated
                    self.socket.emit('terminal_exit', {}, room=self.sid)
                    break
            except OSError:
                # Process exited or error occurred
                self.socket.emit('terminal_exit', {}, room=self.sid)
                break

    def resize(self, rows, cols):
        """Resize the terminal window."""
        if self.fd:
            # Create the window size structure
            winsize = struct.pack("HHHH", rows, cols, 0, 0)
            fcntl.ioctl(self.fd, termios.TIOCSWINSZ, winsize)

    def write(self, data):
        """Write data to the terminal."""
        if self.fd:
            os.write(self.fd, data.encode())

    def terminate(self):
        """Terminate the terminal process."""
        if self.pid:
            try:
                os.kill(self.pid, signal.SIGTERM)
            except OSError:
                # Process already terminated
                pass

# Socket.IO event handlers for terminal
@socketio.on('connect')
def handle_connect():
    print('Client connected', request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected', request.sid)
    # Terminate any active terminal session for this client
    if request.sid in terminals:
        terminals[request.sid].terminate()
        del terminals[request.sid]

@socketio.on('terminal_init')
def handle_terminal_init(data):
    """Initialize a new terminal session."""
    print('Terminal init requested by', request.sid)
    
    # Create a new terminal instance
    term = Terminal(socketio, request.sid)
    
    # Start a bash shell or specified command
    command = data.get('command', None)
    if command:
        success = term.start_command(command)
    else:
        success = term.start()
        
    if success:
        # Store the terminal instance
        terminals[request.sid] = term
        emit('terminal_ready', {}, room=request.sid)
    else:
        emit('terminal_error', {'message': 'Failed to start terminal'}, room=request.sid)

@socketio.on('terminal_input')
def handle_terminal_input(data):
    """Send input to the terminal."""
    if request.sid in terminals:
        terminals[request.sid].write(data.get('input', ''))

@socketio.on('terminal_resize')
def handle_terminal_resize(data):
    """Resize the terminal."""
    if request.sid in terminals:
        rows = data.get('rows', 24)
        cols = data.get('cols', 80)
        terminals[request.sid].resize(rows, cols)

@socketio.on('terminal_kill')
def handle_terminal_kill():
    """Kill the terminal session."""
    if request.sid in terminals:
        terminals[request.sid].terminate()
        del terminals[request.sid]
        emit('terminal_exit', {}, room=request.sid)

@socketio.on('run_python_code')
def handle_run_python_code(data):
    """Run Python code in a dedicated terminal."""
    import tempfile
    
    code = data.get('code', '')
    if not code.strip():
        emit('terminal_error', {'message': 'No code provided'}, room=request.sid)
        return
    
    # Create a temporary file with the code
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
        temp_path = temp.name
        temp.write(code.encode('utf-8'))
    
    # Create a new terminal instance
    if request.sid in terminals:
        terminals[request.sid].terminate()
    
    term = Terminal(socketio, request.sid)
    success = term.start_command(f"python3 {temp_path}")
    
    if success:
        terminals[request.sid] = term
        emit('terminal_ready', {}, room=request.sid)
    else:
        emit('terminal_error', {'message': 'Failed to start Python terminal'}, room=request.sid)
        try:
            os.unlink(temp_path)
        except:
            pass

if __name__ == '__main__':
    socketio.run(app, debug=True)