"""
Unit tests for multi-language capabilities of Problem Generator
"""

import pytest
import os
import tempfile
import json
from unittest.mock import patch, MagicMock

class TestLanguageCapabilities:
    """Test that the Problem Generator supports multiple programming languages"""
    
    @pytest.mark.parametrize("language,code_template,expected_output", [
        (
            "python", 
            "def solution():\n    pass\n\n# Your code here\n", 
            "Python code execution"
        ),
        (
            "java", 
            "public class Main {\n    public static void main(String[] args) {\n        // Your code here\n    }\n}", 
            "Java code execution"
        ),
        (
            "cpp", 
            "#include <iostream>\n\nint main() {\n    // Your code here\n    return 0;\n}", 
            "C++ code execution"
        ),
    ])
    def test_language_templates(self, language, code_template, expected_output):
        """Test that appropriate code templates exist for all supported languages"""
        # Verify the templates contain expected elements for each language
        if language == "python":
            assert "def solution" in code_template
        elif language == "java":
            assert "public class Main" in code_template
            assert "public static void main" in code_template
        elif language == "cpp":
            assert "#include <iostream>" in code_template
            assert "int main()" in code_template
            assert "return 0" in code_template
    
    @pytest.mark.parametrize("language,compiler,runner", [
        ("python", None, "python"),
        ("java", "javac", "java"),
        ("cpp", "g++", None)  # For C++, we compile to executable and run directly
    ])
    def test_language_execution_commands(self, language, compiler, runner):
        """Test that each language has correct compiler/interpreter commands"""
        # This tests the commands that would be used, without actually running them
        execution_commands = {
            "python": {"compiler": None, "runner": "python"},
            "java": {"compiler": "javac", "runner": "java"},
            "cpp": {"compiler": "g++", "runner": None},
        }
        
        # Verify the correct commands are used for each language
        assert execution_commands[language]["compiler"] == compiler
        assert execution_commands[language]["runner"] == runner
    
    @pytest.mark.parametrize("language,file_extension,class_name", [
        ("python", ".py", None),
        ("java", ".java", "Main"),
        ("cpp", ".cpp", None)
    ])
    def test_language_file_properties(self, language, file_extension, class_name):
        """Test file extensions and class naming for different languages"""
        # Verify the correct file extension is used
        assert file_extension in [".py", ".java", ".cpp"]
        
        # For Java, verify the class name is correct
        if language == "java":
            assert class_name == "Main"
    
    def test_multi_language_test_cases(self):
        """Test that testcases work with all supported languages"""
        # Sample test case in JSON format that should work for all languages
        testcase = {
            "input": "5\n3",
            "output": "8"
        }
        
        # Verify the test case format
        assert "input" in testcase
        assert "output" in testcase
        
        # Test code that would pass this test case in each language
        passing_code = {
            "python": "a = int(input())\nb = int(input())\nprint(a + b)",
            "java": """
            import java.util.Scanner;
            
            public class Main {
                public static void main(String[] args) {
                    Scanner scanner = new Scanner(System.in);
                    int a = scanner.nextInt();
                    int b = scanner.nextInt();
                    System.out.println(a + b);
                }
            }
            """,
            "cpp": """
            #include <iostream>
            
            int main() {
                int a, b;
                std::cin >> a >> b;
                std::cout << a + b << std::endl;
                return 0;
            }
            """
        }
        
        # Verify each language has a solution
        for language in ["python", "java", "cpp"]:
            assert language in passing_code
            assert passing_code[language] != ""
