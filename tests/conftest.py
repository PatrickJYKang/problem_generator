"""
Common test fixtures and configuration

This module contains fixtures that can be shared across different test modules.
"""

import os
import tempfile
import pytest
import json
from unittest.mock import patch, MagicMock

import db
from app import app as flask_app

@pytest.fixture(scope="function")
def app():
    """Create and configure a Flask app for testing"""
    # Configure app for testing
    flask_app.config.update({
        "TESTING": True,
    })
    
    # Create a test database in a temporary file
    _, test_db_path = tempfile.mkstemp()
    
    # Override DB path for testing
    with patch('db.DATABASE', test_db_path):
        # Initialize the test database
        db.init_db()
        yield flask_app
        
    # Clean up the test database
    if os.path.exists(test_db_path):
        os.unlink(test_db_path)

@pytest.fixture(scope="function")
def client(app):
    """Create a test client for the app"""
    return app.test_client()

@pytest.fixture(scope="function")
def sample_problem():
    """Create a sample problem data structure"""
    return {
        "id": 1,
        "title": "Test Problem",
        "problem": "Write a function that adds two numbers.",
        "testcases": json.dumps([
            {"input": "1, 2", "output": "3"},
            {"input": "5, -3", "output": "2"}
        ]),
        "course": "learnpython.org",
        "lesson": "Basic Operators",
        "language": "python",
        "created_at": "2025-04-05 17:00:00"
    }

@pytest.fixture(scope="function")
def sample_solution():
    """Create a sample solution data structure"""
    return {
        "id": 1,
        "problem_id": 1,
        "solution": "def add(a, b):\n    return a + b",
        "language": "python",
        "passed": 2,
        "total": 2,
        "created_at": "2025-04-05 17:30:00"
    }

@pytest.fixture(scope="function")
def mock_github_fetcher():
    """Create a mock GitHubFetcher with predefined responses"""
    mock_fetcher = MagicMock()
    
    # Configure mock responses
    mock_fetcher.get_lessons.return_value = {
        "basics": {
            "_order": ["Hello World", "Variables", "Loops"],
            "Hello World": "Hello World",
            "Variables": "Variables",
            "Loops": "Loops"
        }
    }
    
    mock_fetcher.get_file_content.return_value = "# Test Content\nThis is test content."
    mock_fetcher.get_json_content.return_value = {"key": "value"}
    
    return mock_fetcher
