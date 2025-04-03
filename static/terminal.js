// Terminal functionality for Problem Generator

class Terminal {
  constructor() {
    // DOM elements
    this.terminalOutput = document.getElementById('terminal-output');
    this.terminalInput = document.getElementById('terminal-input');
    this.clearTerminalBtn = document.getElementById('clear-terminal-btn');
    this.lockTerminalBtn = document.getElementById('lock-terminal-btn');
    
    // Terminal state
    this.isLocked = false;
    this.commandHistory = [];
    this.historyIndex = -1;
    this.allowedCommands = ["python", "python3", "javac", "java", "g++", "ls", "cat", "echo", "clear", "run"];
    
    // Bind methods
    this.handleInput = this.handleInput.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.clearTerminal = this.clearTerminal.bind(this);
    this.toggleLock = this.toggleLock.bind(this);
    this.runCommand = this.runCommand.bind(this);
    this.appendOutput = this.appendOutput.bind(this);
    this.executeCode = this.executeCode.bind(this);
    
    // Set up event listeners
    this.terminalInput.addEventListener('keydown', this.handleKeyDown);
    this.clearTerminalBtn.addEventListener('click', this.clearTerminal);
    this.lockTerminalBtn.addEventListener('click', this.toggleLock);
    
    // Initialize
    this.terminalInput.focus();
  }
  
  // Handle Enter key in input
  handleInput(command) {
    // Add command to history
    this.commandHistory.unshift(command);
    if (this.commandHistory.length > 50) {
      this.commandHistory.pop();
    }
    this.historyIndex = -1;
    
    // Show the command in the terminal
    this.appendOutput(`$ ${command}`, 'command-text');
    
    // Process the command
    if (command.trim().toLowerCase() === 'clear') {
      this.clearTerminal();
      return;
    }
    
    // Special 'run' command to execute current code
    if (command.trim().toLowerCase() === 'run') {
      this.executeCode();
      return;
    }
    
    // Execute normal command on the server
    this.runCommand(command);
  }
  
  // Handle keyboard navigation (up/down for history, etc.)
  handleKeyDown(event) {
    if (this.isLocked && event.key !== 'Tab') {
      event.preventDefault();
      return;
    }
    
    if (event.key === 'Enter') {
      const command = this.terminalInput.value.trim();
      if (command) {
        this.handleInput(command);
      }
      this.terminalInput.value = '';
      event.preventDefault();
    } else if (event.key === 'ArrowUp') {
      // Navigate command history (up)
      if (this.historyIndex < this.commandHistory.length - 1) {
        this.historyIndex++;
        this.terminalInput.value = this.commandHistory[this.historyIndex];
        // Move cursor to end
        setTimeout(() => {
          this.terminalInput.selectionStart = this.terminalInput.value.length;
          this.terminalInput.selectionEnd = this.terminalInput.value.length;
        }, 0);
      }
      event.preventDefault();
    } else if (event.key === 'ArrowDown') {
      // Navigate command history (down)
      if (this.historyIndex > 0) {
        this.historyIndex--;
        this.terminalInput.value = this.commandHistory[this.historyIndex];
      } else if (this.historyIndex === 0) {
        this.historyIndex--;
        this.terminalInput.value = '';
      }
      event.preventDefault();
    }
  }
  
  // Clear the terminal output
  clearTerminal() {
    this.terminalOutput.innerHTML = '';
    
    // Add welcome message
    const welcomeDiv = document.createElement('div');
    welcomeDiv.className = 'welcome-message';
    welcomeDiv.innerHTML = `
      <p>Welcome to Problem Generator Terminal</p>
      <p>Use 'run' to execute your code or type allowed commands.</p>
      <p>Allowed commands: ${this.allowedCommands.join(', ')}</p>
    `;
    this.terminalOutput.appendChild(welcomeDiv);
    
    // Focus the input
    this.terminalInput.focus();
  }
  
  // Toggle terminal lock state
  toggleLock() {
    this.isLocked = !this.isLocked;
    this.terminalInput.disabled = this.isLocked;
    this.lockTerminalBtn.textContent = this.isLocked ? 'Unlock' : 'Lock';
    
    if (!this.isLocked) {
      this.terminalInput.focus();
    }
    
    this.appendOutput(
      this.isLocked ? 'Terminal is now locked.' : 'Terminal is now unlocked.',
      'system-message'
    );
  }
  
  // Send command to server for execution
  runCommand(command) {
    // Check if command is allowed
    const cmdParts = command.trim().split(/\s+/);
    const baseCmd = cmdParts[0];
    
    if (!this.allowedCommands.includes(baseCmd)) {
      this.appendOutput(`Command not allowed: ${baseCmd}`, 'command-error');
      this.appendOutput('Allowed commands: ' + this.allowedCommands.join(', '), 'system-message');
      return;
    }
    
    // Lock the terminal during command execution
    const wasLocked = this.isLocked;
    this.isLocked = true;
    this.terminalInput.disabled = true;
    
    // Send to server
    fetch('/execute_command', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        command: command
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        this.appendOutput(data.error, 'command-error');
      } else {
        // Show stdout if any
        if (data.stdout && data.stdout.trim()) {
          this.appendOutput(data.stdout, 'command-output');
        }
        
        // Show stderr if any
        if (data.stderr && data.stderr.trim()) {
          this.appendOutput(data.stderr, 'command-error');
        }
        
        // Show return code if non-zero
        if (data.returncode !== 0) {
          this.appendOutput(`Command exited with code: ${data.returncode}`, 'command-error');
        }
      }
    })
    .catch(error => {
      this.appendOutput(`Error executing command: ${error.message}`, 'command-error');
    })
    .finally(() => {
      // Restore previous lock state
      this.isLocked = wasLocked;
      this.terminalInput.disabled = wasLocked;
      if (!wasLocked) {
        this.terminalInput.focus();
      }
    });
  }
  
  // Special method to execute the code in the editor
  executeCode() {
    // Get code from CodeMirror editor
    const code = codeEditor.getValue();
    const language = document.getElementById('language-select').value;
    
    if (!code.trim()) {
      this.appendOutput('No code to run!', 'command-error');
      return;
    }
    
    // Show what we're doing
    this.appendOutput(`Running ${language} code...`, 'system-message');
    
    // Lock the terminal during execution
    const wasLocked = this.isLocked;
    this.isLocked = true;
    this.terminalInput.disabled = true;
    
    // Get any input from the terminal's recent history
    // This is used as stdin for the program
    let stdin = '';
    if (this.commandHistory.length > 0) {
      // Look for the most recent non-command input (lines without $ prefix)
      const outputDivs = this.terminalOutput.querySelectorAll('.command-output');
      if (outputDivs.length > 0) {
        const lastOutput = outputDivs[outputDivs.length - 1];
        if (lastOutput.previousElementSibling && 
            lastOutput.previousElementSibling.textContent.includes('Enter input for your program:')) {
          stdin = lastOutput.textContent;
        }
      }
    }
    
    // Use the run_code endpoint
    fetch("/run_code", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        code, 
        stdin, 
        language 
      })
    })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        this.appendOutput(`Error: ${data.error}`, 'command-error');
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
      
      // Prompt for more input if needed
      this.appendOutput('Enter input for your program:', 'system-message');
    })
    .catch(err => {
      this.appendOutput(`Error running code: ${err}`, 'command-error');
    })
    .finally(() => {
      // Restore previous lock state
      this.isLocked = wasLocked;
      this.terminalInput.disabled = wasLocked;
      if (!wasLocked) {
        this.terminalInput.focus();
      }
    });
  }
  
  // Add output to the terminal
  appendOutput(text, className = '') {
    const output = document.createElement('div');
    output.className = className;
    output.textContent = text;
    this.terminalOutput.appendChild(output);
    
    // Scroll to bottom
    this.terminalOutput.scrollTop = this.terminalOutput.scrollHeight;
  }
  
  // Set terminal lock state programmatically
  setLock(locked) {
    if (this.isLocked !== locked) {
      this.toggleLock();
    }
  }
}

// Initialize terminal when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.terminal = new Terminal();
});
