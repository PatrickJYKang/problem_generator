#!/usr/bin/env python
"""
Test Environment Setup Script

This script prepares the test environment by:
1. Creating necessary test data
2. Setting up a test database
3. Verifying dependencies
"""

import os
import sys
import tempfile
import subprocess
import argparse
from pathlib import Path

# Add the parent directory to the path so we can import app modules
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

import db
from tests.utils.test_data import generate_test_database

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Set up test environment for Problem Generator")
    parser.add_argument(
        "--db-path", 
        help="Path to test database (default: temporary file)",
        default=None
    )
    parser.add_argument(
        "--problems", 
        type=int,
        help="Number of test problems to generate (default: 5)",
        default=5
    )
    parser.add_argument(
        "--solutions", 
        type=int,
        help="Number of solutions per problem (default: 2)",
        default=2
    )
    parser.add_argument(
        "--verify-deps", 
        action="store_true",
        help="Verify dependencies are installed"
    )
    
    return parser.parse_args()

def setup_test_database(db_path=None, num_problems=5, solutions_per_problem=2):
    """
    Set up a test database with sample data
    
    Args:
        db_path: Path to the database file (default: temporary file)
        num_problems: Number of test problems to generate
        solutions_per_problem: Number of solutions per problem
    
    Returns:
        Path to the database file
    """
    # If no db_path is provided, create a temporary file
    if db_path is None:
        fd, db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
    
    print(f"Setting up test database at: {db_path}")
    
    # Override the database path
    original_db_path = db.DATABASE
    db.DATABASE = db_path
    
    try:
        # Initialize the database
        db.init_db()
        
        # Generate test data
        problems, solutions = generate_test_database(
            num_problems=num_problems, 
            solutions_per_problem=solutions_per_problem
        )
        
        # Insert problems
        for problem in problems:
            # Extract the ID before storing (store_problem will assign a new ID)
            problem_id = problem.pop("id")
            
            # Store the problem and verify it gets the expected ID
            stored_id = db.store_problem(
                title=problem["title"],
                problem=problem["problem"],
                testcases=problem["testcases"],
                course=problem["course"],
                lesson=problem["lesson"],
                language=problem["language"]
            )
            
            # Verify ID matches expected
            if stored_id != problem_id:
                print(f"Warning: Expected problem ID {problem_id}, got {stored_id}")
        
        # Insert solutions
        for solution in solutions:
            # Store the solution
            db.store_solution(
                problem_id=solution["problem_id"],
                language=solution["language"],
                solution=solution["solution"],
                passed=solution["passed"],
                total=solution["total"]
            )
        
        print(f"Successfully populated test database with {len(problems)} problems and {len(solutions)} solutions")
        
        # Verify data
        conn = db.get_db_connection()
        problems_in_db = conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0]
        solutions_in_db = conn.execute("SELECT COUNT(*) FROM solutions").fetchone()[0]
        conn.close()
        
        print(f"Verification: Database contains {problems_in_db} problems and {solutions_in_db} solutions")
        
        return db_path
    
    finally:
        # Restore the original database path
        db.DATABASE = original_db_path

def verify_dependencies():
    """Verify that all required dependencies are installed"""
    required_packages = [
        "pytest", 
        "pytest-cov", 
        "pytest-html", 
        "pytest-mock", 
        "selenium", 
        "requests-mock", 
        "flask",
        "coverage"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"ERROR: Missing dependencies: {', '.join(missing_packages)}")
        print("Install the missing dependencies with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("All dependencies verified successfully")
    return True

def main():
    """Main entry point"""
    args = parse_args()
    
    if args.verify_deps:
        if not verify_dependencies():
            sys.exit(1)
    
    # Set up the test database
    db_path = setup_test_database(
        db_path=args.db_path,
        num_problems=args.problems,
        solutions_per_problem=args.solutions
    )
    
    print(f"\nTest environment set up successfully.")
    print(f"Test database: {db_path}")
    
    # Provide helpful instructions
    print("\nTo run tests with this database:")
    print(f"DB_PATH={db_path} pytest tests/")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
