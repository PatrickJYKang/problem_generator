// Style Check Module
const styleCheck = (function() {
  // Store original code editor content
  let originalCode = "";
  let originalEditorMode = "";
  
  // DOM elements - these will be initialized in the init function
  let styleCheckButton;
  
  // Initialize the module
  function init() {
    // Check if the button already exists to prevent duplicates
    if (!document.getElementById('style-check-btn')) {
      // Create and add the style check button
      styleCheckButton = document.createElement('button');
      styleCheckButton.id = 'style-check-btn';
      styleCheckButton.className = 'btn btn-primary';
      styleCheckButton.textContent = 'Check Style';
      styleCheckButton.title = 'Check code style with a linter';
      
      // Add the button near the check answer button, but not inside the style check container
      const styleCheckContainer = document.querySelector('.style-check-container');
      if (!styleCheckContainer) {
        const actionButtonsDiv = document.querySelector('.action-buttons');
        if (actionButtonsDiv) {
          actionButtonsDiv.appendChild(styleCheckButton);
        } else {
          const checkAnswerBtn = document.getElementById('check-answer-btn');
          if (checkAnswerBtn && checkAnswerBtn.parentNode) {
            checkAnswerBtn.parentNode.insertBefore(styleCheckButton, checkAnswerBtn.nextSibling);
          }
        }
      }
      
      // Add event listener
      styleCheckButton.addEventListener('click', runStyleCheck);
      console.log('Style check button added to DOM');
    }
  }
  
  // Run the style check
  function runStyleCheck() {
    // Get the current code and language
    const code = codeEditor.getValue();
    const language = document.getElementById('language-select').value;
    
    // Don't run style check on empty code
    if (!code.trim()) {
      alert('Please write some code before checking style.');
      return;
    }
    
    // Save the original code for later
    originalCode = code;
    originalEditorMode = codeEditor.getOption('mode');
    
    // Show loading state
    styleCheckButton.disabled = true;
    styleCheckButton.textContent = 'Checking...';
    
    // Send request to backend
    fetch('/check_style', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        code: code,
        language: language
      })
    })
    .then(response => response.json())
    .then(data => {
      displayStyleResults(data, language);
    })
    .catch(error => {
      console.error('Style check failed:', error);
      alert('Style check failed. See console for details.');
    })
    .finally(() => {
      // Reset button state
      styleCheckButton.disabled = false;
      styleCheckButton.textContent = 'Check Style';
    });
  }
  
  // Display style check results in the problem area
  function displayStyleResults(data, language) {
    // If there's an error, show it and return
    if (data.error) {
      alert(`Style check error: ${data.error}`);
      return;
    }
    
    console.log('Style check data received:', data);
    
    // Get the raw code, code lines and errors
    const rawCode = data.raw_code || '';
    let codeLines = Array.isArray(data.code) ? data.code : [];
    const errors = data.errors || [];
    const linter = data.linter || "style checker";
    const totalErrors = data.total || 0;
    
    // Always prefer raw_code over code array
    if (rawCode) {
      codeLines = rawCode.split('\n');
    }
    
    // Find the problem content area
    const resultDiv = document.getElementById('result');
    if (!resultDiv) {
      console.error('Problem content area not found');
      return;
    }
    
    // Save the original problem content
    if (!resultDiv.getAttribute('data-original-content')) {
      resultDiv.setAttribute('data-original-content', resultDiv.innerHTML);
    }
    
    // Clear the problem area
    resultDiv.innerHTML = '';
    
    // Create the style check container
    const styleCheckContainer = document.createElement('div');
    styleCheckContainer.className = 'style-check-container';
    
    // Create header with summary and back button
    const header = document.createElement('div');
    header.className = 'style-check-header';
    header.style.display = 'flex';
    header.style.justifyContent = 'space-between';
    header.style.alignItems = 'center';
    
    // Create left side with error count
    const leftSide = document.createElement('div');
    leftSide.style.display = 'flex';
    leftSide.style.alignItems = 'center';
    
    // Create right side with buttons
    const rightSide = document.createElement('div');
    rightSide.style.display = 'flex';
    rightSide.style.alignItems = 'center';
    
    // Create error count display
    const errorCount = document.createElement('div');
    errorCount.className = 'error-count';
    errorCount.textContent = `${totalErrors} style ${totalErrors === 1 ? 'issue' : 'issues'} found with ${linter}`;
    leftSide.appendChild(errorCount);
    
    // Add a return button
    const returnButton = document.createElement('button');
    returnButton.className = 'btn btn-secondary return-button';
    returnButton.textContent = 'Back to problem';
    returnButton.addEventListener('click', function() {
      // Restore the original problem
      restoreOriginalProblem();
      
      // Optionally restore the editor content
      if (originalCode) {
        codeEditor.setValue(originalCode);
      }
    });
    
    // Add buttons to right side
    rightSide.appendChild(returnButton);
    
    // Add Format Code button for C++ and Java code
    if (language === 'cpp' || language === 'java') {
      const formatButton = document.createElement('button');
      formatButton.className = 'btn btn-primary format-button';
      formatButton.textContent = 'Format Code';
      formatButton.title = 'Format code with clang-format';
      formatButton.addEventListener('click', function() {
        formatCode(rawCode || codeEditor.getValue(), language);
      });
      
      // Add styles and margin
      formatButton.style.marginLeft = '10px';
      rightSide.appendChild(formatButton);
    }
    
    // Add sides to header
    header.appendChild(leftSide);
    header.appendChild(rightSide);
    
    // Add header to container
    styleCheckContainer.appendChild(header);
    
    // Create the content area for code display and errors
    const content = document.createElement('div');
    content.className = 'style-check-content';
    
    // Create code display section
    const codeDisplay = document.createElement('div');
    codeDisplay.className = 'code-display';
    
    // Handle empty code case
    if (codeLines.length === 0) {
      // Display a message if there are no code lines
      const noCodeMsg = document.createElement('div');
      noCodeMsg.className = 'no-code-message';
      noCodeMsg.textContent = 'No code found to display';
      codeDisplay.appendChild(noCodeMsg);
    } else {
      // Create a code block for syntax highlighting
      const codeBlock = document.createElement('pre');
      codeBlock.className = 'code-block';
      
      // Map errors by line (1-based for API, but we display 0-based)
      const errorsByLine = {};
      errors.forEach(error => {
        const lineNum = error.line || 1;
        if (!errorsByLine[lineNum]) {
          errorsByLine[lineNum] = [];
        }
        errorsByLine[lineNum].push(error);
      });
      
      // Add each line of code with highlighting for errors
      codeLines.forEach((lineContent, lineIndex) => {
        // Make sure lineContent is a string
        lineContent = (typeof lineContent === 'string') ? lineContent : String(lineContent || '');
        
        const lineNum = lineIndex + 1; // 1-based line number for matching errors
        const lineErrors = errorsByLine[lineNum] || [];
        
        // Create line container
        const lineElement = document.createElement('div');
        lineElement.className = 'code-line';
        if (lineErrors.length > 0) {
          lineElement.classList.add('has-error');
        }
        lineElement.setAttribute('data-line-num', lineNum);
        
        // Add line number
        const lineNumberSpan = document.createElement('span');
        lineNumberSpan.className = 'line-number';
        lineNumberSpan.textContent = lineNum;
        lineElement.appendChild(lineNumberSpan);
        
        // Add line content with potential error highlights
        const lineContentSpan = document.createElement('span');
        lineContentSpan.className = 'line-content';
        
        if (lineErrors.length > 0) {
          // Sort errors by column
          lineErrors.sort((a, b) => (a.column || 0) - (b.column || 0));
          
          // Build highlighted content
          let htmlContent = '';
          let lastPosition = 0;
          
          lineErrors.forEach(error => {
            const column = Math.max(0, (error.column || 1) - 1); // Convert to 0-based index
            
            // Add text before the error
            if (column > lastPosition) {
              htmlContent += escapeHtml(lineContent.substring(lastPosition, column));
            }
            
            // Determine how much text to highlight
            let errorLength = 1; // Default to 1 character
            
            if (column < lineContent.length) {
              // Try to find a reasonable length for the error highlight
              const restOfLine = lineContent.substring(column);
              const match = restOfLine.match(/^[\w]+|^\S+/);
              errorLength = match ? match[0].length : 1;
              
              // Special handling for specific error types
              if (error.code === 'readability-magic-numbers' || 
                  error.code === 'magic-numbers') {
                // Highlight numeric literals
                const numMatch = restOfLine.match(/^\d+(\.\d+)?/);
                errorLength = numMatch ? numMatch[0].length : errorLength;
              } else if (error.code === 'readability-identifier-length') {
                // Highlight short identifiers
                const idMatch = restOfLine.match(/^[a-zA-Z_]\w*/);
                errorLength = idMatch ? idMatch[0].length : errorLength;
              }
            }
            
            // Create the tooltip
            const errorId = `error-${lineNum}-${column}`;
            const tooltipCode = error.code || '';
            const tooltipMessage = error.message || 'Style issue';
            const tooltip = `<span class="error-code">${tooltipCode}</span> ${escapeHtml(tooltipMessage)}`;
            
            // Get the content to highlight
            const highlightContent = column < lineContent.length ? 
                                     lineContent.substring(column, column + errorLength) : 
                                     '⏎'; // Use symbol if we're at the end of line
            
            // Add the error highlight with tooltip
            htmlContent += `<span class="error-highlight" data-error-id="${errorId}">${escapeHtml(highlightContent)}<span class="error-tooltip" id="${errorId}-tooltip">${tooltip}</span></span>`;
            
            // Update position tracker
            lastPosition = column + errorLength;
          });
          
          // Add any remaining content after the last error
          if (lastPosition < lineContent.length) {
            htmlContent += escapeHtml(lineContent.substring(lastPosition));
          }
          
          lineContentSpan.innerHTML = htmlContent;
        } else {
          // No errors on this line, just add the plain text
          lineContentSpan.textContent = lineContent;
        }
        
        lineElement.appendChild(lineContentSpan);
        codeBlock.appendChild(lineElement);
      });
      
      codeDisplay.appendChild(codeBlock);
    }
    
    // Add code display to content area
    content.appendChild(codeDisplay);
    
    // Create error list
    if (errors.length > 0) {
      const errorList = document.createElement('div');
      errorList.className = 'error-list';
      
      // Add error list header
      const errorListHeader = document.createElement('div');
      errorListHeader.className = 'error-list-header';
      errorListHeader.textContent = 'Style Issues';
      errorList.appendChild(errorListHeader);
      
      // Add each error to the list
      errors.forEach(error => {
        const errorItem = document.createElement('div');
        errorItem.className = 'error-item';
        
        const location = document.createElement('span');
        location.className = 'error-location';
        location.textContent = `Line ${error.line || '?'}, Col ${error.column || '?'}: `;
        
        const code = document.createElement('span');
        code.className = 'error-code';
        code.textContent = error.code || '';
        
        const message = document.createElement('span');
        message.className = 'error-message';
        message.textContent = ` ${error.message || 'Style issue'}`;
        
        errorItem.appendChild(location);
        errorItem.appendChild(code);
        errorItem.appendChild(message);
        errorList.appendChild(errorItem);
      });
      
      content.appendChild(errorList);
    }
    
    // Add content to container
    styleCheckContainer.appendChild(content);
    
    // Add the container to the problem area
    resultDiv.appendChild(styleCheckContainer);
    
    // Hide check-answer and show return button
    const checkAnswerBtn = document.getElementById('check-answer-btn');
    const retryBtn = document.getElementById('retry-btn');
    
    if (checkAnswerBtn) checkAnswerBtn.style.display = 'none';
    if (retryBtn) retryBtn.style.display = 'inline-block';
    
    // Add event listeners for positioning tooltips
    setupTooltipPositioning();
  }
  
  // Restore the original problem content
  function restoreOriginalProblem() {
    // Get the problem content area
    const resultDiv = document.getElementById('result');
    if (!resultDiv) return;
    
    // Get the original content
    const originalContent = resultDiv.getAttribute('data-original-content');
    
    // If we have saved original content, restore it
    if (originalContent) {
      resultDiv.innerHTML = originalContent;
    }
    
    // Show/hide appropriate buttons
    const checkAnswerBtn = document.getElementById('check-answer-btn');
    const retryBtn = document.getElementById('retry-btn');
    
    if (checkAnswerBtn && currentProblemId) checkAnswerBtn.style.display = 'inline-block';
    if (retryBtn && !currentProblemId) retryBtn.style.display = 'none';
  }
  
  // Format C++ code using clang-format
  function formatCode(code, language) {
    if (!code || !code.trim()) {
      alert('No code to format');
      return;
    }
    
    // Disable all buttons to prevent multiple clicks
    const formatButton = document.querySelector('.format-button');
    const returnButton = document.querySelector('.return-button');
    
    if (formatButton) formatButton.disabled = true;
    if (returnButton) returnButton.disabled = true;
    
    if (formatButton) formatButton.textContent = 'Formatting...';
    
    // Call backend to format the code
    fetch('/format_code', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        code: code,
        language: language
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Format response:', data);
      
      if (data.success && data.formatted_code) {
        // Update editor with formatted code
        codeEditor.setValue(data.formatted_code);
        
        // Create a notification
        showNotification('Code formatted successfully!', 'success');
        
        // Replace the button with "Done!" text
        const formatButton = document.querySelector('.format-button');
        if (formatButton) {
          const doneText = document.createElement('span');
          doneText.textContent = 'Done!';
          doneText.className = 'format-done-text';
          doneText.style.color = '#4CAF50';
          doneText.style.fontWeight = 'bold';
          doneText.style.marginLeft = '10px';
          
          // Replace the button with text
          formatButton.parentNode.replaceChild(doneText, formatButton);
        }
      } else {
        // Show error
        const errorMsg = data.error || 'Failed to format code';
        showNotification(errorMsg, 'error');
      }
    })
    .catch(error => {
      console.error('Error formatting code:', error);
      showNotification('Error formatting code: ' + error.message, 'error');
    })
    .finally(() => {
      // Re-enable buttons
      if (formatButton) {
        formatButton.disabled = false;
        formatButton.textContent = 'Format Code';
      }
      if (returnButton) returnButton.disabled = false;
    });
  }
  
  // Utility function to escape HTML special characters
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  // Show a notification message
  function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Add styles directly to the element
    Object.assign(notification.style, {
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      padding: '10px 20px',
      backgroundColor: type === 'error' ? '#f44336' : '#4CAF50',
      color: 'white',
      borderRadius: '4px',
      boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
      zIndex: '10000',
      transition: 'opacity 0.5s'
    });
    
    // Add to document
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
      notification.style.opacity = '0';
      setTimeout(() => {
        notification.remove();
      }, 500);
    }, 3000);
  }
  
  // Set up tooltip positioning based on mouse position
  function setupTooltipPositioning() {
    // Find all error highlights
    const highlights = document.querySelectorAll('.error-highlight');
    
    // Add mouseover event to each highlight
    highlights.forEach(highlight => {
      highlight.addEventListener('mouseover', function(e) {
        const tooltipId = this.getAttribute('data-error-id') + '-tooltip';
        const tooltip = document.getElementById(tooltipId);
        
        if (tooltip) {
          // Position the tooltip at the mouse coordinates
          const rect = this.getBoundingClientRect();
          tooltip.style.left = e.clientX + 'px';
          tooltip.style.top = (rect.top - 10) + 'px';
        }
      });
    });
  }
  
  // Public API
  return {
    init: init,
    runStyleCheck: runStyleCheck,
    restoreOriginalProblem: restoreOriginalProblem,
    formatCode: formatCode
  };
})();

// Initialize the module when the document is ready
document.addEventListener('DOMContentLoaded', function() {
  // Initialize after a short delay to ensure other elements are loaded
  setTimeout(styleCheck.init, 500);
  
  // Add console log for debugging
  console.log('Style check module initialized');
});
