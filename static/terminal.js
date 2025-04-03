// Real Terminal Implementation for Problem Generator

class Terminal {
  constructor() {
    // DOM elements
    this.terminalContainer = document.getElementById('terminal-container');
    this.terminalOutput = document.getElementById('terminal-output');
    this.clearTerminalBtn = document.getElementById('clear-terminal-btn');
    this.lockTerminalBtn = document.getElementById('lock-terminal-btn');
    
    // Terminal state
    this.isLocked = true; // Start locked by default
    this.isRunningProgram = false;
    this.canAcceptInput = false;
    this.commandHistory = [];
    this.historyIndex = -1;
    this.currentInput = '';
    this.cursorPosition = 0;
    this.commandPrompt = '$';
    
    // Create cursor element - this will be moved as needed
    this.cursor = document.createElement('span');
    this.cursor.className = 'terminal-cursor';
    this.cursor.style.display = 'none';
    
    // Create the current line display
    this.currentLineElement = null;
    
    // Bind methods
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.clearTerminal = this.clearTerminal.bind(this);
    this.toggleLock = this.toggleLock.bind(this);
    this.appendOutput = this.appendOutput.bind(this);
    this.executeCode = this.executeCode.bind(this);
    this.processCommand = this.processCommand.bind(this);
    this.startProgramRun = this.startProgramRun.bind(this);
    this.endProgramRun = this.endProgramRun.bind(this);
    this.renderCurrentInput = this.renderCurrentInput.bind(this);
    
    // Set up event listeners
    document.addEventListener('keydown', this.handleKeyDown);
    this.clearTerminalBtn.addEventListener('click', this.clearTerminal);
    this.lockTerminalBtn.addEventListener('click', this.toggleLock);
    
    // Initialize terminal
    this.initialize();
  }
  
  // Initialize terminal with welcome message
  initialize() {
  
    // Show welcome message
    this.appendOutput('Welcome to Problem Generator Terminal', 'welcome-message');
    this.appendOutput('This terminal only accepts input when running a program.', 'welcome-message');
    this.appendOutput('The code editor will use this terminal for input/output.', 'welcome-message');
    this.appendOutput('', 'empty-line');
    
    // Lock the terminal by default
    this.updateLockStatus();
  }
  
  // Handle all keyboard input to the terminal
  handleKeyDown(event) {
    // Only process keyboard input if we're accepting input (during program execution)
    if (!this.canAcceptInput) return;
    
    // Prevent default for most keys when terminal is active
    if ((event.key.length === 1 || 
        event.key === 'Enter' || 
        event.key === 'Backspace' || 
        event.key === 'ArrowLeft' || 
        event.key === 'ArrowRight' || 
        event.key === 'ArrowUp' || 
        event.key === 'ArrowDown') && 
        this.isRunningProgram) {
      event.preventDefault();
    } else {
      return; // Let other keys through
    }
    
    // Handle Enter key
    if (event.key === 'Enter') {
      const input = this.currentInput;
      
      // Add a new line after the current input
      this.appendOutput('', 'empty-line');
      
      // Add to history if not empty
      if (input.trim()) {
        this.commandHistory.unshift(input);
        if (this.commandHistory.length > 50) {
          this.commandHistory.pop();
        }
      }
      
      // Reset input state
      this.historyIndex = -1;
      this.currentInput = '';
      this.cursorPosition = 0;
      
      // Process the input for the running program
      if (this.isRunningProgram) {
        // In a real implementation, this would pass the input to the running program
        // For now we'll just echo it back
        this.sendInputToProgram(input);
      }
      
      // Create a new line for new input
      this.renderCurrentInput();
      return;
    }
    
    // Handle Backspace
    if (event.key === 'Backspace') {
      if (this.cursorPosition > 0) {
        this.currentInput = 
          this.currentInput.substring(0, this.cursorPosition - 1) + 
          this.currentInput.substring(this.cursorPosition);
        this.cursorPosition--;
        this.renderCurrentInput();
      }
      return;
    }
    
    // Handle arrow keys
    if (event.key === 'ArrowLeft') {
      if (this.cursorPosition > 0) {
        this.cursorPosition--;
        this.renderCurrentInput();
      }
      return;
    }
    
    if (event.key === 'ArrowRight') {
      if (this.cursorPosition < this.currentInput.length) {
        this.cursorPosition++;
        this.renderCurrentInput();
      }
      return;
    }
    
    if (event.key === 'ArrowUp') {
      if (this.historyIndex < this.commandHistory.length - 1) {
        this.historyIndex++;
        this.currentInput = this.commandHistory[this.historyIndex];
        this.cursorPosition = this.currentInput.length;
        this.renderCurrentInput();
      }
      return;
    }
    
    if (event.key === 'ArrowDown') {
      if (this.historyIndex > 0) {
        this.historyIndex--;
        this.currentInput = this.commandHistory[this.historyIndex];
      } else if (this.historyIndex === 0) {
        this.historyIndex = -1;
        this.currentInput = '';
      }
      this.cursorPosition = this.currentInput.length;
      this.renderCurrentInput();
      return;
    }
    
    // Handle regular character input
    if (event.key.length === 1) {
      this.currentInput = 
        this.currentInput.substring(0, this.cursorPosition) + 
        event.key + 
        this.currentInput.substring(this.cursorPosition);
      this.cursorPosition++;
      this.renderCurrentInput();
    }
  }
  
  // Render the current input line with proper cursor positioning
  renderCurrentInput() {
    // Remove previous line if it exists
    if (this.currentLineElement) {
      this.currentLineElement.remove();
    }
    
    // Create new line
    this.currentLineElement = document.createElement('div');
    this.currentLineElement.className = 'terminal-input-display';
    
    // Add prompt
    const promptSpan = document.createElement('span');
    promptSpan.className = 'terminal-prompt';
    promptSpan.textContent = this.commandPrompt + ' ';
    this.currentLineElement.appendChild(promptSpan);
    
    // Add text before cursor
    if (this.cursorPosition > 0) {
      const beforeCursor = document.createElement('span');
      beforeCursor.textContent = this.currentInput.substring(0, this.cursorPosition);
      this.currentLineElement.appendChild(beforeCursor);
    }
    
    // Add cursor
    const cursor = document.createElement('span');
    cursor.className = 'terminal-cursor';
    this.currentLineElement.appendChild(cursor);
    
    // Add text after cursor
    if (this.cursorPosition < this.currentInput.length) {
      const afterCursor = document.createElement('span');
      afterCursor.textContent = this.currentInput.substring(this.cursorPosition);
      this.currentLineElement.appendChild(afterCursor);
    }
    
    this.terminalOutput.appendChild(this.currentLineElement);
    this.scrollToBottom();
  }
  
  // Clear the terminal output
  clearTerminal() {
    this.terminalOutput.innerHTML = '';
    
    // Show welcome message again
    this.appendOutput('Welcome to Problem Generator Terminal', 'welcome-message');
    this.appendOutput('This terminal only accepts input when running a program.', 'welcome-message');
    this.appendOutput('The code editor will use this terminal for input/output.', 'welcome-message');
    this.appendOutput('', 'empty-line');
    
    // If we're currently running a program, show the input prompt
    if (this.isRunningProgram) {
      this.renderCurrentInput();
    }
  }
  
  // Toggle terminal lock state (only affects button display, real input is controlled by program state)
  toggleLock() {
    this.isLocked = !this.isLocked;
    this.updateLockStatus();
    
    this.appendOutput(
      this.isLocked ? 'Terminal is now locked.' : 'Terminal is now unlocked.',
      'system-message'
    );
  }
  
  // Update the visual lock status
  updateLockStatus() {
    this.lockTerminalBtn.textContent = this.isLocked ? 'Unlock' : 'Lock';
  }
  
  // Process a command (only used for internal commands during program execution)
  processCommand(command) {
    // For now, we just support the clear command
    if (command.trim().toLowerCase() === 'clear') {
      this.clearTerminal();
      return true;
    }
    return false;
  }
  
  // Start a program execution
  startProgramRun() {
    this.isRunningProgram = true;
    this.canAcceptInput = true;
    this.appendOutput('Program is running. Terminal is now accepting input...', 'system-message');
    this.currentInput = '';
    this.cursorPosition = 0;
    this.renderCurrentInput();
    
    // Focus the terminal
    this.terminalContainer.focus();
  }
  
  // End program execution
  endProgramRun() {
    this.isRunningProgram = false;
    this.canAcceptInput = false;
    this.appendOutput('Program execution completed. Terminal is now read-only.', 'system-message');
    
    // Remove the current input line
    if (this.currentLineElement) {
      this.currentLineElement.remove();
      this.currentLineElement = null;
    }
  }
  
  // Send input to the running program
  sendInputToProgram(input) {
    // In a real implementation, this would communicate with the backend
    // For now, we'll just log it
    console.log('Input sent to program:', input);
  }
  
  // Execute the code in the editor - this is called by the run button in the UI
  executeCode() {
    // Get code from CodeMirror editor
    const code = codeEditor.getValue();
    const language = document.getElementById('language-select').value;
    
    if (!code.trim()) {
      this.appendOutput('No code to run!', 'command-error');
      return;
    }
    
    // Clear any previous output first
    this.clearTerminal();
    
    // Show what we're doing
    this.appendOutput(`Running ${language} code...`, 'system-message');
    
    // Enable terminal input for this execution
    this.startProgramRun();
    
    // Use the run_code endpoint
    fetch("/run_code", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        code, 
        stdin: "", // We'll handle stdin differently now - through real-time interaction 
        language 
      })
    })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        this.appendOutput(`Error: ${data.error}`, 'command-error');
        this.endProgramRun();
        return;
      }
      
      // Display output
      if (data.stdout && data.stdout.trim()) {
        this.appendOutput(data.stdout, 'command-output');
      }
      
      // Display errors
      if (data.stderr && data.stderr.trim()) {
        this.appendOutput(data.stderr, 'command-error');
      }
      
      // If no output at all, say so
      if ((!data.stdout || !data.stdout.trim()) && (!data.stderr || !data.stderr.trim())) {
        this.appendOutput('(No output)', 'system-message');
      }
      
      // End the program run
      this.endProgramRun();
    })
    .catch(err => {
      this.appendOutput(`Error running code: ${err.message || err}`, 'command-error');
      this.endProgramRun();
    });
  }
  
  // Add output to the terminal
  appendOutput(text, className = '') {
    const output = document.createElement('div');
    output.className = className;
    output.textContent = text;
    this.terminalOutput.appendChild(output);
    this.scrollToBottom();
  }
  
  // Scroll to the bottom of the terminal
  scrollToBottom() {
    this.terminalOutput.scrollTop = this.terminalOutput.scrollHeight;
  }
  
  // Set terminal lock state programmatically
  setLock(locked) {
    if (this.isLocked !== locked) {
      this.toggleLock();
    }
  }
}

// Connect the terminal to the run button
function connectTerminalToRunButton() {
  const runBtn = document.getElementById('run-btn');
  if (runBtn && window.terminal) {
    // Replace the old event listener with our new one
    const oldListeners = runBtn.getEventListeners?.('click') || [];
    oldListeners.forEach(listener => {
      runBtn.removeEventListener('click', listener.listener);
    });
    
    // Add the new listener that uses our terminal
    runBtn.addEventListener('click', () => {
      window.terminal.executeCode();
    });
  }
}

// Function to initialize the terminal once the page is loaded
function initTerminal() {
  // Create terminal instance if it doesn't exist
  if (!window.terminal) {
    window.terminal = new Terminal();
  }
  
  // Connect it to the run button
  connectTerminalToRunButton();
}

// Initialize terminal when DOM is loaded
document.addEventListener('DOMContentLoaded', initTerminal);

// Also ensure it's initialized if the script loads after DOMContentLoaded
if (document.readyState === 'complete' || document.readyState === 'interactive') {
  setTimeout(initTerminal, 100);
}
