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
const historyBtn     = document.getElementById("history-btn");
const historyModal   = document.getElementById("history-modal");
const historyList    = document.getElementById("history-list");
const closeModalBtn  = document.getElementById("close-modal");
const helpBtn        = document.getElementById("help-btn");
const helpModal      = document.getElementById("help-modal");
const helpContent    = document.getElementById("help-content");
const closeHelpBtn   = document.getElementById("close-help-modal");
const chatButton     = document.getElementById("chat-button");
const chatToggleBtn  = document.getElementById("chat-toggle-btn");
const chatWindow     = document.getElementById("chat-window");
const closeChat      = document.getElementById("close-chat");

// Global state
let currentProblemId = null;

// CodeMirror editor setup
let codeEditor;

// Function to render markdown to HTML (simple version without LaTeX)
function renderMarkdown(markdownContent, targetElement) {
  // Convert markdown to HTML
  const htmlContent = marked.parse(markdownContent);
  targetElement.innerHTML = htmlContent;
}

// Sync the programming language with the selected course
function syncLanguageWithCourse(course) {
  // Map course names to their corresponding programming languages
  const courseToLanguage = {
    "learnpython.org": "python",
    "learn-cpp.org": "cpp",
    "learnjavaonline.org": "java"
  };
  
  // Get the appropriate language for the course
  const language = courseToLanguage[course] || "python";
  
  // Update the language selector
  if (languageSelect.value !== language) {
    console.log(`Changing language from ${languageSelect.value} to ${language} based on course selection`);
    languageSelect.value = language;
    
    // Trigger the change event to update the editor mode and template
    const changeEvent = new Event('change');
    languageSelect.dispatchEvent(changeEvent);
  }
}

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
    // Force theme refresh by applying the appropriate theme with a small delay
    if (newTheme === 'dark') {
      codeEditor.setOption('theme', 'idea');
      setTimeout(() => codeEditor.setOption('theme', 'darcula'), 10);
    } else {
      codeEditor.setOption('theme', 'darcula');
      setTimeout(() => codeEditor.setOption('theme', 'idea'), 10);
    }
    console.log(`Theme changed to: ${newTheme}, CodeMirror theme: ${newTheme === 'dark' ? 'darcula' : 'idea'}`);
  }
}

// Initialize the application when the document is ready
document.addEventListener("DOMContentLoaded", function() {
  // Initialize KaTeX auto-render functionality
  if (typeof renderMathInElement === 'function') {
    console.log('Initializing KaTeX auto-render');
    renderMathInElement(document.body, {
      delimiters: [
        {left: '$$', right: '$$', display: true},
        {left: '$', right: '$', display: false},
        {left: '\\(', right: '\\)', display: false},
        {left: '\\[', right: '\\]', display: true}
      ],
      throwOnError: false
    });
  } else {
    console.warn('KaTeX auto-render not available');
  }
  // Get current theme directly from localStorage which is more reliable than data-theme attribute
  const storedTheme = localStorage.getItem('theme');
  const currentTheme = storedTheme || 'light';
  const cmTheme = currentTheme === 'dark' ? 'darcula' : 'idea';
  
  console.log(`Theme from localStorage: ${storedTheme}, Using theme: ${currentTheme}`);
  
  // Ensure the theme attribute is set correctly in case it's not
  document.documentElement.setAttribute('data-theme', currentTheme);
  
  // Force a theme redraw by quickly toggling and toggling back if we're in dark mode
  if (currentTheme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'light');
    setTimeout(() => document.documentElement.setAttribute('data-theme', 'dark'), 5);
  }
  
  // Initialize CodeMirror with appropriate theme based on current mode
  codeEditor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
    lineNumbers: true,
    mode: "text/x-python",
    theme: cmTheme,
    indentUnit: 4,
    indentWithTabs: false,
    lineWrapping: true,
    extraKeys: {
      "Tab": function(cm) {
        cm.replaceSelection("    ", "end");
      }
    }
  });
  
  console.log(`Initialized CodeMirror with theme: ${cmTheme} based on theme: ${currentTheme}`);
  
  // For dark mode, force theme application in a more robust way
  if (currentTheme === 'dark') {
    // Use a longer delay and multiple attempts to ensure the theme is applied
    setTimeout(() => {
      codeEditor.setOption('theme', 'idea');
      console.log('Forcing theme reset to idea first');
      
      setTimeout(() => {
        codeEditor.setOption('theme', 'darcula');
        console.log('Applied darcula theme');
        
        // Force a refresh of the editor
        codeEditor.refresh();
        console.log('Refreshed CodeMirror instance');
      }, 100);
    }, 100);
  }

  // Set initial height
  codeEditor.setSize(null, 400);
  
  // Set consistent initial heights for input boxes
  inputContainer.style.minHeight = "150px";
  inputEditor.style.height = "120px";

  // Load lessons for the selected course
  loadLessons();

  // Set up event listeners
  setupEventListeners();
  
  // Initialize theme
  initializeTheme();
  
  // Enable history button if problems exist
  checkForProblems();
});

// Help Modal Functions
function openHelpModal() {
  // Display the modal
  helpModal.style.display = "block";
  
  // Load the help markdown content
  fetch("/static/help.md")
    .then(response => {
      if (!response.ok) {
        throw new Error("Failed to load help content");
      }
      return response.text();
    })
    .then(markdown => {
      // Use simple markdown rendering
      renderMarkdown(markdown, helpContent);
      
      // Simply use the global auto-render from KaTeX if available
      if (window.renderMathInElement && typeof renderMathInElement === 'function') {
        setTimeout(() => {
          try {
            renderMathInElement(helpContent, {
              delimiters: [
                {left: '$$', right: '$$', display: true},
                {left: '$', right: '$', display: false},
                {left: '\\(', right: '\\)', display: false},
                {left: '\\[', right: '\\]', display: true}
              ],
              throwOnError: false
            });
          } catch (e) {
            console.error('Error rendering LaTeX in help content:', e);
          }
        }, 100); // Small delay to ensure DOM is updated
      }
    })
    .catch(error => {
      console.error("Error loading help content:", error);
      helpContent.innerHTML = `<p class="error">Error loading help content: ${error.message}</p>`;
    });
}

function closeHelpModal() {
  helpModal.style.display = "none";
}

// History Modal Functions
function openHistoryModal() {
  // Clear previous history list
  historyList.innerHTML = "<p>Loading problems...</p>";
  
  // Show the modal
  historyModal.style.display = "flex";
  
  // Fetch all problems (not filtered by course/lesson)
  fetch(`/problems`)
    .then(res => res.json())
    .then(data => {
      const problems = data.problems || [];
      
      // Update the modal with problems
      if (problems.length === 0) {
        historyList.innerHTML = "<p>No problems found.</p>";
        return;
      }
      
      // Clear and build the problem list
      historyList.innerHTML = "";
      
      problems.forEach(problem => {
        const date = new Date(problem.created_at);
        const formattedDate = date.toLocaleString();
        
        const problemItem = document.createElement("div");
        problemItem.className = "problem-item";
        
        // Create the content container (for everything except delete button)
        const contentContainer = document.createElement("div");
        contentContainer.className = "problem-content";
        // Format language with proper capitalization
        let languageDisplay = problem.language || '';
        if (languageDisplay) {
          if (languageDisplay === 'cpp') {
            languageDisplay = 'C++';
          } else {
            languageDisplay = languageDisplay.charAt(0).toUpperCase() + languageDisplay.slice(1);
          }
        }
        
        contentContainer.innerHTML = `
          <div class="problem-title">${problem.title}</div>
          <div class="problem-meta">
            ${problem.course} / ${problem.lesson} ${languageDisplay ? '| ' + languageDisplay : ''} <br>
            Created: ${formattedDate}
          </div>
        `;
        
        // Add click handler to content container to load the problem
        contentContainer.addEventListener("click", (e) => {
          loadProblem(problem.id);
        });
        
        // Create delete button
        const deleteBtn = document.createElement("button");
        deleteBtn.className = "delete-btn";
        deleteBtn.innerHTML = "🗑️";
        deleteBtn.title = "Delete this problem";
        
        // Add click handler to delete button
        deleteBtn.addEventListener("click", (e) => {
          e.stopPropagation(); // Prevent event bubbling to parent
          deleteProblem(problem.id, problemItem);
        });
        
        // Append elements to problem item
        problemItem.appendChild(contentContainer);
        problemItem.appendChild(deleteBtn);
        
        historyList.appendChild(problemItem);
      });
    })
    .catch(err => {
      console.error("Error loading problems:", err);
      historyList.innerHTML = "<p>Error loading problems. Please try again.</p>";
    });
}

function closeHistoryModal() {
  historyModal.style.display = "none";
}

function deleteProblem(problemId, problemElement) {
  // Confirm before deleting
  if (!confirm(`Are you sure you want to delete this problem and all associated solutions?`)) {
    return;
  }
  
  // Show loading state
  problemElement.classList.add("deleting");
  
  // Send delete request
  fetch(`/problems/${problemId}`, {
    method: "DELETE"
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      // Remove the problem from the DOM with animation
      problemElement.style.height = `${problemElement.offsetHeight}px`;
      setTimeout(() => {
        problemElement.style.height = "0";
        problemElement.style.opacity = "0";
        problemElement.style.padding = "0";
        problemElement.style.margin = "0";
        
        // Remove element completely after animation
        setTimeout(() => {
          problemElement.remove();
          
          // If no problems left, show message
          if (historyList.children.length === 0) {
            historyList.innerHTML = "<p>No problems found.</p>";
          }
        }, 300);
      }, 10);
    } else {
      // Show error
      alert(`Error deleting problem: ${data.message}`);
      problemElement.classList.remove("deleting");
    }
  })
  .catch(err => {
    console.error("Error deleting problem:", err);
    alert("Error deleting problem. Please try again.");
    problemElement.classList.remove("deleting");
  });
}

function loadProblem(problemId) {
  // Check if code editor has content before loading a different problem
  if (codeEditor && codeEditor.getValue().trim() !== "") {
    if (!confirm("Loading a problem will clear your current code. Are you sure you want to continue?")) {
      // User canceled, don't load the problem
      closeHistoryModal();
      return;
    }
    // Clear the code editor and reset chat
    codeEditor.setValue("");
    resetChatConversation();
  }
  
  // Close the modal
  closeHistoryModal();
  
  // Show loading state
  resultDiv.textContent = "Loading problem...";
  
  // Fetch the problem
  fetch(`/problems/${problemId}`)
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        resultDiv.textContent = `Error: ${data.error}`;
        return;
      }
      
      const problem = data.problem;
      
      // Display the problem
      titleHeader.textContent = problem.title;
      
      // Render markdown to HTML
      renderMarkdown(problem.problem_text, resultDiv);
      
      // Render LaTeX formulas if available
      if (window.renderMathInElement && typeof renderMathInElement === 'function') {
        setTimeout(() => {
          try {
            renderMathInElement(resultDiv, {
              delimiters: [
                {left: '$$', right: '$$', display: true},
                {left: '$', right: '$', display: false},
                {left: '\\(', right: '\\)', display: false},
                {left: '\\[', right: '\\]', display: true}
              ],
              throwOnError: false
            });
          } catch (e) {
            console.error('Error rendering LaTeX in problem:', e);
          }
        }, 100); // Small delay to ensure DOM is updated
      }
      
      // Store problem ID and testcases
      currentProblemId = problem.id;
      
      // Use the testcases from the database for this problem
      window.testcases = problem.testcases || [];
      
      // Set the course and lesson values
      if (problem.course) {
        courseSelect.value = problem.course;
        // Trigger lesson loading
        loadLessons(false); // Pass false to avoid clearing code since we already did that
        
        // If lesson is available, set it after lessons are loaded
        if (problem.lesson) {
          setTimeout(() => {
            lessonSelect.value = problem.lesson;
          }, 500); // Small delay to ensure lessons are loaded
        }
      }
      
      // Set the programming language based on problem language
      // Try to detect language from solutions or course name
      let detectedLanguage = null;
      
      // First try to determine from course name
      if (problem.course && problem.course.toLowerCase().includes('python')) {
        detectedLanguage = 'python';
      } else if (problem.course && problem.course.toLowerCase().includes('java')) {
        detectedLanguage = 'java';
      } else if (problem.course && (problem.course.toLowerCase().includes('cpp') || problem.course.toLowerCase().includes('c++'))) {
        detectedLanguage = 'cpp';
      }
      
      // Set the language in the dropdown if detected
      if (detectedLanguage && languageSelect) {
        languageSelect.value = detectedLanguage;
        
        // Update editor mode according to the language
        if (codeEditor) {
          if (detectedLanguage === 'python') {
            codeEditor.setOption("mode", "text/x-python");
          } else if (detectedLanguage === 'java') {
            codeEditor.setOption("mode", "text/x-java");
          } else if (detectedLanguage === 'cpp') {
            codeEditor.setOption("mode", "text/x-c++src");
          }
        }
      }
      
      // Clear any previous results and hide console
      resultsDiv.innerHTML = "";
      if (consoleDiv.style.display !== "none") {
        consoleDiv.style.display = "none";
        inputContainer.style.display = "block";
      }
      
      // Hide course and lesson selectors when a problem is shown
      document.querySelector('label[for="course-select"]').style.display = 'none';
      courseSelect.style.display = 'none';
      document.querySelector('label[for="lesson-select"]').style.display = 'none';
      lessonSelect.style.display = 'none';
      document.querySelectorAll('br').forEach(br => {
        if (br.nextElementSibling === courseSelect || br.nextElementSibling === lessonSelect ||
            br.previousElementSibling === courseSelect || br.previousElementSibling === lessonSelect) {
          br.style.display = 'none';
        }
      });
      
      // Show check answer and retry buttons
      checkAnswerBtn.style.display = "inline-block";
      retryBtn.style.display = "inline-block";
      generateBtn.style.display = "none";
      
      // Hide the selection module when problem is loaded
      const selectionModule = document.getElementById('selection-module');
      if (selectionModule) selectionModule.classList.add('hidden');
    })
    .catch(err => {
      console.error("Error loading problem:", err);
      resultDiv.textContent = "Error loading problem. Please try again.";
    });
}

function checkForProblems() {
  // Check if we have any problems in the database at all
  if (!historyBtn) return;
  
  fetch(`/problems?limit=1`)
    .then(res => res.json())
    .then(data => {
      const problems = data.problems || [];
      historyBtn.disabled = problems.length === 0;
    })
    .catch(err => {
      console.error("Error checking for problems:", err);
      historyBtn.disabled = true;
    });
}

// Load lessons based on the selected course
function loadLessons(skipClearCodeCheck = true) {
  const course = courseSelect.value || "learnpython.org";
  const lang = "en"; // Default language is English
  
  // If we need to check for code clearing and editor has content
  if (!skipClearCodeCheck && codeEditor && codeEditor.getValue().trim() !== "") {
    if (!confirm("Changing lessons will clear your code. Are you sure you want to continue?")) {
      // Reset the selection to the previous value
      setTimeout(() => {
        // Restore previous course selection
        const prevCourse = localStorage.getItem('prevCourse') || "learnpython.org";
        courseSelect.value = prevCourse;
      }, 0);
      return; // Don't load lessons if user cancels
    }
    // Clear the code editor
    codeEditor.setValue("");
    
    // Also reset chat conversation
    resetChatConversation();
  }
  
  // Store the current course for future reference
  localStorage.setItem('prevCourse', course);
  
  console.log(`Loading lessons for course: ${course}`);
  
  // Sync language selector with course
  if (typeof syncLanguageWithCourse === 'function') {
    syncLanguageWithCourse(course);
  } else {
    // Fallback manual language selection based on course
    if (course === "learn-cpp.org" && languageSelect.value !== "cpp") {
      languageSelect.value = "cpp";
      // Trigger change event
      languageSelect.dispatchEvent(new Event('change'));
    } else if (course === "learnpython.org" && languageSelect.value !== "python") {
      languageSelect.value = "python";
      // Trigger change event
      languageSelect.dispatchEvent(new Event('change'));
    }
  }
  
  // Use our new endpoint that fetches from GitHub
  fetch(`/github/lessons?language=${course}&lang=${lang}`)
    .then(response => {
      if (!response.ok) {
        throw new Error("Failed to fetch lessons from GitHub");
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
      
      // Add optgroups for each category in the correct order
      const categories = ["basics", "advanced"];
      
      categories.forEach(category => {
        if (data[category]) {
          // Create an optgroup for this category
          const group = document.createElement("optgroup");
          group.label = category.charAt(0).toUpperCase() + category.slice(1); // Capitalize
          
          // For ordered categories, we need a special approach
          // Since Object.keys() and for...in loops don't guarantee order in JS objects
          
          // If the data comes with an _order array property, use that
          const orderedLessons = [];
          
          if (Array.isArray(data[category]._order)) {
            // Server provided an explicit order
            console.log(`Using explicit _order array for ${category}`); 
            orderedLessons.push(...data[category]._order);
          } else {
            // Fallback: collect lessons and maintain insertion order
            console.log(`No explicit ordering found for ${category}, collecting lessons`);
            for (const lessonName in data[category]) {
              if (lessonName !== '_order') { // Skip the order property itself
                orderedLessons.push(lessonName);
              }
            }
          }
          
          // Now add each lesson to the group in the original order
          orderedLessons.forEach(lesson => {
            const option = document.createElement("option");
            option.value = lesson;
            option.textContent = lesson;
            group.appendChild(option);
          });
          
          lessonSelect.appendChild(group);
        }
      });
      
      console.log(`Loaded ${Object.keys(data.basics || {}).length + Object.keys(data.advanced || {}).length} lessons from GitHub`);
    })
    .catch(err => {
      console.error("Error loading lessons from GitHub:", err);
      // Add a fallback option
      lessonSelect.innerHTML = "<option value=''>Error loading lessons from GitHub</option>";
      
      // Add a fallback option for testing
      const option = document.createElement("option");
      option.value = "Hello, World!";
      option.textContent = "Hello, World! (fallback)";
      lessonSelect.appendChild(option);
    });
}

// Set up all event listeners
function setupEventListeners() {
  // Course select change handler
  courseSelect.addEventListener("change", function() {
    // Check if code editor has content before changing course
    if (codeEditor && codeEditor.getValue().trim() !== "") {
      if (!confirm("Changing the course will clear your code editor. Are you sure you want to continue?")) {
        // Reset the selection to the previous value
        setTimeout(() => {
          const prevCourse = localStorage.getItem('prevCourse') || "learnpython.org";
          courseSelect.value = prevCourse;
        }, 0);
        return;
      }
      // Clear the code editor
      codeEditor.setValue("");
      
      // Also reset chat conversation
      resetChatConversation();
    }
    
    // Store the current course for future reference
    localStorage.setItem('prevCourse', courseSelect.value);
    
    // Reload lessons when course changes
    loadLessons();
  });
  
  // Theme toggle button
  themeToggleBtn.addEventListener("click", toggleTheme);
  
  // Chat toggle button in header
  if (chatToggleBtn) {
    chatToggleBtn.addEventListener("click", toggleChatWindow);
  }
  
  // Close chat button functionality
  if (closeChat) {
    closeChat.addEventListener("click", toggleChatWindow);
  }
  
  // History button and modal functionality
  if (historyBtn) {
    historyBtn.addEventListener("click", openHistoryModal);
  }
  
  if (closeModalBtn) {
    closeModalBtn.addEventListener("click", closeHistoryModal);
  }
  
  // Help button
  helpBtn.addEventListener("click", openHelpModal);
  
  // Close help modal button
  closeHelpBtn.addEventListener("click", closeHelpModal);
  
  // Close modals when clicking outside of them
  window.addEventListener("click", (event) => {
    if (event.target === historyModal) {
      closeHistoryModal();
    }
    if (event.target === helpModal) {
      closeHelpModal();
    }
  });
  
  // Handle language change
  languageSelect.addEventListener("change", () => {
    const language = languageSelect.value;
    
    if (language === "python") {
      codeEditor.setOption("mode", "text/x-python");
      // No default code template
    } else if (language === "java") {
      codeEditor.setOption("mode", "text/x-java");
      // No default code template
    } else if (language === "cpp") {
      codeEditor.setOption("mode", "text/x-c++src");
      // No default code template
    }
  });

  // Handle Generate Problem
  generateBtn.addEventListener("click", () => {
    // Check if code editor has content before generating a new problem
    if (codeEditor && codeEditor.getValue().trim() !== "") {
      if (!confirm("Generating a new problem will clear your code. Are you sure you want to continue?")) {
        return; // Don't proceed if user cancels
      }
      // Clear the code editor
      codeEditor.setValue("");
      
      // Also reset chat conversation
      resetChatConversation();
    }
    
    const course = courseSelect.value;
    const lesson = lessonSelect.value;
    
    // Set the programming language based on the course
    let language;
    if (course.toLowerCase().includes('python')) {
      language = 'python';
    } else if (course.toLowerCase().includes('java')) {
      language = 'java';
    } else if (course.toLowerCase().includes('cpp') || course.toLowerCase().includes('c++')) {
      language = 'cpp';
    } else {
      // Default to Python if course doesn't match any known language
      language = 'python';
    }

    if (!lesson) {
      alert("Please select the lesson you're currently learning.");
      return;
    }

    // Hide the generate button while generating but keep the history button visible
    generateBtn.style.display = "none";
    
    // Show loading animation with dots
    let dots = 0;
    const loadingText = "Generating";
    resultDiv.textContent = loadingText + "...";
    
    const loadingInterval = setInterval(() => {
      dots = (dots + 1) % 4;
      let dotsText = ".".repeat(dots);
      resultDiv.textContent = loadingText + dotsText.padEnd(3, " ");
    }, 300);

    fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ course, lesson, language })
    })
    .then(res => res.json())
    .then(data => {
      // Clear the loading interval
      clearInterval(loadingInterval);
      
      const title = data?.data?.outputs?.Title || "Generated Problem";
      const problemMarkdown = data?.data?.outputs?.Problem || "No problem found.";
      let testcases = data?.testcases || []; // Get testcases from the response
      
      // Store the problem ID from the response
      currentProblemId = data.problem_id || null;
      
      // Handle case where testcases might be a string instead of an array
      if (typeof testcases === 'string') {
        try {
          // Try to parse the string as JSON
          testcases = JSON.parse(testcases);
        } catch (e) {
          console.error("Error parsing testcases:", e);
          testcases = [];
        }
      }

      titleHeader.textContent = title;
      resultDiv.innerHTML = marked.parse(problemMarkdown);
      
      // Store test cases globally so they can be accessed later
      window.testcases = testcases;

      // Show the check and retry buttons
      checkAnswerBtn.style.display = "inline-block";
      retryBtn.style.display = "inline-block";
      
      // Hide course and lesson selectors when a problem is shown
      document.querySelector('label[for="course-select"]').style.display = 'none';
      courseSelect.style.display = 'none';
      document.querySelector('label[for="lesson-select"]').style.display = 'none';
      lessonSelect.style.display = 'none';
      document.querySelectorAll('br').forEach(br => {
        if (br.nextElementSibling === courseSelect || br.nextElementSibling === lessonSelect ||
            br.previousElementSibling === courseSelect || br.previousElementSibling === lessonSelect) {
          br.style.display = 'none';
        }
      });
      
      // Make sure history button is enabled
      if (historyBtn) {
        historyBtn.disabled = false;
      }
      
      // Hide the selection module when problem is loaded
      const selectionModule = document.getElementById('selection-module');
      if (selectionModule) selectionModule.classList.add('hidden');
    })
    .catch(err => {
      // Clear the loading interval
      clearInterval(loadingInterval);
      
      console.error(err);
      resultDiv.textContent = "Error generating problem.";
      
      // Show generate button again on error
      generateBtn.style.display = "inline-block";
    });
  });

  // Handle Retry - Goes back to input stage
  retryBtn.addEventListener("click", () => {
    // Check if code editor has content before returning
    if (codeEditor && codeEditor.getValue().trim() !== "") {
      if (!confirm("Returning to the problem selection will clear your code. Are you sure you want to continue?")) {
        return; // Don't proceed if user cancels
      }
      // Clear the code editor
      codeEditor.setValue("");
      
      // Also reset chat conversation
      resetChatConversation();
    }
    
    checkAnswerBtn.style.display = "none";
    retryBtn.style.display = "none";
    resultsDiv.innerHTML = "";  // Clear test case results

    // Hide console if visible and show input container
    consoleDiv.style.display = "none";
    inputContainer.style.display = "block";

    // Reset UI elements back to input stage
    titleHeader.textContent = "Problem Generator"; // Reset title
    resultDiv.innerHTML = `<p>Your generated problem will appear here.</p>`;
    generateBtn.style.display = "inline-block";
    
    // Show the selection module again
    const selectionModule = document.getElementById('selection-module');
    if (selectionModule) selectionModule.classList.remove('hidden');
    
    // Show course and lesson selectors again
    document.querySelector('label[for="course-select"]').style.display = 'block';
    courseSelect.style.display = 'block';
    document.querySelector('label[for="lesson-select"]').style.display = 'block';
    lessonSelect.style.display = 'block';
    document.querySelectorAll('br').forEach(br => {
      if (br.nextElementSibling === courseSelect || br.nextElementSibling === lessonSelect ||
          br.previousElementSibling === courseSelect || br.previousElementSibling === lessonSelect) {
        br.style.display = 'inline';
      }
    });
    
    // Clear current problem ID
    currentProblemId = null;
    
    // Ensure input container has consistent height
    inputContainer.style.minHeight = "150px";
    inputEditor.style.height = "120px";
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
    // We don't need to save the console height since we're using fixed heights
    
    consoleDiv.style.display = "none";
    inputContainer.style.display = "block";
    // Set consistent fixed heights
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

    // Show checking animation
    checkAnswerBtn.disabled = true;
    let dots = 0;
    const originalText = checkAnswerBtn.textContent;
    const loadingText = "Checking";
    checkAnswerBtn.textContent = loadingText + "...";
    
    const loadingInterval = setInterval(() => {
      dots = (dots + 1) % 4;
      let dotsText = ".".repeat(dots);
      checkAnswerBtn.textContent = loadingText + dotsText.padEnd(3, " ");
    }, 300);

    let testcases = window.testcases;
    
    // Handle different formats of testcases
    if (typeof testcases === 'string') {
      try {
        testcases = JSON.parse(testcases);
        console.log("Parsed testcases from string in check_answer:", testcases);
      } catch (e) {
        console.error("Error parsing testcases in check_answer:", e);
        alert("Error parsing test cases. Please try generating the problem again.");
        clearInterval(loadingInterval);
        checkAnswerBtn.textContent = originalText;
        checkAnswerBtn.disabled = false;
        return;
      }
    }
    
    if (!testcases || !Array.isArray(testcases) || testcases.length === 0) {
      alert("No valid test cases found.");
      clearInterval(loadingInterval);
      checkAnswerBtn.textContent = originalText;
      checkAnswerBtn.disabled = false;
      return;
    }

    fetch("/check_code", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        code, 
        testcases, 
        language,
        problem_id: currentProblemId 
      })
    })
    .then(res => res.json())
    .then(data => {
      // Clear loading animation
      clearInterval(loadingInterval);
      checkAnswerBtn.textContent = originalText;
      checkAnswerBtn.disabled = false;
      
      if (data.error) {
        resultsDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        return;
      }

      // Count the number of passing tests
      let passingTests = 0;
      const totalTests = data.results.length;
      
      let tableHTML = `<h2>Test Case Results</h2><table border="1" style="width: 100%; table-layout: fixed;">
                      <tr>
                        <th style="width: 20%;">Input</th>
                        <th style="width: 30%;">Expected Output</th>
                        <th style="width: 30%;">Your Output</th>
                        <th style="width: 10%; text-align: center;">Status</th>
                      </tr>`;
      data.results.forEach(tc => {
        const isPassing = tc.status === '✅';
        if (isPassing) passingTests++;
        
        // Add background color to the entire row based on test result
        const rowColor = isPassing 
          ? 'background-color: rgba(0, 255, 0, 0.1);' // Light green for passing
          : 'background-color: rgba(255, 0, 0, 0.1);'; // Light red for failing
          
        tableHTML += `<tr style="${rowColor}">
                        <td style="word-wrap: break-word; overflow-wrap: break-word;"><pre style="white-space: pre-wrap; word-wrap: break-word; max-width: 100%;">${tc.input}</pre></td>
                        <td style="word-wrap: break-word; overflow-wrap: break-word;"><pre style="white-space: pre-wrap; word-wrap: break-word; max-width: 100%;">${tc.expected_output}</pre></td>
                        <td style="word-wrap: break-word; overflow-wrap: break-word;"><pre style="white-space: pre-wrap; word-wrap: break-word; max-width: 100%;">${tc.user_output}</pre></td>
                        <td style="color: ${isPassing ? 'green' : 'red'}; text-align: center; font-size: 1.2em;">${tc.status}</td>
                      </tr>`;
      });
      tableHTML += "</table>";
      
      // Add a summary of the test results
      tableHTML += `<p style="text-align: center; margin-top: 10px;">
                      <strong>${passingTests} of ${totalTests} tests passing</strong>
                    </p>`;

      resultsDiv.innerHTML = tableHTML;  // Now results are stored correctly
      
      // If all tests pass, show confetti!
      if (passingTests === totalTests && totalTests > 0) {
        showConfetti();
      }
    })
    .catch(err => {
      // Clear loading animation
      clearInterval(loadingInterval);
      checkAnswerBtn.textContent = originalText;
      checkAnswerBtn.disabled = false;
      
      console.error(err);
      resultsDiv.innerHTML = `<p style="color: red;">Error checking answer.</p>`;
    });
  });
}

// Function to toggle the chat window visibility
function toggleChatWindow() {
  // Toggle the 'open' class instead of manipulating display style directly
  chatWindow.classList.toggle('open');
  document.body.classList.toggle('chat-open'); // Toggle body class for the push-in effect
  
  // Focus the chat input if window is open
  if (chatWindow.classList.contains('open')) {
    const chatInput = document.getElementById('chat-input');
    if (chatInput) chatInput.focus();
  }
}

// Function to reset the chat conversation
function resetChatConversation() {
  // Reset conversation ID and clear messages
  if (window.resetChat && typeof window.resetChat === 'function') {
    window.resetChat();
    console.log('Chat conversation reset');
  } else {
    console.log('resetChat function not available');
  }
}

// Function to show confetti animation when all tests pass
function showConfetti() {
  // Create confetti container
  const confettiContainer = document.createElement('div');
  confettiContainer.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 9999;
    overflow: hidden;
  `;
  document.body.appendChild(confettiContainer);
  
  // Create confetti pieces
  const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff'];
  const totalPieces = 150;
  
  for (let i = 0; i < totalPieces; i++) {
    const piece = document.createElement('div');
    
    // Random properties for each piece
    const color = colors[Math.floor(Math.random() * colors.length)];
    const size = Math.random() * 10 + 5; // 5-15px
    const startPositionLeft = Math.random() * 100; // 0-100%
    const startOpacity = 0.8;
    const endPositionTop = 95 + Math.random() * 5; // 95-100%
    const endPositionLeft = startPositionLeft + Math.random() * 20 - 10; // +/- 10% from start
    const rotateStart = Math.random() * 360; // 0-360 degrees
    const rotateEnd = rotateStart + Math.random() * 360; // additional 0-360 degrees
    const duration = 3000 + Math.random() * 2000; // 3-5 seconds
    const delay = Math.random() * 1500; // 0-1.5 seconds
    
    // Configure the piece
    piece.style.cssText = `
      position: absolute;
      width: ${size}px;
      height: ${size}px;
      background-color: ${color};
      top: -5%;
      left: ${startPositionLeft}%;
      opacity: ${startOpacity};
      transform: rotate(${rotateStart}deg);
      transition: top ${duration}ms ease-out, left ${duration}ms ease-out, transform ${duration}ms ease-out, opacity ${duration}ms ease-out;
      transition-delay: ${delay}ms;
      pointer-events: none;
    `;
    
    confettiContainer.appendChild(piece);
    
    // Trigger the animation after a small delay
    setTimeout(() => {
      piece.style.top = `${endPositionTop}%`;
      piece.style.left = `${endPositionLeft}%`;
      piece.style.transform = `rotate(${rotateEnd}deg)`;
      piece.style.opacity = '0';
    }, 50);
    
    // Remove the piece after animation is done
    setTimeout(() => {
      piece.remove();
      // Remove container once all pieces are gone
      if (i === totalPieces - 1) {
        setTimeout(() => {
          confettiContainer.remove();
        }, duration + delay + 100);
      }
    }, duration + delay + 100);
  }
  
  // Show a success message
  const successMessage = document.createElement('div');
  successMessage.textContent = 'All Tests Passed! 🎉';
  successMessage.style.cssText = `
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: rgba(0, 200, 0, 0.7);
    color: white;
    padding: 15px 30px;
    border-radius: 10px;
    font-size: 24px;
    font-weight: bold;
    z-index: 10000;
    animation: successFadeOut 2.5s forwards;
    text-align: center;
    white-space: nowrap;
  `;
  
  // Add keyframes for fading out
  const style = document.createElement('style');
  style.innerHTML = `
    @keyframes successFadeOut {
      0% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
      20% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
      30% { transform: translate(-50%, -50%) scale(1); }
      70% { opacity: 1; }
      100% { opacity: 0; }
    }
  `;
  document.head.appendChild(style);
  document.body.appendChild(successMessage);
  
  // Remove the success message after animation
  setTimeout(() => {
    successMessage.remove();
    style.remove();
  }, 2500);
}
