import pytest
import time
import os
import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

# Check if we should run actual UI tests or skip them
# Set this to True only when you have a server running on port 5000
RUN_LIVE_UI_TESTS = False

@pytest.fixture(scope="module")
def driver():
    """Set up and tear down the WebDriver for UI testing"""
    if not RUN_LIVE_UI_TESTS:
        pytest.skip("Live UI tests are disabled. Set RUN_LIVE_UI_TESTS=True to enable.")
        return None
        
    # Set up headless Chrome for testing
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Create a WebDriver instance
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        
        # Try connecting to the server to verify it's running
        try:
            driver.get("http://localhost:5000")
            WebDriverWait(driver, 5).until(EC.title_contains("Problem Generator"))
        except (TimeoutException, WebDriverException) as e:
            pytest.skip(f"Server not available at http://localhost:5000: {e}")
            driver.quit()
            return None
            
        yield driver
    finally:
        if 'driver' in locals() and driver:
            driver.quit()

class TestUIComponents:
    """
    UI tests for the Problem Generator application
    
    Tests user interface components and interactions using Selenium WebDriver.
    These tests require a running server on localhost:5000 to work properly.
    """
    
    def test_initial_page_load(self, driver):
        """Test that the initial page loads correctly"""
        driver.get("http://localhost:5000")
        
        # Wait for the page title to be correct
        WebDriverWait(driver, 10).until(EC.title_contains("Problem Generator"))
        
        # Verify key elements are present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "course-select")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "lesson-select")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "problem-module")))
        
        # Verify visible elements
        assert driver.find_element(By.ID, "course-select").is_displayed()
        assert driver.find_element(By.ID, "lesson-select").is_displayed()
        assert driver.find_element(By.ID, "title").is_displayed()
    
    def test_theme_toggle(self, driver):
        """Test that the theme toggle works correctly"""
        driver.get("http://localhost:5000")
        
        # Wait for page to load properly
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "theme-toggle-btn")))
        
        # Get the initial theme state
        body = driver.find_element(By.TAG_NAME, "body")
        initial_has_dark = "dark-mode" in body.get_attribute("class") if body.get_attribute("class") else False
        
        # Click the theme toggle button
        theme_toggle = driver.find_element(By.ID, "theme-toggle-btn")
        theme_toggle.click()
        
        # Wait for the theme to change (a short delay for the animation/JS to apply)
        time.sleep(1)
        
        # Check that the theme has changed
        body = driver.find_element(By.TAG_NAME, "body")
        new_has_dark = "dark-mode" in body.get_attribute("class") if body.get_attribute("class") else False
        
        assert initial_has_dark != new_has_dark, "Theme did not toggle after clicking the button"
    
    def test_language_selection(self, driver):
        """Test that the language selection works correctly"""
        driver.get("http://localhost:5000")
        
        # Wait for page to load completely
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "language-select")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "CodeMirror")))
        
        # Select the language dropdown
        language_select = driver.find_element(By.ID, "language-select")
        
        # Check initial language is Python
        assert language_select.get_attribute("value") == "python"
        
        # Change to Java
        language_select.click()
        java_option = driver.find_element(By.XPATH, "//select[@id='language-select']/option[@value='java']")
        java_option.click()
        
        # Check that language is now Java
        assert language_select.get_attribute("value") == "java"
        
        # Wait for CodeMirror to update its mode
        time.sleep(2)
        
        # Check that the CodeMirror mode has updated
        # Note: in some setups, this might require a different approach to verify the mode
        code_mirror_mode = driver.execute_script(
            "return document.querySelector('.CodeMirror').CodeMirror.getMode().name"
        )
        assert "java" in code_mirror_mode.lower() or "clike" in code_mirror_mode.lower()
    
    def test_chat_window_toggle(self, driver):
        """Test that the chat window toggle works correctly"""
        driver.get("http://localhost:5000")
        
        # Wait for elements to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "chat-window")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "chat-toggle-btn")))
        
        # Check if chat is initially hidden
        chat_window = driver.find_element(By.ID, "chat-window")
        initial_visibility = chat_window.is_displayed()
        
        # Click the chat toggle button
        chat_toggle = driver.find_element(By.ID, "chat-toggle-btn")
        chat_toggle.click()
        
        # Wait for animation
        time.sleep(1)
        
        # Chat window should have toggled visibility
        assert chat_window.is_displayed() != initial_visibility, "Chat window visibility did not toggle"
        
        # Toggle again
        chat_toggle.click()
        
        # Wait for animation
        time.sleep(1)
        
        # Should be back to initial state
        assert chat_window.is_displayed() == initial_visibility, "Chat window didn't return to initial state"
    
    def test_code_editor_functionality(self, driver):
        """Test that the code editor works correctly"""
        driver.get("http://localhost:5000")
        
        # Wait for editor to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "CodeMirror")))
        
        # Find the CodeMirror instance
        code_mirror = driver.find_element(By.CLASS_NAME, "CodeMirror")
        
        # CodeMirror has a complex structure, so we need to use JavaScript to set its value
        test_code = "def hello_world():\n    print('Hello, World!')\n\nhello_world()"
        driver.execute_script(
            "if (arguments[0].CodeMirror) arguments[0].CodeMirror.setValue(arguments[1]);", 
            code_mirror, 
            test_code
        )
        
        # Verify the code was set
        actual_code = driver.execute_script(
            "return arguments[0].CodeMirror ? arguments[0].CodeMirror.getValue() : '';", 
            code_mirror
        )
        
        assert actual_code == test_code, "Code editor didn't properly set the test code"
        
        # Test running the code (requires backend to be running)
        run_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "run-btn"))
        )
        run_btn.click()
        
        # Wait for the console to be displayed
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "console"))
        )
        
        # Since the actual output depends on the backend, just verify the console is shown
        console = driver.find_element(By.ID, "console")
        assert console.is_displayed(), "Console should be visible after running code"
