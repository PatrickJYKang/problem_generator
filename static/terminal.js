// Real Terminal Implementation using xterm.js and Socket.IO
class Terminal {
  constructor() {
    // DOM elements
    this.containerElement = document.getElementById('terminal-container');
    this.xtermContainer = document.getElementById('xterm-container');
    this.clearButton = document.getElementById('clear-terminal-btn');
    
    // Terminal state
    this.isRunningProgram = false;
    this.socket = null;
    this.term = null;
    this.fitAddon = null;
    this.linksAddon = null;
    
    // Initialize terminal
    this.initialize();
  }
  
  // Initialize terminal with all components
  initialize() {
    // Initialize Socket.IO connection
    this.initializeSocketConnection();
    
    // Initialize xterm.js terminal
    this.initializeTerminal();
    
    // Set up event listeners
    this.clearButton.addEventListener('click', () => this.clearTerminal());
    
    // Handle window resize
    window.addEventListener('resize', () => this.fitTerminal());
    
    // Add theme change handler
    this.setupThemeListener();
  }
  
  // Initialize Socket.IO connection to the server
  initializeSocketConnection() {
    // Connect to the Socket.IO server with robust settings
    this.socket = io({
      reconnectionAttempts: 5,   // Number of reconnection attempts
      reconnectionDelay: 1000,   // Start with 1s delay
      reconnectionDelayMax: 5000, // Max 5s delay
      timeout: 20000,           // Longer connection timeout
      transports: ['websocket', 'polling'] // Try WebSocket first, fallback to polling
    });
    
    // Socket.IO event handlers
    this.socket.on('connect', () => {
      console.log('Connected to terminal server');
    });
    
    this.socket.on('disconnect', () => {
      console.log('Disconnected from terminal server');
      if (this.term) {
        this.term.writeln('\r\n\x1b[1;31mDisconnected from terminal server\x1b[0m');
      }
    });
    
    this.socket.on('terminal_ready', () => {
      console.log('Terminal session ready');
    });
    
    this.socket.on('terminal_output', (data) => {
      if (this.term) {
        this.term.write(data.output);
      }
    });
    
    this.socket.on('terminal_exit', () => {
      if (this.term) {
        this.term.writeln('\r\n\x1b[1;33mTerminal session ended\x1b[0m');
      }
      this.isRunningProgram = false;
    });
    
    this.socket.on('terminal_error', (data) => {
      if (this.term) {
        this.term.writeln(`\r\n\x1b[1;31mError: ${data.message}\x1b[0m`);
      }
    });
  }
  
  // Initialize the xterm.js terminal
  initializeTerminal() {
    // Create xterm.js terminal instance
    this.term = new Terminal({
      cursorBlink: true,
      fontSize: 14,
      fontFamily: 'Menlo, Monaco, "Courier New", monospace',
      rows: 24,
      cols: 80,
      scrollback: 1000,
      theme: this.getCurrentThemeColors()
    });
    
    // Create and load the FitAddon
    this.fitAddon = new FitAddon.FitAddon();
    this.term.loadAddon(this.fitAddon);
    
    // Create and load the WebLinksAddon
    this.linksAddon = new WebLinksAddon.WebLinksAddon();
    this.term.loadAddon(this.linksAddon);
    
    // Open the terminal in its container
    this.term.open(this.xtermContainer);
    
    // Set up input handler - send keystrokes to the server
    this.term.onData(data => {
      if (this.socket && this.isRunningProgram) {
        this.socket.emit('terminal_input', { input: data });
      }
    });
    
    // Set up resize handler
    this.term.onResize(size => {
      if (this.socket && this.isRunningProgram) {
        this.socket.emit('terminal_resize', { 
          cols: size.cols, 
          rows: size.rows 
        });
      }
    });
    
    // Initial fit
    setTimeout(() => this.fitTerminal(), 100);
    
    // Show welcome message
    this.term.writeln('\x1b[1;34mWelcome to Problem Generator Terminal\x1b[0m');
    this.term.writeln('This is a real terminal that allows input and output from your programs.');
    this.term.writeln('Press the Run button to execute your code in this terminal.');
    this.term.writeln('');
  }
  
  // Make the terminal fit its container
  fitTerminal() {
    if (this.fitAddon) {
      try {
        this.fitAddon.fit();
        
        // Send new dimensions to server
        if (this.socket && this.isRunningProgram) {
          this.socket.emit('terminal_resize', { 
            cols: this.term.cols, 
            rows: this.term.rows 
          });
        }
      } catch (err) {
        console.error('Error fitting terminal:', err);
      }
    }
  }
  
  // Clear the terminal output
  clearTerminal() {
    if (this.term) {
      this.term.clear();
    }
  }
  
  // Get terminal colors based on the current theme
  getCurrentThemeColors() {
    const isDarkTheme = document.documentElement.getAttribute('data-theme') === 'dark';
    
    // Return appropriate terminal colors based on theme
    return isDarkTheme ? {
      background: '#1e1e1e',
      foreground: '#f0f0f0',
      cursor: '#f0f0f0',
      cursorAccent: '#1e1e1e',
      selection: 'rgba(255, 255, 255, 0.3)',
      black: '#000000',
      red: '#ff5555',
      green: '#50fa7b',
      yellow: '#f1fa8c',
      blue: '#bd93f9',
      magenta: '#ff79c6',
      cyan: '#8be9fd',
      white: '#bbbbbb',
      brightBlack: '#555555',
      brightRed: '#ff6e6e',
      brightGreen: '#69ff94',
      brightYellow: '#ffffa5',
      brightBlue: '#d6acff',
      brightMagenta: '#ff92df',
      brightCyan: '#a4ffff',
      brightWhite: '#ffffff'
    } : {
      background: '#f5f5f5',
      foreground: '#333333',
      cursor: '#333333',
      cursorAccent: '#f5f5f5',
      selection: 'rgba(0, 0, 0, 0.3)',
      black: '#000000',
      red: '#c91b00',
      green: '#00c200',
      yellow: '#c7c400',
      blue: '#0225c7',
      magenta: '#c930c7',
      cyan: '#00c5c7',
      white: '#c7c7c7',
      brightBlack: '#676767',
      brightRed: '#ff6d67',
      brightGreen: '#5ff967',
      brightYellow: '#fefb67',
      brightBlue: '#6871ff',
      brightMagenta: '#ff76ff',
      brightCyan: '#5ffdff',
      brightWhite: '#ffffff'
    };
  }

  // Update terminal theme when dark/light mode changes
  updateTheme() {
    if (this.term) {
      this.term.options.theme = this.getCurrentThemeColors();
      this.term.refresh();
    }
  }
  
  // Set up listener for theme changes
  setupThemeListener() {
    // Watch for theme attribute changes on the document element
    const observer = new MutationObserver(mutations => {
      mutations.forEach(mutation => {
        if (mutation.attributeName === 'data-theme') {
          this.updateTheme();
        }
      });
    });
    
    observer.observe(document.documentElement, { attributes: true });
  }
  
  // Execute the code in the editor using a real terminal
  executeCode() {
    // Get code from CodeMirror editor
    const code = codeEditor.getValue();
    const language = document.getElementById('language-select').value;
    
    if (!code.trim()) {
      if (this.term) {
        this.term.writeln('\r\n\x1b[1;31mNo code to run!\x1b[0m');
      }
      return;
    }
    
    // Clear terminal and show running message
    this.clearTerminal();
    if (this.term) {
      this.term.writeln(`\x1b[1;32mRunning ${language} code...\x1b[0m\r\n`);
    }
    
    // Set running state
    this.isRunningProgram = true;
    
    // Kill any existing terminal session
    if (this.socket) {
      this.socket.emit('terminal_kill');
    }
    
    // Start a new terminal session with the code
    if (language === 'python') {
      this.socket.emit('run_python_code', { code });
    } else {
      // For other languages, we would need to implement handlers on the server
      if (this.term) {
        this.term.writeln(`\x1b[1;33mRunning ${language} code directly in terminal is not yet supported\x1b[0m`);
      }
      
      // Fallback to the regular run_code endpoint
      fetch("/run_code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          code, 
          stdin: "", 
          language 
        })
      })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          this.term.writeln(`\x1b[1;31mError: ${data.error}\x1b[0m`);
          return;
        }
        
        // Display output
        if (data.stdout && data.stdout.trim()) {
          this.term.writeln(data.stdout);
        }
        
        // Display errors
        if (data.stderr && data.stderr.trim()) {
          this.term.writeln(`\x1b[1;31m${data.stderr}\x1b[0m`);
        }
        
        // If no output at all, say so
        if ((!data.stdout || !data.stdout.trim()) && (!data.stderr || !data.stderr.trim())) {
          this.term.writeln('(No output)');
        }
        
        this.isRunningProgram = false;
      })
      .catch(err => {
        this.term.writeln(`\x1b[1;31mError running code: ${err.message || err}\x1b[0m`);
        this.isRunningProgram = false;
      });
    }
  }
}

// Connect the terminal to the run button
function connectTerminalToRunButton() {
  const runBtn = document.getElementById('run-btn');
  if (runBtn && window.terminal) {
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
