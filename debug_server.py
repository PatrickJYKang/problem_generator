#!/usr/bin/env python3
"""
Debug script to help identify server issues
Run this on your server to check for common problems
"""

import os
import sys
import json
import requests
import importlib.util
import traceback

def check_environment():
    """Check environment variables and dependencies"""
    print("\n=== CHECKING ENVIRONMENT ===")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check for .env file and API key
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_file):
        print(f".env file exists: {env_file}")
        with open(env_file, 'r') as f:
            content = f.read()
            if 'API_KEY' in content:
                print("API_KEY found in .env file")
            else:
                print("WARNING: API_KEY not found in .env file")
    else:
        print(f"WARNING: .env file not found at {env_file}")
    
    # Check API key in environment
    api_key = os.environ.get('API_KEY')
    if api_key:
        print("API_KEY found in environment variables")
    else:
        print("WARNING: API_KEY not found in environment variables")

def check_dependencies():
    """Check required dependencies"""
    print("\n=== CHECKING DEPENDENCIES ===")
    
    required_modules = ['flask', 'requests', 'python-dotenv', 'gunicorn']
    
    for module in required_modules:
        try:
            if module == 'python-dotenv':
                importlib.import_module('dotenv')
            else:
                importlib.import_module(module)
            print(f"✓ {module} is installed")
        except ImportError:
            print(f"✗ {module} is NOT installed")

def check_file_access():
    """Check if critical files are accessible"""
    print("\n=== CHECKING FILE ACCESS ===")
    
    critical_files = [
        'app.py',
        'request.py',
        'run.py',
        'check.py',
        'wsgi.py',
        'static/index.html',
        'static/script.js',
        'static/style.css',
        'syllabi/python/index.json'
    ]
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for file in critical_files:
        file_path = os.path.join(base_dir, file)
        if os.path.exists(file_path):
            print(f"✓ {file} is accessible")
            # Check permissions
            try:
                with open(file_path, 'r') as f:
                    f.read(1)  # Try to read 1 byte
                print(f"  - File has read permissions")
            except Exception as e:
                print(f"  - ERROR reading file: {str(e)}")
        else:
            print(f"✗ {file} is NOT accessible")

def check_api_connection():
    """Check connection to the external API"""
    print("\n=== CHECKING API CONNECTION ===")
    
    # Try to import request.py to get the BASE_URL
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from request import BASE_URL, API_KEY
        
        if not API_KEY:
            print("ERROR: API_KEY is not set")
            return
            
        # Try a simple API request
        url = f"{BASE_URL}/health"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        
        try:
            response = requests.get(url, headers=headers, timeout=5)
            print(f"API response status: {response.status_code}")
            if response.status_code == 200:
                print("API connection successful")
            else:
                print(f"API connection failed: {response.text}")
        except Exception as e:
            print(f"Error connecting to API: {str(e)}")
            
    except Exception as e:
        print(f"Error importing request.py: {str(e)}")

def check_compilers():
    """Check if required compilers are installed"""
    print("\n=== CHECKING COMPILERS ===")
    
    # Check Python
    try:
        import subprocess
        result = subprocess.run(['python3', '--version'], capture_output=True, text=True)
        print(f"Python: {result.stdout.strip()}")
    except Exception as e:
        print(f"Error checking Python: {str(e)}")
    
    # Check Java
    try:
        result = subprocess.run(['javac', '-version'], capture_output=True, text=True)
        if result.stdout:
            print(f"Java: {result.stdout.strip()}")
        else:
            print(f"Java: {result.stderr.strip()}")
    except Exception as e:
        print(f"Error checking Java: {str(e)}")
    
    # Check C++
    try:
        result = subprocess.run(['g++', '--version'], capture_output=True, text=True)
        version_line = result.stdout.strip().split('\n')[0]
        print(f"C++: {version_line}")
    except Exception as e:
        print(f"Error checking C++: {str(e)}")

def test_flask_app():
    """Test the Flask app directly"""
    print("\n=== TESTING FLASK APP ===")
    
    try:
        # Import the Flask app
        from app import app
        
        # Create a test client
        client = app.test_client()
        
        # Test the index route
        response = client.get('/')
        if response.status_code == 200:
            print("✓ Flask app index route works")
        else:
            print(f"✗ Flask app index route failed: {response.status_code}")
        
        # Test the generate endpoint
        test_data = {
            "course": "Learnpython.org",
            "lesson": "Variables and Types"
        }
        
        try:
            response = client.post('/generate', 
                                  data=json.dumps(test_data),
                                  content_type='application/json')
            
            print(f"Generate endpoint status: {response.status_code}")
            if response.status_code == 200:
                print("✓ Generate endpoint works")
            else:
                print(f"✗ Generate endpoint failed: {response.status_code}")
                print(f"Response: {response.data.decode('utf-8')}")
        except Exception as e:
            print(f"Error testing generate endpoint: {str(e)}")
            traceback.print_exc()
            
    except Exception as e:
        print(f"Error importing Flask app: {str(e)}")
        traceback.print_exc()

def main():
    """Run all checks"""
    print("=== PROBLEM GENERATOR SERVER DIAGNOSTICS ===")
    print(f"Current directory: {os.getcwd()}")
    print(f"Script location: {os.path.dirname(os.path.abspath(__file__))}")
    
    check_environment()
    check_dependencies()
    check_file_access()
    check_api_connection()
    check_compilers()
    test_flask_app()
    
    print("\n=== DIAGNOSTICS COMPLETE ===")
    print("If you're still having issues, check the following:")
    print("1. Make sure your API_KEY is correct")
    print("2. Check if the API server is accessible from your server")
    print("3. Verify that all required directories exist and have proper permissions")
    print("4. Check if Nginx is properly configured to proxy requests to your Flask app")

if __name__ == "__main__":
    main()
