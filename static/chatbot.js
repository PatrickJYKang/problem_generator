// Chatbot functionality - Using an IIFE to avoid global variable conflicts
(function() {
  // Private variables encapsulated in this function scope
  let chatWindow;
  let chatButton;
  let chatMessages;
  let chatForm;
  let chatInput;
  let chatSubmitBtn;
  let conversationId = null; // To maintain conversation history with Dify API

  // Initialize the chatbot when the document is ready
  document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing chatbot...');
    
    // Get all the DOM elements
    chatWindow = document.getElementById('chat-window');
    chatButton = document.getElementById('chat-button');
    chatMessages = document.getElementById('chat-messages');
    chatForm = document.getElementById('chat-form');
    chatInput = document.getElementById('chat-input');
    chatSubmitBtn = document.getElementById('chat-submit-btn');
    
    console.log('Chat elements found:', {
      chatWindow: !!chatWindow,
      chatButton: !!chatButton,
      chatMessages: !!chatMessages,
      chatForm: !!chatForm,
      chatInput: !!chatInput,
      chatSubmitBtn: !!chatSubmitBtn
    });

    // Setup event listeners
    if (chatButton) {
      chatButton.addEventListener('click', toggleChatWindow);
    }
    
    if (chatSubmitBtn) {
      console.log('Adding click handler to send button');
      chatSubmitBtn.addEventListener('click', function() {
        console.log('Send button clicked!');
        handleChatSubmit();
      });
    }
    
    if (chatInput) {
      chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          console.log('Enter key pressed in chat input');
          handleChatSubmit();
        }
      });
    }

    // Add initial greeting message
    setTimeout(function() {
      addBotMessage("Hello! I'm your AI assistant. How can I help you with your coding problem?");
    }, 1000);
    
    // Expose the reset function globally
    window.resetChat = resetChatConversation;
  });

  // Toggle chat window
  function toggleChatWindow() {
  chatWindow.classList.toggle('open');
  document.body.classList.toggle('chat-open'); // Toggle body class for the push-in effect
  
  if (chatWindow.classList.contains('open')) {
    chatInput.focus();
  }
}

  // Handle chat form submission
  function handleChatSubmit(e) {
  if (e) e.preventDefault(); // Ensure this always runs
  console.log('Chat form submitted, preventing default behavior');
  const message = chatInput.value.trim();
  if (!message) return false;

  // Add user message to chat
  addUserMessage(message);
  chatInput.value = '';

  // Show typing indicator
  const typingIndicator = document.createElement('div');
  typingIndicator.className = 'typing-indicator';
  typingIndicator.innerHTML = '<span></span><span></span><span></span>';
  chatMessages.appendChild(typingIndicator);
  scrollToBottom();

  // Get current state of the application
  const currentCourse = document.getElementById('course-select').value;
  const currentLesson = document.getElementById('lesson-select').value;
  const currentProblem = document.getElementById('result').innerHTML;
  const currentCode = codeEditor.getValue();

  // Get syllabus content (if available)
  let syllabus = '';
  // We'll try to get the syllabus for the current lesson
  fetchSyllabus(currentCourse, currentLesson)
    .then(syllabusContent => {
      // Now we have all the data needed to send to the chatbot API
      sendChatRequest(message, currentCourse, currentLesson, currentProblem, currentCode, syllabusContent);
    })
    .catch(error => {
      console.error('Error fetching syllabus:', error);
      // Still send the request without syllabus
      sendChatRequest(message, currentCourse, currentLesson, currentProblem, currentCode, '');
    });
}

  // Add user message to chat window
  function addUserMessage(message) {
  const messageElement = document.createElement('div');
  messageElement.className = 'message user-message';
  messageElement.textContent = message;
  chatMessages.appendChild(messageElement);
  scrollToBottom();
}

  // Add bot message to chat window with markdown support
  function addBotMessage(message) {
    // Remove any typing indicators
    const typingIndicators = chatMessages.querySelectorAll('.typing-indicator');
    typingIndicators.forEach(indicator => indicator.remove());
    
    const messageElement = document.createElement('div');
    messageElement.className = 'message bot-message';
    
    // Process markdown in the message
    const formattedMessage = marked.parse(message);
    messageElement.innerHTML = formattedMessage;
    
    // Render LaTeX formulas in the message
    try {
      if (typeof renderMathInElement === 'function') {
        renderMathInElement(messageElement, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false},
            {left: '\\(', right: '\\)', display: false},
            {left: '\\[', right: '\\]', display: true}
          ],
          throwOnError: false
        });
      }
    } catch (e) {
      console.error('Error rendering LaTeX in chat message:', e);
    }
    
    // Add code highlighting to any code blocks
    const codeBlocks = messageElement.querySelectorAll('pre code');
    if (codeBlocks.length) {
      codeBlocks.forEach(block => {
        // Add a copy button to code blocks
        const codeContainer = block.parentNode;
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-code-btn';
        copyButton.textContent = 'Copy';
        copyButton.addEventListener('click', function() {
          const code = block.textContent;
          navigator.clipboard.writeText(code).then(() => {
            // Visual feedback
            copyButton.textContent = 'Copied!';
            setTimeout(() => {
              copyButton.textContent = 'Copy';
            }, 2000);
          });
        });
        
        // Add copy button to pre element
        codeContainer.style.position = 'relative';
        codeContainer.appendChild(copyButton);
        
        // Apply syntax highlighting (if hljs is available)
        if (window.hljs) {
          hljs.highlightElement(block);
        }
      });
    }
    
    chatMessages.appendChild(messageElement);
    scrollToBottom();
  }

  // Helper function to scroll chat to bottom
  function scrollToBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

  // Fetch syllabus for the current lesson (simplified approach)
  async function fetchSyllabus(course, lesson) {
  if (!course || !lesson) return '';
  
  try {
    console.log(`Fetching syllabus for ${course}/${lesson}`);
    
    // Just fetch the current lesson to keep the payload smaller
    try {
      const lessonResponse = await fetch(`/syllabi/${course}/en/${lesson}.md`);
      if (lessonResponse.ok) {
        const lessonText = await lessonResponse.text();
        return `## ${lesson}\n${lessonText}`;
      } else {
        console.warn(`Couldn't fetch lesson ${lesson}, trying to get index`);
      }
    } catch (error) {
      console.error(`Error fetching specific lesson ${lesson}:`, error);
    }
    
    // If we couldn't get the specific lesson, try the index approach
    const response = await fetch(`/syllabi/${course}/en/index.json`);
    if (!response.ok) {
      throw new Error('Failed to fetch index.json');
    }
    
    const indexData = await response.json();
    let syllabusContent = '';
    let foundLesson = false;
    
    // Only get the current lesson from the index
    for (const category in indexData) {
      if (typeof indexData[category] === 'object' && !foundLesson) {
        for (const lessonKey in indexData[category]) {
          if (lessonKey === lesson) {
            foundLesson = true;
            try {
              const lessonResponse = await fetch(`/syllabi/${course}/en/${lessonKey}.md`);
              if (lessonResponse.ok) {
                const lessonText = await lessonResponse.text();
                syllabusContent = `## ${lessonKey}\n${lessonText}`;
                break;
              }
            } catch (error) {
              console.error(`Error fetching lesson ${lessonKey}:`, error);
            }
          }
        }
      }
    }
    
    return syllabusContent;
  } catch (error) {
    console.error('Error fetching syllabus:', error);
    return '';
  }
}

  // Reset chat conversation
  function resetChatConversation() {
  // Reset the conversation ID
  conversationId = null;
  
  // Clear all messages except the initial greeting
  if (chatMessages) {
    // Keep only the first message (greeting) if it exists
    const messages = chatMessages.querySelectorAll('.message');
    if (messages.length > 1) {
      // Remove all but the first message
      for (let i = messages.length - 1; i > 0; i--) {
        messages[i].remove();
      }
    } else if (messages.length === 0) {
      // If no messages, add a greeting
      addBotMessage("Hello! I'm your AI assistant. How can I help you with your coding problem?");
    }
  }
  
  console.log('Chat conversation has been reset');
}

  // Send chat request to backend
  async function sendChatRequest(query, course, lesson, problem, code, syllabus) {
  try {
    console.log('Sending chat request with:', { query, course, lesson });
    
    // Limit the size of code and syllabus to prevent payload issues
    if (code && code.length > 50000) {
      code = code.substring(0, 50000) + '\n... (truncated for size)'; 
    }
    
    if (syllabus && syllabus.length > 50000) {
      syllabus = syllabus.substring(0, 50000) + '\n... (truncated for size)';
    }
    
    // Determine the appropriate language based on the course
    let language;
    if (course === 'csa') {
      // AP Computer Science A uses Java
      language = 'java';
    } else if (course.toLowerCase().includes('python')) {
      language = 'python';
    } else if (course.toLowerCase().includes('java')) {
      language = 'java';
    } else if (course.toLowerCase().includes('cpp') || course.toLowerCase().includes('c++')) {
      language = 'cpp';
    } else {
      // Default to Python if course doesn't match any known language
      language = 'python';
    }
    
    console.log(`Determined language for course ${course}: ${language}`);
    
    // Create request data - using same format that works with generate endpoint
    const requestData = {
      query,
      course,
      lesson,
      problem,
      code,
      syllabus,
      language, // Add the language parameter explicitly
      conversation_id: conversationId,
      user: 'end_user' // Required parameter
    };
    
    console.log('Sending request data:', requestData);
    
    const response = await fetch('/chatbot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    });

    const data = await response.json();
    console.log('Chat response received:', data);
    
    // Handle error returned with 200 status (our custom error format)
    if (data.error) {
      console.warn('API returned error:', data.error);
      if (data.answer) {
        addBotMessage(data.answer);
      } else {
        addBotMessage("Sorry, there was an error communicating with the AI assistant. Please try again later.");
      }
      return;
    }
    
    // Save conversation ID for continuity
    if (data.conversation_id) {
      conversationId = data.conversation_id;
    }

    // Display bot response
    if (data.answer) {
      addBotMessage(data.answer);
    } else if (data.id) {
      // Handle Dify streaming response format
      addBotMessage(data.text || "I received your message and am processing it.");
    } else {
      addBotMessage("I'm sorry, I couldn't process your request at this time.");
    }
  } catch (error) {
    console.error('Error sending chat request:', error);
    addBotMessage("Sorry, there was an error communicating with the AI assistant. Please try again later.");
  }
}

// Close the IIFE
})();
