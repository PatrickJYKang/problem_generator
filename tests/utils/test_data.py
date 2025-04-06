"""
Test Data Generators

This module provides utility functions for generating test data
for unit and integration tests in a consistent manner.
"""

import json
import random
import string
from datetime import datetime, timedelta

def generate_problem(problem_id=None, language=None):
    """
    Generate a test problem data structure
    
    Args:
        problem_id: Optional ID for the problem
        language: Optional language (python, java, or cpp)
    
    Returns:
        A dictionary representing a problem
    """
    languages = ["python", "java", "cpp"]
    language = language or random.choice(languages)
    
    if language == "python":
        test_cases = [
            {"input": "1, 2", "output": "3"},
            {"input": "5, -3", "output": "2"},
            {"input": "0, 0", "output": "0"}
        ]
        title = "Add Two Numbers in Python"
        description = (
            "Write a Python function named `add_numbers` that takes two parameters and returns their sum.\n\n"
            "Example:\n"
            "```python\n"
            "add_numbers(1, 2) # Should return 3\n"
            "add_numbers(5, -3) # Should return 2\n"
            "```"
        )
    elif language == "java":
        test_cases = [
            {"input": "1 2", "output": "3"},
            {"input": "5 -3", "output": "2"},
            {"input": "0 0", "output": "0"}
        ]
        title = "Add Two Numbers in Java"
        description = (
            "Write a Java method named `addNumbers` that takes two integer parameters and returns their sum.\n\n"
            "Example:\n"
            "```java\n"
            "addNumbers(1, 2) // Should return 3\n"
            "addNumbers(5, -3) // Should return 2\n"
            "```"
        )
    else:  # cpp
        test_cases = [
            {"input": "1 2", "output": "3"},
            {"input": "5 -3", "output": "2"},
            {"input": "0 0", "output": "0"}
        ]
        title = "Add Two Numbers in C++"
        description = (
            "Write a C++ function named `addNumbers` that takes two integer parameters and returns their sum.\n\n"
            "Example:\n"
            "```cpp\n"
            "addNumbers(1, 2) // Should return 3\n"
            "addNumbers(5, -3) // Should return 2\n"
            "```"
        )
    
    courses = {
        "python": "learnpython.org",
        "java": "learnjavaonline.org",
        "cpp": "learn-cpp.org"
    }
    
    lessons = {
        "python": "Basic Operators",
        "java": "Variables and Types",
        "cpp": "Variables and Types"
    }
    
    return {
        "id": problem_id or random.randint(1, 1000),
        "title": title,
        "problem": description,
        "testcases": json.dumps(test_cases),
        "course": courses[language],
        "lesson": lessons[language],
        "language": language,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def generate_solution(problem_id=None, language=None, correct=True):
    """
    Generate a test solution data structure
    
    Args:
        problem_id: Optional ID for the problem
        language: Optional language (python, java, or cpp)
        correct: Whether the solution should be correct
    
    Returns:
        A dictionary representing a solution
    """
    languages = ["python", "java", "cpp"]
    language = language or random.choice(languages)
    problem_id = problem_id or random.randint(1, 1000)
    
    if language == "python":
        if correct:
            code = "def add_numbers(a, b):\n    return a + b"
            passed = 3
            total = 3
        else:
            code = "def add_numbers(a, b):\n    # Bug: adds 1 to the sum\n    return a + b + 1"
            passed = 0
            total = 3
    elif language == "java":
        if correct:
            code = (
                "public class Solution {\n"
                "    public static int addNumbers(int a, int b) {\n"
                "        return a + b;\n"
                "    }\n"
                "}"
            )
            passed = 3
            total = 3
        else:
            code = (
                "public class Solution {\n"
                "    public static int addNumbers(int a, int b) {\n"
                "        // Bug: adds 1 to the sum\n"
                "        return a + b + 1;\n"
                "    }\n"
                "}"
            )
            passed = 0
            total = 3
    else:  # cpp
        if correct:
            code = (
                "#include <iostream>\n\n"
                "int addNumbers(int a, int b) {\n"
                "    return a + b;\n"
                "}\n"
            )
            passed = 3
            total = 3
        else:
            code = (
                "#include <iostream>\n\n"
                "int addNumbers(int a, int b) {\n"
                "    // Bug: adds 1 to the sum\n"
                "    return a + b + 1;\n"
                "}\n"
            )
            passed = 0
            total = 3
    
    return {
        "id": random.randint(1, 1000),
        "problem_id": problem_id,
        "solution": code,
        "language": language,
        "passed": passed,
        "total": total,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def generate_random_string(length=10):
    """Generate a random string of given length"""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def generate_test_database(num_problems=5, solutions_per_problem=2):
    """
    Generate test problems and solutions
    
    Args:
        num_problems: Number of problems to generate
        solutions_per_problem: Number of solutions per problem
    
    Returns:
        A tuple of (problems, solutions)
    """
    problems = []
    solutions = []
    
    for i in range(1, num_problems + 1):
        # Create a problem with random language
        language = random.choice(["python", "java", "cpp"])
        problem = generate_problem(problem_id=i, language=language)
        problems.append(problem)
        
        # Create solutions for the problem
        for j in range(solutions_per_problem):
            # Mix of correct and incorrect solutions
            correct = random.choice([True, False])
            solution = generate_solution(problem_id=i, language=language, correct=correct)
            solution["id"] = i * 100 + j
            solutions.append(solution)
    
    return problems, solutions
