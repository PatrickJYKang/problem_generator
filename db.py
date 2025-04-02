import os
import sqlite3
import json
from datetime import datetime

# Database configuration
DB_DIRECTORY = '/var/lib/problem_generator/'
DB_PATH = os.path.join(DB_DIRECTORY, 'problem_generator.db')

# Ensure the database directory exists
os.makedirs(DB_DIRECTORY, exist_ok=True)

def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Returns rows as dictionaries
    return conn

def init_db():
    """Initialize the database with the required schema."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create problems table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        problem_text TEXT NOT NULL,
        course TEXT NOT NULL,
        lesson TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create testcases table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS testcases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id INTEGER NOT NULL,
        input TEXT,
        expected_output TEXT NOT NULL,
        FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE CASCADE
    )
    ''')

    # Create solutions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS solutions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id INTEGER NOT NULL,
        language TEXT NOT NULL,
        code TEXT NOT NULL,
        passed_testcases INTEGER NOT NULL,
        total_testcases INTEGER NOT NULL,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (problem_id) REFERENCES problems(id)
    )
    ''')

    # Enable foreign keys
    cursor.execute('PRAGMA foreign_keys = ON')

    conn.commit()
    conn.close()

def store_problem(title, problem_text, course, lesson, testcases):
    """
    Store a newly generated problem and its testcases.
    
    Args:
        title (str): Problem title
        problem_text (str): Markdown content of the problem
        course (str): Course identifier
        lesson (str): Lesson identifier
        testcases (list): List of testcase objects with input/expected_output fields
        
    Returns:
        int: ID of the inserted problem
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert the problem
    cursor.execute(
        'INSERT INTO problems (title, problem_text, course, lesson) VALUES (?, ?, ?, ?)',
        (title, problem_text, course, lesson)
    )
    problem_id = cursor.lastrowid
    
    # Insert each testcase
    for tc in testcases:
        cursor.execute(
            'INSERT INTO testcases (problem_id, input, expected_output) VALUES (?, ?, ?)',
            (problem_id, tc.get('input', ''), tc['expected_output'])
        )
    
    conn.commit()
    conn.close()
    
    return problem_id

def store_solution(problem_id, language, code, passed_testcases, total_testcases):
    """
    Store a solution attempt.
    
    Args:
        problem_id (int): ID of the problem being solved
        language (str): Programming language used ('python', 'java', 'cpp')
        code (str): Source code of the solution
        passed_testcases (int): Number of testcases passed
        total_testcases (int): Total number of testcases
        
    Returns:
        int: ID of the inserted solution
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO solutions (problem_id, language, code, passed_testcases, total_testcases) VALUES (?, ?, ?, ?, ?)',
        (problem_id, language, code, passed_testcases, total_testcases)
    )
    solution_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return solution_id

def get_problem_by_id(problem_id):
    """
    Retrieve a problem by its ID.
    
    Args:
        problem_id (int): ID of the problem to retrieve
        
    Returns:
        dict: Problem data with testcases or None if not found
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get problem data
    cursor.execute('SELECT * FROM problems WHERE id = ?', (problem_id,))
    problem = cursor.fetchone()
    
    if not problem:
        conn.close()
        return None
    
    # Convert to dictionary
    problem_dict = dict(problem)
    
    # Get testcases
    cursor.execute('SELECT input, expected_output FROM testcases WHERE problem_id = ?', (problem_id,))
    testcases = [dict(tc) for tc in cursor.fetchall()]
    problem_dict['testcases'] = testcases
    
    conn.close()
    return problem_dict

def get_problems_by_lesson(course, lesson):
    """
    Get all problems for a specific course and lesson.
    
    Args:
        course (str): Course identifier
        lesson (str): Lesson identifier
        
    Returns:
        list: List of problem dictionaries (without testcases)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'SELECT id, title, created_at FROM problems WHERE course = ? AND lesson = ? ORDER BY created_at DESC',
        (course, lesson)
    )
    problems = [dict(p) for p in cursor.fetchall()]
    
    conn.close()
    return problems

def get_solutions_for_problem(problem_id):
    """
    Get all solutions for a specific problem.
    
    Args:
        problem_id (int): ID of the problem
        
    Returns:
        list: List of solution dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'SELECT * FROM solutions WHERE problem_id = ? ORDER BY submitted_at DESC',
        (problem_id,)
    )
    solutions = [dict(s) for s in cursor.fetchall()]
    
    conn.close()
    return solutions

# Initialize the database when this module is imported
init_db()
