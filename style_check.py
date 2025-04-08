import subprocess
import json
import os
import tempfile
import re
from flask import jsonify

def check_style(code, language):
    """
    Check code style using language-specific linters.
    
    Args:
        code (str): The user's code to check
        language (str): Programming language (python, java, cpp)
        
    Returns:
        Flask response with style check results
    """
    print(f"\n[STYLE CHECK] Received request for language: {language}")
    print(f"[STYLE CHECK] Code length: {len(code)} characters")
    print(f"[STYLE CHECK] Code preview: {code[:50]}...")
    
    # Safety check - make sure code isn't just an error code
    if code and len(code) <= 5 and re.match(r'^[EWF][0-9]{3}$', code):
        print(f"[STYLE CHECK] WARNING: Code appears to be just an error code: {code}")
        code = f"# Placeholder code - no valid code provided\n# Error code: {code}"
    
    if not code.strip():
        print("[STYLE CHECK] Error: No code provided")
        return jsonify({"error": "No code provided"}), 400
        
    try:
        # Select appropriate style checker based on language
        print(f"[STYLE CHECK] Using checker for {language}")
        
        if language == "python":
            try:
                # Quick check if flake8 is installed
                subprocess.run(['flake8', '--version'], capture_output=True, check=True)
                return check_python_style(code)
            except (subprocess.SubprocessError, FileNotFoundError):
                print("[STYLE CHECK] flake8 not found, using fallback")
                return provide_fallback_style_check(code, language)
                
        elif language == "java":
            try:
                # Check if PMD is installed
                subprocess.run(['pmd', 'check', '--help'], capture_output=True)
                return check_java_style(code)
            except (subprocess.SubprocessError, FileNotFoundError):
                print("[STYLE CHECK] PMD not found, using fallback")
                return provide_fallback_style_check(code, language)
                
        elif language == "cpp":
            try:
                # Check if clang-tidy is installed
                subprocess.run(['clang-tidy', '--version'], capture_output=True, check=True)
                return check_cpp_style(code)
            except (subprocess.SubprocessError, FileNotFoundError):
                print("[STYLE CHECK] clang-tidy not found, using fallback")
                return provide_fallback_style_check(code, language)
                
        else:
            print(f"[STYLE CHECK] Error: Style checking not supported for {language}")
            return jsonify({"error": f"Style checking not supported for {language}"}), 400
            
    except Exception as e:
        print(f"[STYLE CHECK] Exception: {str(e)}")
        return provide_fallback_style_check(code, language)

def get_linter_name(language):
    """Return the name of the linter used for each language"""
    if language == "python":
        return "flake8"
    elif language == "java":
        return "PMD"
    elif language == "cpp":
        return "clang-tidy"
    else:
        return "Unknown"
        
def provide_fallback_style_check(code, language):
    """Provide basic style feedback when actual linters aren't available"""
    print(f"[STYLE CHECK] Using fallback style checker for {language}")
    
    # Split the code into lines
    code_lines = code.splitlines()
    if not code_lines and code.strip():
        code_lines = [code]
    
    # Create basic style feedback
    errors = []
    linter_name = get_linter_name(language) + " (Fallback Mode)"
    
    if language == "python":
        # Check for common Python style issues
        for i, line in enumerate(code_lines):
            line_num = i + 1
            # Check line length
            if len(line) > 79:
                errors.append({
                    "line": line_num,
                    "column": 80,
                    "message": "Line too long (> 79 characters)",
                    "code": "E501"
                })
            # Check for trailing whitespace
            if line.rstrip() != line:
                errors.append({
                    "line": line_num,
                    "column": len(line.rstrip()) + 1,
                    "message": "Trailing whitespace",
                    "code": "W291"
                })
            # Check for tabs
            if '\t' in line:
                errors.append({
                    "line": line_num,
                    "column": line.find('\t') + 1,
                    "message": "Tab character instead of spaces",
                    "code": "W191"
                })
    
    elif language == "java":
        # Check for common Java style issues
        for i, line in enumerate(code_lines):
            line_num = i + 1
            # Check line length
            if len(line) > 100:
                errors.append({
                    "line": line_num,
                    "column": 101,
                    "message": "Line exceeds 100 characters",
                    "code": "LineLength"
                })
            # Check for trailing whitespace
            if line.rstrip() != line:
                errors.append({
                    "line": line_num,
                    "column": len(line.rstrip()) + 1,
                    "message": "Trailing whitespace",
                    "code": "TrailingWhitespace"
                })
            # Check for tabs
            if '\t' in line:
                errors.append({
                    "line": line_num,
                    "column": line.find('\t') + 1,
                    "message": "Tab used for indentation",
                    "code": "TabIndentation"
                })
            # Check braces for placement
            if line.strip().endswith('{') and ') {' not in line and '} {' not in line:
                errors.append({
                    "line": line_num,
                    "column": line.find('{') + 1,
                    "message": "'{' should be on the same line as the declaration",
                    "code": "LeftCurly"
                })
    
    elif language == "cpp":
        # Check for common C++ style issues
        for i, line in enumerate(code_lines):
            line_num = i + 1
            # Check line length
            if len(line) > 80:
                errors.append({
                    "line": line_num,
                    "column": 81,
                    "message": "Line is longer than 80 characters",
                    "code": "readability-line-length"
                })
            # Check for trailing whitespace
            if line.rstrip() != line:
                errors.append({
                    "line": line_num,
                    "column": len(line.rstrip()) + 1,
                    "message": "Trailing whitespace detected",
                    "code": "whitespace-trailing"
                })
            # Check for tabs
            if '\t' in line:
                errors.append({
                    "line": line_num,
                    "column": line.find('\t') + 1,
                    "message": "Tab character used instead of spaces",
                    "code": "whitespace-tab"
                })
            # Check for spacing around operators
            for op in ['+', '-', '*', '/', '=', '==', '!=']:
                if op in line and f" {op} " not in line and line.strip() != op:
                    errors.append({
                        "line": line_num,
                        "column": line.find(op) + 1,
                        "message": f"Missing space around '{op}' operator",
                        "code": "whitespace-around-operators"
                    })
    
    # Add a note about fallback mode
    if len(errors) == 0:
        # Add at least one suggestion if none were found
        errors.append({
            "line": 1,
            "column": 1,
            "message": f"No style issues found in fallback mode. Install {get_linter_name(language)} for more comprehensive checks.",
            "code": "INFO"
        })
    else:
        # Add a note about limited checking
        errors.append({
            "line": 1,
            "column": 1,
            "message": f"Limited style checking only. Install {get_linter_name(language)} for comprehensive checks.",
            "code": "NOTE"
        })
    
    # Return the results
    return jsonify({
        "errors": errors,
        "total": len(errors),
        "code": code_lines,
        "raw_code": code,
        "linter": linter_name,
        "fallback": True
    })

def check_python_style(code):
    """Check Python code style using flake8"""
    print("[STYLE CHECK] Running Python style check with flake8")
    print(f"[STYLE CHECK] Original code (first 100 chars): {code[:100]}...")
    
    # Store the original code to preserve it throughout the process
    original_code = code
    
    try:
        # Create a temporary file with the code
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as temp_file:
            temp_file.write(code)
            temp_path = temp_file.name
            print(f"[STYLE CHECK] Created temporary file: {temp_path}")
        
        # Run flake8 on the temporary file
        try:
            # First try with JSON format if flake8-json is available
            result = subprocess.run(
                ['flake8', '--format=json', temp_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Parse the output as JSON if possible
            try:
                error_data = json.loads(result.stdout)
                # Convert to our standardized format
                errors = []
                
                for file_path, file_errors in error_data.items():
                    for error in file_errors:
                        errors.append({
                            "line": error.get("line_number", 1),
                            "column": error.get("column_number", 1),
                            "message": error.get("text", "Unknown error"),
                            "code": error.get("code", "")
                        })
                        
            except json.JSONDecodeError:
                # If JSON parsing fails, fallback to standard format
                raise ValueError("JSON parsing failed")
                
        except (subprocess.SubprocessError, ValueError):
            # Fallback to standard format if JSON format is not available
            result = subprocess.run(
                ['flake8', temp_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Parse the output in standard format (filename:line:column: error)
            pattern = r'.*?:(\d+):(\d+): ([A-Z]\d+) (.*)'
            errors = []
            
            for line in result.stdout.splitlines():
                match = re.match(pattern, line)
                if match:
                    line_num, col_num, error_code, message = match.groups()
                    errors.append({
                        "line": int(line_num),
                        "column": int(col_num),
                        "message": message,
                        "code": error_code
                    })
        
        # Clean up the temporary file
        os.unlink(temp_path)
        
        # Return the formatted results
        code_lines = code.splitlines()
        if not code_lines and code.strip():
            # Handle case where code might not have proper line endings
            code_lines = [code]
            
        # Sanity check for code_lines
        if len(code_lines) == 1 and code_lines[0].strip() in [error.get('code', '') for error in errors]:
            print(f"[STYLE CHECK] WARNING: code_lines appears to contain just an error code: {code_lines[0]}")
            # Split the original code again to ensure we have the real code
            code_lines = code.splitlines() or ["# No valid code lines found"]
            
        # Log code lines for debugging
        print(f"[STYLE CHECK] Code has {len(code_lines)} lines")
        print(f"[STYLE CHECK] Raw code length: {len(code)} characters")
        print(f"[STYLE CHECK] First line of code: {code_lines[0] if code_lines else 'None'}")
        # Double-check if code_lines only contains error codes
        if all(line.strip() in [error.get('code', '') for error in errors] for line in code.splitlines()):
            print("[STYLE CHECK] WARNING: All code lines appear to be error codes, using original code")
            code_lines = code.splitlines() or ["# Could not parse code lines properly"]
        # Always use the original code for the response
        code_lines = original_code.splitlines()
        if not code_lines and original_code.strip():
            code_lines = [original_code]
            
        # Create result dictionary
        result = {
            "errors": errors,
            "total": len(errors),
            "code": code_lines,
            "raw_code": original_code,  # Include raw code for frontend
            "linter": "flake8"
        }
        print(f"[STYLE CHECK] Found {len(errors)} Python style issues")
        for error in errors[:5]:  # Print first 5 errors for debugging
            print(f"[STYLE CHECK] Issue: Line {error['line']}, Col {error['column']}: {error['message']} ({error['code']})")
        if len(errors) > 5:
            print(f"[STYLE CHECK] ...and {len(errors) - 5} more issues")
        return jsonify(result)
        
    except Exception as e:
        print(f"[STYLE CHECK] Python style check error: {str(e)}")
        # Even on error, return original code with error info
        return jsonify({
            "errors": [{
                "line": 1,
                "column": 1,
                "message": f"Python style check failed: {str(e)}",
                "code": "flake8-error"
            }],
            "total": 1,
            "code": original_code.splitlines(),
            "raw_code": original_code,
            "linter": "flake8",
            "error_info": "Check if flake8 is installed properly"
        })

def check_java_style(code):
    """Check Java code style using PMD"""
    try:
        # Save the original code for the response
        original_code = code
        print(f"[STYLE CHECK] Java code length: {len(original_code)} chars")
        
        # Create a temporary file with the user's code exactly as-is
        with tempfile.NamedTemporaryFile(suffix='.java', mode='w', delete=False) as temp_file:
            # Write the EXACT code with NO modifications
            temp_file.write(original_code)
            temp_path = temp_file.name
        
        # Debug the content we wrote
        print(f"[STYLE CHECK] Wrote Java file {temp_path} with EXACT contents from user")
        
        # Run PMD with all formatting-related rules
        cmd = [
            'pmd',
            'check',
            '-d', temp_path,
            '-R', 'category/java/codestyle.xml,rulesets/java/braces.xml,rulesets/java/empty.xml,rulesets/java/whitespace.xml',
            '-f', 'text'
        ]
        
        # Execute PMD
        try:
            print(f"[STYLE CHECK] Running PMD on {temp_path}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            
            # Parse results, plus add our own basic formatting checks
            errors = []
            for line in result.stdout.splitlines():
                # Skip empty lines or suppressed messages
                if not line.strip() or "No violations found" in line or "suppressed" in line:
                    continue
                
                # Skip NoPackage and ShortClassName rules completely
                if "NoPackage" in line or "ShortClassName" in line:
                    print(f"[STYLE CHECK] Filtering out rule: {line}")
                    continue
                
                # Extract the line number, message and rule name
                match = re.search(r'.*:(\d+):\s*(.*?)\s+([A-Za-z0-9]+)$', line)
                if match:
                    line_num, message, rule_name = match.groups()
                    
                        # Skip NoPackage and ShortClassName rules
                    if rule_name in ['NoPackage', 'ShortClassName']:
                        continue
                    
                    # Add the error to our list
                    errors.append({
                        "line": int(line_num),
                        "column": 1,  # PMD doesn't provide column info in text format
                        "message": message.strip(),
                        "code": rule_name.strip()
                    })
            
            # Add our own basic formatting checks since PMD misses some obvious things
            lines = original_code.splitlines()
            for i, line in enumerate(lines):
                line_num = i + 1
                
                # Check for inconsistent spacing around operators - more thorough check
                for op in ['=', '+', '-', '*', '/', '<', '>']:
                    if op in line and not line.strip().startswith('//') and not line.strip().startswith('/*'):
                        # Print debug information about the line
                        print(f"[STYLE CHECK] Checking line {line_num}: '{line.strip()}'")
                        
                        # Look for patterns of operators without proper spacing
                        if op == '=' and re.search(r'[\w)]}]=[\w({\[]', line):
                            errors.append({
                                "line": line_num,
                                "column": line.find(op) + 1,
                                "message": f"Missing space around '{op}' operator",
                                "code": "SpaceAroundOperator"
                            })
                            print(f"[STYLE CHECK] Found missing space around '=' at line {line_num}")
                        
                        # Check for spacing around comparison operators
                        elif op in ['<', '>'] and re.search(r'[\w)]\s*{op}\s*\s+[\w(]'.format(op=re.escape(op)), line):
                            errors.append({
                                "line": line_num,
                                "column": line.find(op) + 1,
                                "message": f"Inconsistent spacing around '{op}' operator",
                                "code": "SpaceAroundOperator"
                            })
                            print(f"[STYLE CHECK] Found inconsistent spacing around '{op}' at line {line_num}")
                                
                # Check for statements without proper spacing before braces
                if '{' in line and not line.strip().startswith('{') and not line.strip().startswith('if') and not line.strip().startswith('for') and not line.strip().startswith('while'):
                    index = line.find('{')
                    if index > 0 and line[index-1] != ' ':
                        errors.append({
                            "line": line_num,
                            "column": index + 1,
                            "message": "Missing space before opening brace",
                            "code": "SpaceBeforeBrace"
                        })
                        print(f"[STYLE CHECK] Found missing space before brace at line {line_num}")
                
                # Check for lines with multiple statements (excluding for loop initialization)
                if ';' in line and ';' in line[line.find(';')+1:] and not line.strip().startswith('for'):
                    errors.append({
                        "line": line_num,
                        "column": line.find(';') + 1,
                        "message": "Multiple statements on same line",
                        "code": "OneStatementPerLine"
                    })
                    print(f"[STYLE CHECK] Found multiple statements at line {line_num}")
                
                # Look for code like 'for(...){' without space before brace or '(...){'
                if re.search(r'\)\{', line):
                    errors.append({
                        "line": line_num,
                        "column": line.find('){') + 2,
                        "message": "Missing space before opening brace",
                        "code": "SpaceBeforeBrace"
                    })
                    print(f"[STYLE CHECK] Found missing space before brace after parenthesis at line {line_num}")
            
        except Exception as e:
            print(f"[STYLE CHECK] PMD execution error: {str(e)}")
            # Safely return with the original code even on PMD error
            return jsonify({
                "errors": [{
                    "line": 1, 
                    "column": 1,
                    "message": f"PMD execution error: {str(e)}",
                    "code": "PMD-error"
                }],
                "total": 1,
                "code": original_code.splitlines() or [original_code],
                "raw_code": original_code,
                "linter": "PMD"
            })
        
        finally:
            # Always clean up the temp file
            try:
                os.unlink(temp_path)
                print(f"[STYLE CHECK] Removed temporary file: {temp_path}")
            except Exception as e:
                print(f"[STYLE CHECK] Error removing temp file: {str(e)}")
        
        # Prepare the code lines from the original code
        code_lines = original_code.splitlines()
        if not code_lines and original_code.strip():
            code_lines = [original_code]
        
        # Return the results with the original code
        return jsonify({
            "errors": errors,
            "total": len(errors),
            "code": code_lines,
            "raw_code": original_code,
            "linter": "PMD"
        })
        
    except Exception as e:
        print(f"[STYLE CHECK] Java style check error: {str(e)}")
        # Always return the original code
        return jsonify({
            "errors": [{
                "line": 1,
                "column": 1,
                "message": f"Java style check failed: {str(e)}",
                "code": "pmd-error"
            }],
            "total": 1,
            "code": original_code.splitlines() or [original_code],
            "raw_code": original_code,
            "linter": "PMD"
        })

def format_java_code(code):
    """Format Java code with a simple formatter"""
    try:
        # Store original code in case of errors
        original_code = code
        print(f"[FORMAT] Java code length: {len(original_code)} chars")
        
        # Since we don't have google-java-format installed, implement a simple formatter
        formatted_lines = []
        lines = original_code.splitlines()
        
        for line in lines:
            # Fix spacing around operators
            for op in ['=', '+', '-', '*', '/', '<', '>']:
                # Replace missing spaces around operators
                line = re.sub(r'([\w)\]\}])({op})([\w(\[\{{])'.format(op=re.escape(op)), r'\1 \2 \3', line)
                # Fix excessive spaces
                line = re.sub(r'\s+({op})\s+'.format(op=re.escape(op)), r' \1 ', line)
            
            # Fix spacing before opening braces
            line = re.sub(r'\)\{', r') {', line)
            
            # Fix other opening brace spacing
            line = re.sub(r'([^\s])\{', r'\1 {', line)
            
            # Fix spacing after if/for/while
            line = re.sub(r'(if|for|while)\(', r'\1 (', line)
            
            formatted_lines.append(line)
        
        # Basic code structure improvements
        formatted_code = '\n'.join(formatted_lines)
        
        # Handle multiple statements on a line by breaking them out
        # Only do this if not in a for loop header
        formatted_code = re.sub(r'([^;]+;)\s*([^;\s]+;)', r'\1\n    \2', formatted_code)
        
        print(f"[FORMAT] Java code formatted successfully")
        
        return jsonify({
            "formatted_code": formatted_code,
            "success": True
        })
        
    except Exception as e:
        error_message = f"Java formatting error: {str(e)}"
        print(f"[FORMAT] {error_message}")
        return jsonify({
            "error": error_message,
            "success": False,
            "original_code": code
        })

def format_cpp_code(code):
    """Format C++ code using clang-format"""
    try:
        # Store original code in case of errors
        original_code = code
        print(f"[FORMAT] C++ code length: {len(original_code)} chars")
        
        # Create a temporary file with the code
        with tempfile.NamedTemporaryFile(suffix='.cpp', mode='w', delete=False) as temp_file:
            temp_file.write(code)
            temp_path = temp_file.name
            print(f"[FORMAT] Created temporary file: {temp_path}")
        
        # Run clang-format on the temporary file
        # Using LLVM style as default
        cmd = ['clang-format', temp_path, '-style=LLVM']
        
        try:
            # Execute clang-format
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            print(f"[FORMAT] clang-format return code: {result.returncode}")
            
            if result.returncode == 0:
                # Formatting successful
                formatted_code = result.stdout
                
                # If output is empty, read the file (may be an in-place operation)
                if not formatted_code:
                    try:
                        with open(temp_path, 'r') as file:
                            formatted_code = file.read()
                    except Exception as e:
                        print(f"[FORMAT] Error reading formatted file: {str(e)}")
                        formatted_code = original_code
                
                return jsonify({
                    "formatted_code": formatted_code,
                    "success": True
                })
            else:
                # Formatting failed
                error_message = result.stderr or "Formatting failed with no error message"
                print(f"[FORMAT] clang-format error: {error_message}")
                return jsonify({
                    "error": f"Formatting failed: {error_message}",
                    "success": False,
                    "original_code": original_code
                })
                
        except subprocess.SubprocessError as e:
            # Handle potential execution error
            error_message = f"clang-format execution failed: {str(e)}"
            print(f"[FORMAT] {error_message}")
            return jsonify({
                "error": error_message,
                "success": False,
                "original_code": original_code
            })
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_path)
                print(f"[FORMAT] Removed temporary file: {temp_path}")
            except Exception as e:
                print(f"[FORMAT] Error removing temporary file: {str(e)}")
    
    except Exception as e:
        # General error handling
        error_message = f"C++ formatting error: {str(e)}"
        print(f"[FORMAT] {error_message}")
        return jsonify({
            "error": error_message,
            "success": False,
            "original_code": code
        })

def check_cpp_style(code):
    """Check C++ code style using clang-tidy"""
    try:
        # Store original code to ensure it's preserved throughout the process
        original_code = code
        print(f"[STYLE CHECK] C++ code length: {len(original_code)} chars")
        
        # Create a temporary file with the code
        with tempfile.NamedTemporaryFile(suffix='.cpp', mode='w', delete=False) as temp_file:
            temp_file.write(code)
            temp_path = temp_file.name
        
        # Create a temporary file for the clang-tidy output
        with tempfile.NamedTemporaryFile(suffix='.yaml', mode='w', delete=False) as output_file:
            output_path = output_file.name
        
        # Run clang-tidy on the temporary file
        # Using -checks=readability-* focuses on style issues
        cmd = [
            'clang-tidy', 
            temp_path, 
            '-checks=-*,readability-*', 
            '--', 
            '-std=c++17', 
            '-export-fixes=' + output_path
        ]
        
        try:
            # First run clang-tidy to generate output
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Parse the output
            errors = []
            pattern = r'(.*?):(\d+):(\d+): (warning|error): (.*) \[(.*)\]'
            
            for line in result.stdout.splitlines():
                match = re.search(pattern, line)
                if match:
                    _, line_num, col_num, severity, message, code = match.groups()
                    
                    # Skip clang-diagnostic-error messages as requested by user
                    if code.startswith('clang-diagnostic-error'):
                        print(f"[STYLE CHECK] Skipping diagnostic error: {message}")
                        continue
                    
                    errors.append({
                        "line": int(line_num),
                        "column": int(col_num),
                        "message": message,
                        "code": code,
                        "severity": severity
                    })
        
        except subprocess.SubprocessError as e:
            # Handle potential execution error but still return original code
            print(f"[STYLE CHECK] clang-tidy execution failed: {str(e)}")
            return jsonify({
                "errors": [{
                    "line": 1,
                    "column": 1,
                    "message": f"clang-tidy execution failed: {str(e)}",
                    "code": "clang-execution-error"
                }],
                "total": 1,
                "code": original_code.splitlines(),
                "raw_code": original_code,
                "linter": "clang-tidy",
                "error_info": "Make sure clang-tidy is installed properly."
            })
        
        # Clean up temporary files
        os.unlink(temp_path)
        os.unlink(output_path)
        
        # Split the original code into lines
        code_lines = original_code.splitlines()
        if not code_lines and original_code.strip():
            code_lines = [original_code]
            
        # Return the formatted results with preserved original code
        return jsonify({
            "errors": errors,
            "total": len(errors),
            "code": code_lines,
            "raw_code": original_code,
            "linter": "clang-tidy"
        })
        
    except Exception as e:
        print(f"C++ style check error: {str(e)}")
        raise
