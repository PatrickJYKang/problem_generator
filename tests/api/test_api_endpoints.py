import json
import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from flask import jsonify

from app import app as flask_app
from db import init_db  # Import init_db to create test database

class TestAPIEndpoints:
    """
    API tests for the Problem Generator application
    
    Tests the API endpoints to ensure they return expected responses.
    Uses pytest fixtures to mock dependencies and create test data.
    """
    
    @pytest.fixture
    def app(self):
        """Create and configure a Flask app for testing"""
        # Configure app for testing
        flask_app.config.update({
            "TESTING": True,
        })
        
        # Create a test database in a temporary file
        _, test_db_path = tempfile.mkstemp()
        
        # Override DB path for testing
        with patch('db.DB_PATH', test_db_path):
            # Initialize the test database
            init_db()
            yield flask_app
            
        # Clean up the test database
        if os.path.exists(test_db_path):
            os.unlink(test_db_path)
    
    @pytest.fixture
    def client(self, app):
        """Create a test client for the app"""
        return app.test_client()
    
    @pytest.fixture
    def sample_problem(self):
        """Create a sample problem data structure"""
        return {
            "id": 1,
            "title": "Test Problem",
            "problem_text": "Write a function that adds two numbers.",
            "testcases": json.dumps([
                {"input": "1, 2", "expected_output": "3"},
                {"input": "5, -3", "expected_output": "2"}
            ]),
            "course": "learnpython.org",
            "lesson": "Basic Operators",
            "language": "python"
        }
    
    @pytest.fixture
    def sample_solution(self):
        """Create a sample solution data structure"""
        return {
            "id": 1,
            "problem_id": 1,
            "solution": "def add(a, b):\n    return a + b",
            "language": "python",
            "passed": 2,
            "total": 2
        }
    
    def test_serve_index(self, client):
        """Test that the main page is served correctly"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Problem Generator' in response.data
    
    @patch('github_utils.GitHubFetcher.get_lessons')
    def test_get_lessons(self, mock_get_lessons, client):
        """Test getting lessons from GitHub"""
        # Mock the fetcher response
        mock_lessons = {
            "basics": {
                "Hello World": "Hello World",
                "Variables": "Variables"
            }
        }
        mock_get_lessons.return_value = mock_lessons
        
        # Call the API
        response = client.get('/github/lessons?language=learnpython.org&lang=en')
        
        # Verify the response
        assert response.status_code == 200
        assert response.json == mock_lessons
    
    @patch('subprocess.run')
    @patch('db.store_problem')
    def test_generate_problem(self, mock_store_problem, mock_subprocess_run, client):
        """Test generating a new problem"""
        # Mock the subprocess.run response (which simulates request.py output)
        mock_subprocess_process = MagicMock()
        mock_subprocess_process.returncode = 0
        mock_subprocess_process.stdout = json.dumps({
            "data": {
                "outputs": {
                    "Title": "Test Problem",
                    "Problem": "Write a function that adds two numbers.",
                    "Testcases": json.dumps([
                        {"input": "1, 2", "expected_output": "3"},
                        {"input": "5, -3", "expected_output": "2"}
                    ])
                }
            }
        })
        mock_subprocess_process.stderr = ""
        mock_subprocess_run.return_value = mock_subprocess_process
        
        # Mock the database store_problem function to return a problem ID
        mock_store_problem.return_value = 1
        
        # Call the generate endpoint
        response = client.post('/generate', json={
            "course": "learnpython.org",
            "lesson": "Basic Operators",
            "language": "python"
        })
        
        # Check the response
        assert response.status_code == 200
        data = response.json
        assert "problem_id" in data
        assert "testcases" in data
        
        # Verify the test cases format
        assert isinstance(data["testcases"], list)
        assert len(data["testcases"]) == 2
        assert "input" in data["testcases"][0]
        assert "expected_output" in data["testcases"][0]
    
    @patch('check.check_code')
    def test_check_code_endpoint(self, mock_check_code, client, sample_problem):
        """Test checking user code against test cases"""
        # Create a response that matches the current check_code implementation format
        response_data = {
            "passed": 2,
            "total": 2,
            "results": [
                {"input": "1, 2", "expected_output": "3", "user_output": "3", "status": "✅"},
                {"input": "5, -3", "expected_output": "2", "user_output": "2", "status": "✅"}
            ],
            "success_rate": "2/2"
        }
        
        # Mock check_code to return success as a direct response (not jsonify)
        # This avoids the need for a Flask application context
        mock_check_code.return_value = (response_data, 200)
        
        # Mock the database to return our sample problem
        with patch('db.get_problem_by_id', return_value=sample_problem), \
             patch('db.store_solution'):
            
            # Call the check_code endpoint
            response = client.post('/check_code', json={
                "code": "def add(a, b):\n    return a + b",
                "testcases": json.loads(sample_problem["testcases"]),
                "problem_id": 1,
                "language": "python"
            })
            
            # Verify the response
            assert response.status_code == 200
            data = response.json
            assert data["passed"] == 2
            assert data["total"] == 2
            assert len(data["results"]) == 2
            assert data["results"][0]["status"] == "✅"
            assert data["success_rate"] == "2/2"
    
    @patch('run.run_code')
    def test_run_code_endpoint(self, mock_run_code, client):
        """Test executing user code with specified input"""
        # Mock the run_code function to return a direct response (not jsonify)
        # This mocks what jsonify would do without requiring app context
        mock_response = ({"stdout": "3", "stderr": ""}, 200)
        mock_run_code.return_value = mock_response
        
        # Call the run_code endpoint
        response = client.post('/run_code', json={
            "code": "print(1 + 2)",
            "language": "python",
            "stdin": ""
        })
        
        # Verify the response
        assert response.status_code == 200
        data = response.json
        assert data["stdout"] == "3"
        assert data["stderr"] == ""
    
    @patch('db.get_problems')
    def test_get_problems_endpoint(self, mock_get_problems, client):
        """Test retrieving all problems"""
        # Mock the database to return a list of problems
        mock_get_problems.return_value = [{"id": 1, "title": "Test Problem"}]
        
        # Call the get_problems endpoint
        response = client.get('/problems')
        
        # Verify the response
        assert response.status_code == 200
        data = response.json
        assert "problems" in data
        assert len(data["problems"]) == 1
        assert data["problems"][0]["id"] == 1
    
    @patch('db.get_problems_by_lesson')
    def test_get_problems_filtered_by_lesson(self, mock_get_problems_by_lesson, client):
        """Test retrieving problems filtered by course and lesson"""
        # Mock the database to return filtered problems
        mock_get_problems_by_lesson.return_value = [{"id": 1, "title": "Test Problem"}]
        
        # Call the get_problems endpoint with filters
        response = client.get('/problems?course=learnpython.org&lesson=Basic%20Operators')
        
        # Verify the response
        assert response.status_code == 200
        data = response.json
        assert "problems" in data
        assert len(data["problems"]) == 1
        assert data["problems"][0]["id"] == 1
    
    @patch('db.get_problem_by_id')
    def test_get_problem_by_id(self, mock_get_problem_by_id, client, sample_problem):
        """Test retrieving a specific problem by ID"""
        # Mock the database to return our sample problem
        mock_get_problem_by_id.return_value = sample_problem
        
        # Call the get_problem endpoint
        response = client.get('/problems/1')
        
        # Verify the response
        assert response.status_code == 200
        data = response.json
        assert "problem" in data
        assert data["problem"]["id"] == 1
        assert data["problem"]["title"] == "Test Problem"
    
    @patch('db.get_problem_by_id')
    def test_get_problem_not_found(self, mock_get_problem_by_id, client):
        """Test retrieving a non-existent problem"""
        # Mock the database to return None (problem not found)
        mock_get_problem_by_id.return_value = None
        
        # Call the get_problem endpoint with a non-existent ID
        response = client.get('/problems/999')
        
        # Verify the response
        assert response.status_code == 404
        data = response.json
        assert "error" in data
        assert data["error"] == "Problem not found"
    
    @patch('db.get_solutions_for_problem')
    def test_get_solutions(self, mock_get_solutions, client, sample_solution):
        """Test retrieving solutions for a problem"""
        # Mock the database to return our sample solution
        mock_get_solutions.return_value = [sample_solution]
        
        # Call the get_solutions endpoint
        response = client.get('/problems/1/solutions')
        
        # Verify the response
        assert response.status_code == 200
        data = response.json
        assert "solutions" in data
        assert len(data["solutions"]) == 1
        assert data["solutions"][0]["id"] == 1
        assert data["solutions"][0]["problem_id"] == 1
    
    @patch('db.delete_problem')
    def test_delete_problem(self, mock_delete_problem, client):
        """Test deleting a problem"""
        # Mock the database to return success
        mock_delete_problem.return_value = True
        
        # Call the delete_problem endpoint
        response = client.delete('/problems/1')
        
        # Verify the response
        assert response.status_code == 200
        data = response.json
        assert data["success"] is True
    
    @patch('db.delete_problem')
    def test_delete_problem_not_found(self, mock_delete_problem, client):
        """Test deleting a non-existent problem"""
        # Mock the database to return failure
        mock_delete_problem.return_value = False
        
        # Call the delete_problem endpoint with a non-existent ID
        response = client.delete('/problems/999')
        
        # Verify the response
        assert response.status_code == 404
        data = response.json
        assert data["success"] is False
    
    @patch('chatbot.handle_chatbot_request')
    def test_chatbot_endpoint(self, mock_handle_chatbot, client):
        """Test the chatbot endpoint"""
        # Mock the chatbot handler to return a dictionary response instead of using jsonify
        # This avoids the application context requirement
        mock_response = {"response": "This is a test response"}
        mock_handle_chatbot.return_value = mock_response
        
        # Call the chatbot endpoint
        response = client.post('/chatbot', json={
            "message": "Help me with this problem",
            "problem_id": 1,
            "code": "def add(a, b):\n    return a + b"
        })
        
        # Verify that the chatbot handler was called
        mock_handle_chatbot.assert_called_once()
