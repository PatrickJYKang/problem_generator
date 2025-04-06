#!/usr/bin/env python
"""
Test Runner for Problem Generator

This script runs the test suite and generates enhanced reports.
"""

import os
import sys
import subprocess
import argparse
import datetime
import webbrowser
from pathlib import Path

# Add parent directory to path to import test utilities
sys.path.insert(0, os.path.dirname(__file__))
from tests.utils.report_generator import TestReportGenerator

def setup_report_directory():
    """Create the reports directory if it doesn't exist"""
    reports_dir = os.path.join(os.path.dirname(__file__), 'test_reports')
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    return reports_dir

def run_tests(test_path=None, html_report=True, xml_report=True, coverage=True, 
              open_browser=False, db_path=None, verbose=False):
    """
    Run the test suite and generate reports
    
    Args:
        test_path: Optional path to specific tests to run
        html_report: Whether to generate HTML reports
        xml_report: Whether to generate XML reports
        coverage: Whether to measure code coverage
        open_browser: Whether to open reports in browser automatically
        db_path: Optional path to test database
        verbose: Whether to enable verbose output
    
    Returns:
        The exit code from pytest
    """
    reports_dir = setup_report_directory()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Base command for pytest
    cmd = ["pytest"]
    if verbose:
        cmd.append("-v")
    
    # Add test path if specified
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append("tests/")
    
    # Add HTML report option
    html_report_path = None
    if html_report:
        html_report_path = os.path.join(reports_dir, f"report_{timestamp}.html")
        cmd.extend(["--html="+html_report_path])
    
    # Add JUnit XML report option (for CI integration)
    xml_report_path = None
    if xml_report:
        xml_report_path = os.path.join(reports_dir, f"report_{timestamp}.xml")
        cmd.extend(["--junitxml="+xml_report_path])
    
    # Add coverage options
    cov_xml_path = None
    if coverage:
        cmd.extend(["--cov=.", "--cov-branch"])
        if html_report:
            cov_report_path = os.path.join(reports_dir, f"coverage_{timestamp}")
            cmd.extend(["--cov-report=html:" + cov_report_path])
        if xml_report:
            cov_xml_path = os.path.join(reports_dir, f"coverage_{timestamp}.xml")
            cmd.extend(["--cov-report=xml:" + cov_xml_path])
    
    # Set environment variables if db_path is provided
    env = os.environ.copy()
    if db_path:
        env["DB_PATH"] = db_path
    
    # Print the command being run
    print(f"Running: {' '.join(cmd)}")
    
    # Run the tests
    result = subprocess.run(cmd, env=env)
    
    # Generate enhanced report
    report_generator = TestReportGenerator(reports_dir)
    summary_path = report_generator.generate_report(
        coverage_path=cov_xml_path,
        results_path=xml_report_path
    )
    
    # Print results summary
    if result.returncode == 0:
        print("\n✅ Test execution successful!")
    else:
        print("\n❌ Test execution failed!")
    
    # Print report locations
    summary_html = Path(reports_dir) / f"summary_{timestamp}.html"
    print(f"\nReports:")
    print(f"📊 Enhanced Summary: {summary_html}")
    if html_report and html_report_path:
        print(f"📄 HTML Report: {html_report_path}")
    if coverage:
        print(f"📈 Coverage Report: {cov_report_path}/index.html")
    
    # Open browser if requested
    if open_browser and os.path.exists(summary_html):
        print(f"\nOpening summary report in browser...")
        webbrowser.open(f"file://{os.path.abspath(summary_html)}")
    
    return result.returncode

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Run tests for Problem Generator")
    parser.add_argument(
        "--path", 
        help="Path to specific tests to run (e.g., tests/unit/)"
    )
    parser.add_argument(
        "--no-html", 
        action="store_true", 
        help="Disable HTML report generation"
    )
    parser.add_argument(
        "--no-xml", 
        action="store_true", 
        help="Disable XML report generation"
    )
    parser.add_argument(
        "--no-coverage", 
        action="store_true", 
        help="Disable coverage measurement"
    )
    parser.add_argument(
        "--unit", 
        action="store_true", 
        help="Run only unit tests"
    )
    parser.add_argument(
        "--integration", 
        action="store_true", 
        help="Run only integration tests"
    )
    parser.add_argument(
        "--api", 
        action="store_true", 
        help="Run only API tests"
    )
    parser.add_argument(
        "--ui", 
        action="store_true", 
        help="Run only UI tests"
    )
    parser.add_argument(
        "--db-path",
        help="Path to test database"
    )
    parser.add_argument(
        "--setup-db",
        action="store_true",
        help="Set up a test database before running tests"
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open reports in browser after tests complete"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    test_path = args.path
    
    # Handle specific test category flags
    if args.unit:
        test_path = "tests/unit/"
    elif args.integration:
        test_path = "tests/integration/"
    elif args.api:
        test_path = "tests/api/"
    elif args.ui:
        test_path = "tests/ui/"
    
    # Set up a test database if requested
    db_path = args.db_path
    if args.setup_db:
        from tests.setup_test_env import setup_test_database
        db_path = setup_test_database(db_path)
        print(f"Using test database: {db_path}")
    
    # Run the tests
    exit_code = run_tests(
        test_path=test_path,
        html_report=not args.no_html,
        xml_report=not args.no_xml,
        coverage=not args.no_coverage,
        open_browser=args.open,
        db_path=db_path,
        verbose=args.verbose
    )
    
    sys.exit(exit_code)
