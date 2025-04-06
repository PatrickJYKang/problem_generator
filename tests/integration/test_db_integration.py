import os
import tempfile
import json
import pytest
from pathlib import Path
import sqlite3

import db
from db import init_db, get_db_connection

class TestDatabaseIntegration:
    """
    Integration tests for database operations
    
    Verifies that database functions correctly store and retrieve data.
    Uses a temporary database file for testing.
    """
    
    @pytest.fixture(scope="function")
    def test_db_path(self):
        """Create a temporary database file for testing"""
        _, db_path = tempfile.mkstemp()
        yield db_path
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    @pytest.fixture(scope="function")
    def setup_test_db(self, test_db_path):
        """Set up the test database with test data"""
        # Override the database path for testing
        original_db_path = db.DB_PATH
        db.DB_PATH = test_db_path
        
        # Initialize the database
        init_db()
        
        yield
        
        # Restore the original database path
        db.DB_PATH = original_db_path
    
    def test_init_db_creates_tables(self, test_db_path, setup_test_db):
        """Test that init_db creates the required tables"""
        # Connect to the database
        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()
        
        # Check if the tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Verify tables
        assert "problems" in tables
        assert "solutions" in tables
        
        # Verify problems table schema
        cursor.execute("PRAGMA table_info(problems)")
        columns = {row[1] for row in cursor.fetchall()}
        
        assert "id" in columns
        assert "title" in columns
        assert "problem_text" in columns  # Changed from 'problem' to 'problem_text' to match actual schema
        assert "course" in columns
        assert "lesson" in columns
        assert "created_at" in columns
        assert "language" in columns
        
        # Verify solutions table schema
        cursor.execute("PRAGMA table_info(solutions)")
        columns = {row[1] for row in cursor.fetchall()}
        
        assert "id" in columns
        assert "problem_id" in columns
        assert "language" in columns
        assert "code" in columns  # Changed from 'solution' to 'code' to match actual schema
        assert "passed_testcases" in columns  # Changed from 'passed' to 'passed_testcases'
        assert "total_testcases" in columns  # Changed from 'total' to 'total_testcases'
        assert "submitted_at" in columns  # Changed from 'created_at' to 'submitted_at'
        
        conn.close()
    
    def test_store_and_retrieve_problem(self, setup_test_db):
        """Test storing and retrieving a problem"""
        # Store a problem
        # Create a proper Python list instead of a JSON string for testcases
        testcases = [{"input": "1, 2", "expected_output": "3"}]
        problem_id = db.store_problem(
            title="Test Problem",
            problem_text="Write a function that adds two numbers",  # Changed parameter name from 'problem' to 'problem_text'
            testcases=testcases,  # Pass as a Python list, not a JSON string
            course="learnpython.org",
            lesson="Basic Operators",
            language="python"
        )
        
        # Verify the problem was stored
        assert problem_id is not None
        assert problem_id > 0
        
        # Retrieve the problem
        problem = db.get_problem_by_id(problem_id)
        
        # Verify the problem data
        assert problem is not None
        assert problem["id"] == problem_id
        assert problem["title"] == "Test Problem"
        assert problem["problem_text"] == "Write a function that adds two numbers"  # Changed from 'problem' to 'problem_text'
        assert problem["course"] == "learnpython.org"
        assert problem["lesson"] == "Basic Operators"
        assert problem["language"] == "python"
        
        # Verify testcases were stored as JSON
        # The testcases might already be parsed into a Python object or still be a JSON string
        if isinstance(problem["testcases"], str):
            testcases = json.loads(problem["testcases"])
        else:
            testcases = problem["testcases"]
        
        assert len(testcases) == 1
        assert testcases[0]["input"] == "1, 2"
        assert testcases[0]["expected_output"] == "3"
    
    def test_store_and_retrieve_solution(self, setup_test_db):
        """Test storing and retrieving a solution"""
        # Store a problem first
        testcases = [{"input": "1, 2", "output": "3"}]
        problem_id = db.store_problem(
            title="Test Problem",
            problem_text="Write a function that adds two numbers",  # Changed parameter name
            testcases=testcases,  # Use Python list
            course="learnpython.org",
            lesson="Basic Operators",
            language="python"
        )
        
        # Store a solution for the problem
        solution_id = db.store_solution(
            problem_id=problem_id,
            language="python",
            code="def add(a, b):\n    return a + b",  # Changed parameter name from 'solution' to 'code'
            passed_testcases=1,  # Changed parameter name from 'passed' to 'passed_testcases'
            total_testcases=1  # Changed parameter name from 'total' to 'total_testcases'
        )
        
        # Verify the solution was stored
        assert solution_id is not None
        assert solution_id > 0
        
        # Retrieve solutions for the problem
        solutions = db.get_solutions_for_problem(problem_id)
        
        # Verify the solution data
        assert solutions is not None
        assert len(solutions) == 1
        
        solution = solutions[0]
        assert solution["id"] == solution_id
        assert solution["problem_id"] == problem_id
        assert solution["language"] == "python"
        assert solution["code"] == "def add(a, b):\n    return a + b"  # Changed from 'solution' to 'code'
        assert solution["passed_testcases"] == 1  # Changed from 'passed' to 'passed_testcases'
        assert solution["total_testcases"] == 1  # Changed from 'total' to 'total_testcases'
    
    def test_get_problems_by_lesson(self, setup_test_db):
        """Test retrieving problems filtered by course and lesson"""
        # Store multiple problems
        problem1_id = db.store_problem(
            title="Problem 1",
            problem_text="First problem",  # Changed parameter name
            testcases=[{"input": "1", "expected_output": "1"}],  # Use Python list
            course="learnpython.org",
            lesson="Basic Operators",
            language="python"
        )
        
        problem2_id = db.store_problem(
            title="Problem 2",
            problem_text="Second problem",  # Changed parameter name
            testcases=[{"input": "2", "expected_output": "2"}],  # Use Python list
            course="learnpython.org",
            lesson="Basic Operators",
            language="python"
        )
        
        problem3_id = db.store_problem(
            title="Problem 3",
            problem_text="Third problem",  # Changed parameter name
            testcases=[{"input": "3", "expected_output": "3"}],  # Use Python list
            course="learnpython.org",
            lesson="Variables",
            language="python"
        )
        
        # Retrieve problems for a specific lesson
        problems = db.get_problems_by_lesson("learnpython.org", "Basic Operators")
        
        # Verify the filtered problems
        assert problems is not None
        assert len(problems) == 2
        
        problem_ids = [p["id"] for p in problems]
        assert problem1_id in problem_ids
        assert problem2_id in problem_ids
        assert problem3_id not in problem_ids
    
    def test_delete_problem_and_solutions(self, setup_test_db):
        """Test deleting a problem and its solutions"""
        # Store a problem
        problem_id = db.store_problem(
            title="Test Problem",
            problem_text="Write a function that adds two numbers",  # Changed parameter name
            testcases=[{"input": "1, 2", "expected_output": "3"}],  # Use Python list
            course="learnpython.org",
            lesson="Basic Operators",
            language="python"
        )
        
        # Store solutions for the problem
        db.store_solution(
            problem_id=problem_id,
            language="python",
            code="def add(a, b):\n    return a + b",  # Changed parameter name from 'solution' to 'code'
            passed_testcases=1,  # Changed parameter name from 'passed' to 'passed_testcases'
            total_testcases=1  # Changed parameter name from 'total' to 'total_testcases'
        )
        
        db.store_solution(
            problem_id=problem_id,
            language="java",
            code="public int add(int a, int b) {\n    return a + b;\n}",  # Changed parameter name from 'solution' to 'code'
            passed_testcases=1,  # Changed parameter name from 'passed' to 'passed_testcases'
            total_testcases=1  # Changed parameter name from 'total' to 'total_testcases'
        )
        
        # Verify the problem and solutions exist
        problem = db.get_problem_by_id(problem_id)
        assert problem is not None
        
        solutions = db.get_solutions_for_problem(problem_id)
        assert len(solutions) == 2
        
        # Delete the problem
        result = db.delete_problem(problem_id)
        assert result is True
        
        # Verify the problem and solutions are gone
        problem = db.get_problem_by_id(problem_id)
        assert problem is None
        
        solutions = db.get_solutions_for_problem(problem_id)
        assert len(solutions) == 0
