"""
Test Report Generator

This module provides utilities for generating enhanced test reports
beyond what pytest provides by default.
"""

import os
import sys
import json
import datetime
import platform
import subprocess
from pathlib import Path
import pkg_resources

class TestReportGenerator:
    """
    Generates detailed test reports with system information and coverage data.
    """
    
    def __init__(self, report_dir="test_reports"):
        """
        Initialize the report generator
        
        Args:
            report_dir: Directory to store reports
        """
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(exist_ok=True, parents=True)
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.system_info = self._collect_system_info()
        self.dependency_info = self._collect_dependency_info()
    
    def _collect_system_info(self):
        """Collect system information for the report"""
        return {
            "python_version": sys.version,
            "platform": platform.platform(),
            "processor": platform.processor(),
            "machine": platform.machine(),
            "python_implementation": platform.python_implementation(),
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def _collect_dependency_info(self):
        """Collect information about installed packages"""
        return {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    
    def _read_coverage_data(self, coverage_path):
        """Read coverage data from a coverage.xml file if it exists"""
        if not os.path.exists(coverage_path):
            return None
        
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(coverage_path)
            root = tree.getroot()
            
            # Extract summary statistics
            coverage = root.get('line-rate', '0')
            coverage_percent = float(coverage) * 100
            
            # Get coverage by package
            packages = []
            for package in root.findall('.//package'):
                package_name = package.get('name', 'unknown')
                package_coverage = float(package.get('line-rate', '0')) * 100
                packages.append({
                    "name": package_name,
                    "coverage": package_coverage
                })
            
            return {
                "overall": coverage_percent,
                "packages": packages
            }
        except Exception as e:
            print(f"Error reading coverage data: {str(e)}")
            return None
    
    def _read_test_results(self, results_path):
        """Read test results from a junit XML file if it exists"""
        if not os.path.exists(results_path):
            return None
        
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(results_path)
            root = tree.getroot()
            
            # Get overall test statistics
            tests = int(root.get('tests', '0'))
            failures = int(root.get('failures', '0'))
            errors = int(root.get('errors', '0'))
            skipped = int(root.get('skipped', '0'))
            time = float(root.get('time', '0'))
            
            # Get individual test cases
            test_cases = []
            for testcase in root.findall('.//testcase'):
                case = {
                    "name": testcase.get('name', 'unknown'),
                    "classname": testcase.get('classname', 'unknown'),
                    "time": float(testcase.get('time', '0')),
                    "status": "passed"
                }
                
                # Check for failures
                failure = testcase.find('failure')
                if failure is not None:
                    case["status"] = "failed"
                    case["message"] = failure.get('message', '')
                
                # Check for errors
                error = testcase.find('error')
                if error is not None:
                    case["status"] = "error"
                    case["message"] = error.get('message', '')
                
                # Check for skipped
                skipped = testcase.find('skipped')
                if skipped is not None:
                    case["status"] = "skipped"
                    case["message"] = skipped.get('message', '')
                
                test_cases.append(case)
            
            return {
                "summary": {
                    "tests": tests,
                    "failures": failures,
                    "errors": errors,
                    "skipped": skipped,
                    "time": time
                },
                "test_cases": test_cases
            }
        except Exception as e:
            print(f"Error reading test results: {str(e)}")
            return None
    
    def generate_report(self, coverage_path=None, results_path=None):
        """
        Generate a comprehensive report combining multiple data sources
        
        Args:
            coverage_path: Path to coverage.xml file
            results_path: Path to junit xml results file
        
        Returns:
            Path to the generated report file
        """
        report_data = {
            "system_info": self.system_info,
            "dependencies": self.dependency_info,
            "timestamp": self.timestamp,
            "coverage": self._read_coverage_data(coverage_path) if coverage_path else None,
            "test_results": self._read_test_results(results_path) if results_path else None
        }
        
        # Save the report as JSON
        report_file = self.report_dir / f"report_{self.timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        # Generate an HTML summary
        html_file = self.report_dir / f"summary_{self.timestamp}.html"
        self._generate_html_summary(report_data, html_file)
        
        return report_file
    
    def _generate_html_summary(self, report_data, html_file):
        """
        Generate an HTML summary of the test report
        
        Args:
            report_data: The report data as a dictionary
            html_file: Path to save the HTML report
        """
        # Get the summary data
        system_info = report_data["system_info"]
        dependencies = report_data["dependencies"]
        coverage = report_data["coverage"]
        test_results = report_data["test_results"]
        
        # Generate the HTML content
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Problem Generator Test Report</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }
                h1, h2, h3 {
                    color: #2c3e50;
                }
                .summary {
                    display: flex;
                    justify-content: space-between;
                    flex-wrap: wrap;
                    margin-bottom: 30px;
                }
                .summary-box {
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 15px;
                    margin: 10px 0;
                    width: calc(33% - 22px);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .passed {
                    background-color: #e8f5e9;
                    border-left: 5px solid #4caf50;
                }
                .failed {
                    background-color: #ffebee;
                    border-left: 5px solid #f44336;
                }
                .skipped {
                    background-color: #fff8e1;
                    border-left: 5px solid #ffca28;
                }
                .coverage {
                    background-color: #e3f2fd;
                    border-left: 5px solid #2196f3;
                }
                .coverage-bar {
                    height: 20px;
                    background-color: #ddd;
                    border-radius: 10px;
                    margin-top: 10px;
                }
                .coverage-progress {
                    height: 100%;
                    background-color: #4caf50;
                    border-radius: 10px;
                    text-align: center;
                    color: white;
                    line-height: 20px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
                tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                .test-passed {
                    color: #4caf50;
                    font-weight: bold;
                }
                .test-failed {
                    color: #f44336;
                    font-weight: bold;
                }
                .test-skipped {
                    color: #ff9800;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <h1>Problem Generator Test Report</h1>
            <p>Generated on: """ + system_info["timestamp"] + """</p>
            
            <h2>Summary</h2>
            <div class="summary">
        """
        
        # Add test summary box if available
        if test_results:
            summary = test_results["summary"]
            status = "passed" if summary["failures"] == 0 and summary["errors"] == 0 else "failed"
            html_content += f"""
                <div class="summary-box {status}">
                    <h3>Test Results</h3>
                    <p>Total Tests: {summary["tests"]}</p>
                    <p>Passed: {summary["tests"] - (summary["failures"] or 0) - (summary["errors"] or 0) - (summary["skipped"] or 0)}</p>
                    <p>Failed: {summary["failures"] or 0}</p>
                    <p>Errors: {summary["errors"] or 0}</p>
                    <p>Skipped: {summary["skipped"] or 0}</p>
                    <p>Total Time: {summary["time"]:.2f}s</p>
                </div>
            """
        
        # Add coverage summary box if available
        if coverage:
            html_content += f"""
                <div class="summary-box coverage">
                    <h3>Code Coverage</h3>
                    <p>Overall Coverage: {coverage["overall"]:.2f}%</p>
                    <div class="coverage-bar">
                        <div class="coverage-progress" style="width: {coverage["overall"]}%;">{coverage["overall"]:.2f}%</div>
                    </div>
                </div>
            """
        
        # Add system info box
        html_content += f"""
                <div class="summary-box">
                    <h3>System Information</h3>
                    <p>Python: {system_info["python_version"].split()[0]}</p>
                    <p>Platform: {system_info["platform"]}</p>
                    <p>Machine: {system_info["machine"]}</p>
                </div>
            </div>
        """
        
        # Add test details if available
        if test_results and test_results["test_cases"]:
            html_content += """
            <h2>Test Details</h2>
            <table>
                <tr>
                    <th>Test Name</th>
                    <th>Class</th>
                    <th>Status</th>
                    <th>Time (s)</th>
                </tr>
            """
            
            for test_case in test_results["test_cases"]:
                status_class = f"test-{test_case['status']}"
                html_content += f"""
                <tr>
                    <td>{test_case["name"]}</td>
                    <td>{test_case["classname"]}</td>
                    <td class="{status_class}">{test_case["status"].upper()}</td>
                    <td>{test_case["time"]:.3f}</td>
                </tr>
                """
            
            html_content += """
            </table>
            """
        
        # Add coverage details if available
        if coverage and coverage["packages"]:
            html_content += """
            <h2>Coverage by Package</h2>
            <table>
                <tr>
                    <th>Package</th>
                    <th>Coverage</th>
                </tr>
            """
            
            for package in coverage["packages"]:
                html_content += f"""
                <tr>
                    <td>{package["name"]}</td>
                    <td>
                        <div class="coverage-bar">
                            <div class="coverage-progress" style="width: {package["coverage"]}%;">{package["coverage"]:.2f}%</div>
                        </div>
                    </td>
                </tr>
                """
            
            html_content += """
            </table>
            """
        
        # Add dependencies
        html_content += """
            <h2>Dependencies</h2>
            <table>
                <tr>
                    <th>Package</th>
                    <th>Version</th>
                </tr>
        """
        
        for package, version in dependencies.items():
            html_content += f"""
                <tr>
                    <td>{package}</td>
                    <td>{version}</td>
                </tr>
            """
        
        html_content += """
            </table>
        </body>
        </html>
        """
        
        # Write the HTML file
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        return html_file
