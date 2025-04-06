#!/usr/bin/env python
"""
Automated Test Scenarios for Problem Generator

This script runs predefined test scenarios that combine multiple test types
to validate entire workflows in the application.
"""

import os
import sys
import subprocess
import argparse
import tempfile
import time
from pathlib import Path

# Add parent directory to path to import application modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tests.setup_test_env import setup_test_database, verify_dependencies

# Test scenarios definitions
SCENARIOS = {
    "problem-generation": {
        "description": "Tests the full problem generation workflow",
        "components": ["github_utils.py", "app.py"],
        "tests": [
            "tests/unit/test_github_utils.py",
            "tests/api/test_api_endpoints.py::TestAPIEndpoints::test_generate_problem"
        ]
    },
    "code-execution": {
        "description": "Tests the code execution and validation workflow",
        "components": ["app.py", "check.py"],
        "tests": [
            "tests/api/test_api_endpoints.py::TestAPIEndpoints::test_run_code_endpoint",
            "tests/api/test_api_endpoints.py::TestAPIEndpoints::test_check_code_endpoint"
        ]
    },
    "database": {
        "description": "Tests all database operations",
        "components": ["db.py"],
        "tests": [
            "tests/integration/test_db_integration.py"
        ]
    },
    "ui-components": {
        "description": "Tests UI components and interactions",
        "components": ["static/script.js", "static/index.html"],
        "tests": [
            "tests/ui/test_ui_components.py"
        ]
    },
    "full-app": {
        "description": "Tests the entire application",
        "components": ["app.py", "db.py", "github_utils.py", "check.py", "static/*"],
        "tests": [
            "tests/unit/",
            "tests/integration/",
            "tests/api/"
        ]
    }
}

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Run automated test scenarios for Problem Generator")
    parser.add_argument(
        "scenario",
        nargs="?",
        choices=list(SCENARIOS.keys()) + ["list"],
        default="list",
        help="Test scenario to run (or 'list' to show available scenarios)"
    )
    parser.add_argument(
        "--no-coverage",
        action="store_true",
        help="Disable coverage measurement"
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open reports in browser after tests complete"
    )
    parser.add_argument(
        "--server",
        action="store_true",
        help="Start a test server before running UI tests"
    )
    parser.add_argument(
        "--server-port",
        type=int,
        default=5000,
        help="Port for the test server (default: 5000)"
    )
    
    return parser.parse_args()

def list_scenarios():
    """List all available test scenarios"""
    print("Available Test Scenarios:")
    print("-------------------------")
    for name, scenario in SCENARIOS.items():
        print(f"- {name}: {scenario['description']}")
        print(f"  Components: {', '.join(scenario['components'])}")
        print(f"  Tests: {len(scenario['tests'])} test files/cases")
        print()

def start_test_server(port=5000):
    """Start a test server for UI tests"""
    import threading
    import app
    
    def run_server():
        app.app.run(port=port, debug=False)
    
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for server to start
    print(f"Starting test server on port {port}...")
    time.sleep(2)
    
    return server_thread

def run_scenario(scenario_name, coverage=True, open_browser=False, start_server=False, server_port=5000):
    """
    Run a predefined test scenario
    
    Args:
        scenario_name: Name of the scenario to run
        coverage: Whether to measure code coverage
        open_browser: Whether to open reports in browser
        start_server: Whether to start a test server for UI tests
        server_port: Port for the test server
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    if scenario_name not in SCENARIOS:
        print(f"Error: Scenario '{scenario_name}' not found")
        return 1
    
    scenario = SCENARIOS[scenario_name]
    print(f"Running scenario: {scenario_name}")
    print(f"Description: {scenario['description']}")
    print(f"Components: {', '.join(scenario['components'])}")
    print(f"Tests: {len(scenario['tests'])} test files/cases")
    print()
    
    # Set up a test database
    db_path = setup_test_database()
    print(f"Using test database: {db_path}")
    
    # Start test server if needed
    server_thread = None
    if start_server:
        server_thread = start_test_server(server_port)
        print(f"Test server running at http://localhost:{server_port}")
    
    # Set up command for running tests
    cmd = [sys.executable, "run_tests.py", "--verbose"]
    
    # Add test paths
    for test in scenario["tests"]:
        cmd.extend(["--path", test])
    
    # Add other options
    if not coverage:
        cmd.append("--no-coverage")
    if open_browser:
        cmd.append("--open")
    
    # Add database path
    cmd.extend(["--db-path", db_path])
    
    # Run the tests
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    # Clean up
    if os.path.exists(db_path):
        try:
            os.unlink(db_path)
        except:
            pass
    
    return result.returncode

def main():
    """Main entry point"""
    args = parse_args()
    
    # Verify dependencies first
    if not verify_dependencies():
        return 1
    
    # List scenarios and exit if requested
    if args.scenario == "list":
        list_scenarios()
        return 0
    
    # Run the specified scenario
    return run_scenario(
        scenario_name=args.scenario,
        coverage=not args.no_coverage,
        open_browser=args.open,
        start_server=args.server,
        server_port=args.server_port
    )

if __name__ == "__main__":
    sys.exit(main())
