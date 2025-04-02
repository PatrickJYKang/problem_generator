// DOM elements
const generateBtn    = document.getElementById("generate-btn");
const checkAnswerBtn = document.getElementById("check-answer-btn");
const retryBtn       = document.getElementById("retry-btn");
const runBtn         = document.getElementById("run-btn");
const resetBtn       = document.getElementById("reset-btn");
const courseSelect   = document.getElementById("course-select");
const lessonSelect   = document.getElementById("lesson-select");
const languageSelect = document.getElementById("language-select");
const titleHeader    = document.getElementById("title");
const resultDiv      = document.getElementById("result");
const resultsDiv     = document.getElementById("results");
const inputContainer = document.getElementById("input-container");
const inputEditor    = document.getElementById("input-editor");
const consoleDiv     = document.getElementById("console");
const themeToggleBtn = document.getElementById("theme-toggle-btn");
const themeIcon      = document.getElementById("theme-icon");

// CodeMirror editor setup
let codeEditor;

// Theme management
function initializeTheme() {
  // Check for saved theme preference or use light mode as default
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
  } else {
    // Default to light mode
    document.documentElement.setAttribute('data-theme', 'light');
    updateThemeIcon('light');
    localStorage.setItem('theme', 'light');
  }
}

function updateThemeIcon(theme) {
  themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
}

function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  updateThemeIcon(newTheme);
  
  // Update CodeMirror theme if editor is initialized
  if (codeEditor) {
    codeEditor.setOption('theme', newTheme === 'dark' ? 'darcula' : 'default');
  }
}

// Initialize the editor when the DOM is loaded
document.addEventListener("DOMContentLoaded", function() {
  // Initialize CodeMirror
  codeEditor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
    lineNumbers: true,
    mode: "text/x-python",
    theme: "default",
    indentUnit: 4,
    indentWithTabs: false,
    lineWrapping: true,
    extraKeys: {
      "Tab": function(cm) {
        cm.replaceSelection("    ", "end");
      }
    }
  });

  // Set initial height
  codeEditor.setSize(null, 400);

  // Load lessons for the selected course
  loadLessons();

  // Set up event listeners
  setupEventListeners();
  
  // Initialize theme
  initializeTheme();
});

// Load lessons based on the selected course
function loadLessons() {
  const course = courseSelect.value;
  
  fetch(`/syllabi/python/index.json`)
    .then(response => {
      if (!response.ok) {
        throw new Error("Failed to fetch lessons");
      }
      return response.json();
    })
    .then(data => {
      // Clear any existing options except the placeholder
      lessonSelect.innerHTML = "";
      
      // Add a default empty option
      const defaultOption = document.createElement("option");
      defaultOption.value = "";
      defaultOption.textContent = "-- Select a lesson --";
      defaultOption.disabled = true;
      defaultOption.selected = true;
      lessonSelect.appendChild(defaultOption);
      
      // Add optgroups for each category
      const categories = ["basics", "advanced"];
      
      categories.forEach(category => {
        if (data[category]) {
          // Create an optgroup for this category
          const group = document.createElement("optgroup");
          group.label = category.charAt(0).toUpperCase() + category.slice(1); // Capitalize
          
          // Add all lessons in this category
          Object.keys(data[category]).forEach(lesson => {
            const option = document.createElement("option");
            option.value = lesson;
            option.textContent = lesson;
            group.appendChild(option);
          });
          
          lessonSelect.appendChild(group);
        }
      });
    })
    .catch(err => {
      console.error("Error loading lessons:", err);
      // Add a fallback option
      lessonSelect.innerHTML = "<option value=''>Error loading lessons</option>";
      
      // Add a fallback option for testing
      const option = document.createElement("option");
      option.value = "Variables and Types";
      option.textContent = "Variables and Types (fallback)";
      lessonSelect.appendChild(option);
    });
}

// Set up all event listeners
function setupEventListeners() {
  // Theme toggle button
  themeToggleBtn.addEventListener("click", toggleTheme);
  
  // Handle language change
  languageSelect.addEventListener("change", () => {
    const language = languageSelect.value;
    
    if (language === "python") {
      codeEditor.setOption("mode", "text/x-python");
      
      // Set default Python code if editor is empty
      if (!codeEditor.getValue().trim()) {
        codeEditor.setValue(
`# Your Python code here`
        );
      }
    } else if (language === "java") {
      codeEditor.setOption("mode", "text/x-java");
      
      // Set default Java code if editor is empty
      if (!codeEditor.getValue().trim()) {
        codeEditor.setValue(
`public class Main {
    public static void main(String[] args) {
        // Your Java code here
    }
}`
        );
      }
    } else if (language === "cpp") {
      codeEditor.setOption("mode", "text/x-c++src");
      
      // Set default C++ code if editor is empty
      if (!codeEditor.getValue().trim()) {
        codeEditor.setValue(
`#include <iostream>
using namespace std;

int main() {
    // Your C++ code here
    return 0;
}`
        );
      }
    }
  });

  // Handle Generate Problem
  generateBtn.addEventListener("click", () => {
    const course = courseSelect.value;
    const lesson = lessonSelect.value;

    if (!lesson) {
      alert("Please select the lesson you're currently learning.");
      return;
    }

    generateBtn.style.display = "none";
    resultDiv.textContent = "Generating...";

    fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ course, lesson })
    })
    .then(res => res.json())
    .then(data => {
      const title = data?.data?.outputs?.Title || "Generated Problem";
      const problemMarkdown = data?.data?.outputs?.Problem || "No problem found.";
      let testcases = data?.testcases || []; // Get testcases from the response
      
      // Handle case where testcases might be a string instead of an array
      if (typeof testcases === 'string') {
        try {
          // Try to parse the string as JSON
          testcases = JSON.parse(testcases);
          console.log("Parsed testcases from string:", testcases);
        } catch (e) {
          console.error("Error parsing testcases:", e);
          testcases = [];
        }
      }

      titleHeader.textContent = title;
      resultDiv.innerHTML = marked.parse(problemMarkdown);
      
      // Store test cases globally so they can be accessed later
      window.testcases = testcases;
      console.log("Stored testcases:", window.testcases); 

      checkAnswerBtn.style.display = "inline-block";
      retryBtn.style.display = "inline-block";
    })
    .catch(err => {
      console.error(err);
      resultDiv.textContent = "Error generating problem.";
    });
  });

  // Handle Retry - Goes back to input stage
  retryBtn.addEventListener("click", () => {
    checkAnswerBtn.style.display = "none";
    retryBtn.style.display = "none";
    resultsDiv.innerHTML = "";  // Clear test case results

    // Reset UI elements back to input stage
    titleHeader.textContent = "Problem Generator"; // Reset title
    resultDiv.innerHTML = `<p>Your generated problem will appear here.</p>`;
    generateBtn.style.display = "inline-block";
  });

  // Run Code logic
  runBtn.addEventListener("click", () => {
    const code = codeEditor.getValue();
    const userInput = inputEditor.value;
    const language = languageSelect.value;

    // Save the current height of the input container before hiding it
    const currentHeight = inputContainer.offsetHeight;
    
    inputContainer.style.display = "none";
    consoleDiv.style.display = "block";
    // Apply the same height to the console
    if (currentHeight > 0) {
      consoleDiv.style.minHeight = `${currentHeight}px`;
    }
    
    consoleDiv.textContent = `Running ${language} code...`;
    resetBtn.style.display = "inline-block";

    fetch("/run_code", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, stdin: userInput, language })
    })
    .then(res => res.json())
    .then(data => {
      let output = "";
      if (data.stdout) output += data.stdout + "\n";
      if (data.stderr) output += "Errors:\n" + data.stderr + "\n";
      if (!data.stdout && !data.stderr) output = "No output.";
      consoleDiv.textContent = output;
    })
    .catch(err => {
      console.error("Error:", err);
      consoleDiv.textContent = "Error running code.";
    });
  });

  // Reset logic
  resetBtn.addEventListener("click", () => {
    // Save the current height of the console before hiding it
    const currentHeight = consoleDiv.offsetHeight;
    
    consoleDiv.style.display = "none";
    inputContainer.style.display = "block";
    // Set a reasonable height for the input container
    // Use a more moderate height instead of copying the console height
    inputContainer.style.minHeight = "150px";
    inputEditor.style.height = "120px";
    
    resetBtn.style.display = "none";
    consoleDiv.textContent = "";
  });

  // Handle Checking Answers
  checkAnswerBtn.addEventListener("click", () => {
    const code = codeEditor.getValue();
    const language = languageSelect.value;
    
    if (!code.trim()) {
      alert("Please enter code before checking.");
      return;
    }

    let testcases = window.testcases;
    
    // Handle different formats of testcases
    if (typeof testcases === 'string') {
      try {
        testcases = JSON.parse(testcases);
        console.log("Parsed testcases from string in check_answer:", testcases);
      } catch (e) {
        console.error("Error parsing testcases in check_answer:", e);
        alert("Error parsing test cases. Please try generating the problem again.");
        return;
      }
    }
    
    if (!testcases || !Array.isArray(testcases) || testcases.length === 0) {
      alert("No valid test cases found.");
      return;
    }
    
    console.log("Using testcases:", testcases);

    fetch("/check_code", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, testcases, language })
    })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        resultsDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        return;
      }

      let tableHTML = `<h2>Test Case Results</h2><table border="1">
                      <tr><th>Input</th><th>Expected Output</th><th>Your Output</th><th>Status</th></tr>`;
      data.results.forEach(tc => {
        tableHTML += `<tr>
                        <td><pre>${tc.input}</pre></td>
                        <td><pre>${tc.expected_output}</pre></td>
                        <td><pre>${tc.user_output}</pre></td>
                        <td style="color: ${tc.status === '✅' ? 'green' : 'red'}">${tc.status}</td>
                      </tr>`;
        if (tc.error) {
          tableHTML += `<tr><td colspan="4"><button onclick="this.nextElementSibling.style.display='block'">Show Error</button>
                        <pre style="display:none; color: red;">${tc.error}</pre></td></tr>`;
        }
      });
      tableHTML += "</table>";

      resultsDiv.innerHTML = tableHTML;  // Now results are stored correctly
    })
    .catch(err => {
      console.error(err);
      resultsDiv.innerHTML = `<p style="color: red;">Error checking answer.</p>`;
    });
  });
}
