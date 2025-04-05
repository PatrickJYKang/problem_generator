import os
import sqlite3
import json
import logging
import traceback
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database configuration
DB_DIRECTORY = '/var/lib/problem_generator/'
DB_PATH = os.path.join(DB_DIRECTORY, 'problem_generator.db')

try:
    # Ensure the database directory exists
    os.makedirs(DB_DIRECTORY, exist_ok=True)
    logger.info(f"Database directory confirmed: {DB_DIRECTORY}")
    
    # Verify we can write to the directory
    test_file_path = os.path.join(DB_DIRECTORY, 'test_write.tmp')
    with open(test_file_path, 'w') as f:
        f.write('test')
    os.remove(test_file_path)
    logger.info("Successfully verified write permissions to database directory")
except Exception as e:
    logger.error(f"Error setting up database directory: {str(e)}")
    logger.error(traceback.format_exc())
    
    # Fall back to a directory we know should work
    fallback_dir = os.path.dirname(os.path.abspath(__file__))
    DB_DIRECTORY = os.path.join(fallback_dir, 'data')
    DB_PATH = os.path.join(DB_DIRECTORY, 'problem_generator.db')
    
    logger.warning(f"Falling back to alternative database location: {DB_DIRECTORY}")
    os.makedirs(DB_DIRECTORY, exist_ok=True)

def get_db_connection():
    """Create a connection to the SQLite database."""
    try:
        logger.info(f"Connecting to database at {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Returns rows as dictionaries
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def init_db():
    """Initialize the database with the required schema."""
    try:
        logger.info("Initializing database...")
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
        
        # Check if the language column exists, and add it if not
        cursor.execute("PRAGMA table_info(problems)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'language' not in columns:
            logger.info("Adding 'language' column to problems table")
            cursor.execute('ALTER TABLE problems ADD COLUMN language TEXT')

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
        logger.info("Database schema created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        logger.error(traceback.format_exc())
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def store_problem(title, problem_text, course, lesson, testcases, language=None):
    """
    Store a newly generated problem and its testcases.
    
    Args:
        title (str): Problem title
        problem_text (str): Markdown content of the problem
        course (str): Course identifier
        lesson (str): Lesson identifier
        testcases (list): List of testcase objects with input/expected_output fields
        language (str, optional): Programming language for the problem. If None, determined from course.
        
    Returns:
        int: ID of the inserted problem
    """
    logger.info(f"Storing problem: '{title}' for course '{course}', lesson '{lesson}'")
    logger.info(f"Problem text length: {len(problem_text)} chars")
    logger.info(f"Testcases: {len(testcases)} cases")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Determine language based on course if not provided
        if not language:
            if 'python' in course.lower():
                language = 'python'
            elif 'java' in course.lower():
                language = 'java'
            elif 'cpp' in course.lower() or 'c++' in course.lower():
                language = 'cpp'
            else:
                language = 'python'  # Default to Python if we can't determine
        
        # Insert the problem
        cursor.execute(
            'INSERT INTO problems (title, problem_text, course, lesson, language) VALUES (?, ?, ?, ?, ?)',
            (title, problem_text, course, lesson, language)
        )
        problem_id = cursor.lastrowid
        logger.info(f"Inserted problem with ID: {problem_id}")
        
        # Insert each testcase
        for i, tc in enumerate(testcases):
            try:
                input_val = tc.get('input', '')
                output_val = tc.get('expected_output', '')
                
                if not output_val and 'output' in tc:  # Handle alternate field name
                    output_val = tc.get('output', '')
                
                if not output_val:
                    logger.warning(f"Testcase {i} missing expected_output, data: {tc}")
                    continue
                
                cursor.execute(
                    'INSERT INTO testcases (problem_id, input, expected_output) VALUES (?, ?, ?)',
                    (problem_id, input_val, output_val)
                )
                logger.debug(f"Inserted testcase {i} for problem {problem_id}")
            except Exception as e:
                logger.error(f"Error inserting testcase {i}: {str(e)}")
                # Continue with other testcases
        
        conn.commit()
        conn.close()
        logger.info(f"Successfully stored problem ID {problem_id} with {len(testcases)} testcases")
        return problem_id
    except Exception as e:
        logger.error(f"Error storing problem: {str(e)}")
        logger.error(traceback.format_exc())
        return None

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

def get_problems(limit=50):
    """
    Get all problems across all courses and lessons, with optional limit.
    
    Args:
        limit (int): Maximum number of problems to return (default: 50)
        
    Returns:
        list: List of problem dictionaries (without testcases)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'SELECT id, title, course, lesson, language, created_at FROM problems ORDER BY created_at DESC LIMIT ?',
        (limit,)
    )
    problems = [dict(p) for p in cursor.fetchall()]
    
    conn.close()
    return problems

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

def delete_problem(problem_id):
    """
    Delete a problem and all its associated data (testcases and solutions).
    
    Args:
        problem_id (int): ID of the problem to delete
        
    Returns:
        bool: True if the problem was deleted successfully, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if the problem exists
        cursor.execute('SELECT id FROM problems WHERE id = ?', (problem_id,))
        problem = cursor.fetchone()
        
        if not problem:
            logger.warning(f"Attempted to delete non-existent problem ID: {problem_id}")
            conn.close()
            return False
        
        # Due to foreign key constraints, deleting the problem should cascade
        # to delete associated testcases, but let's explicitly delete everything
        # to ensure we don't leave orphaned records
        
        # Delete testcases
        cursor.execute('DELETE FROM testcases WHERE problem_id = ?', (problem_id,))
        testcases_deleted = cursor.rowcount
        logger.info(f"Deleted {testcases_deleted} testcases for problem {problem_id}")
        
        # Delete solutions
        cursor.execute('DELETE FROM solutions WHERE problem_id = ?', (problem_id,))
        solutions_deleted = cursor.rowcount
        logger.info(f"Deleted {solutions_deleted} solutions for problem {problem_id}")
        
        # Delete the problem itself
        cursor.execute('DELETE FROM problems WHERE id = ?', (problem_id,))
        problem_deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        if problem_deleted:
            logger.info(f"Successfully deleted problem ID: {problem_id}")
        else:
            logger.warning(f"Failed to delete problem ID: {problem_id}")
            
        return problem_deleted
    except Exception as e:
        logger.error(f"Error deleting problem {problem_id}: {str(e)}")
        logger.error(traceback.format_exc())
        if 'conn' in locals():
            conn.close()
        return False

def populate_language_column():
    """
    One-time function to populate the language column in the problems table
    based on the course value for each problem.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all problems without a language set
        cursor.execute('SELECT id, course FROM problems WHERE language IS NULL')
        problems = cursor.fetchall()
        
        updates = 0
        for problem in problems:
            problem_id = problem['id']
            course = problem['course']
            
            # Determine language based on course
            language = None
            if 'python' in course.lower():
                language = 'python'
            elif 'java' in course.lower():
                language = 'java'
            elif 'cpp' in course.lower() or 'c++' in course.lower():
                language = 'cpp'
            else:
                language = 'python'  # Default to python
            
            # Update the problem with the determined language
            cursor.execute(
                'UPDATE problems SET language = ? WHERE id = ?',
                (language, problem_id)
            )
            updates += 1
        
        conn.commit()
        conn.close()
        logger.info(f"Updated language for {updates} problems")
        return updates
    except Exception as e:
        logger.error(f"Error populating language column: {str(e)}")
        logger.error(traceback.format_exc())
        if 'conn' in locals():
            conn.close()
        return 0

# Initialize the database when this module is imported
init_db()

# Now run the populate function to fill in language data for existing records
populate_language_column()
