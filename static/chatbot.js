// Chatbot functionality
let chatWindow;
let chatButton;
let chatMessages;
let chatForm;
let chatInput;
let closeChat;
let conversationId = null; // To maintain conversation history with Dify API

// Initialize the chatbot
document.addEventListener('DOMContentLoaded', () => {
  chatWindow = document.getElementById('chat-window');
  chatButton = document.getElementById('chat-button');
  chatMessages = document.getElementById('chat-messages');
  chatForm = document.getElementById('chat-form');
  chatInput = document.getElementById('chat-input');
  closeChat = document.getElementById('close-chat');

  // Event listeners
  chatButton.addEventListener('click', toggleChatWindow);
  closeChat.addEventListener('click', toggleChatWindow);
  chatForm.addEventListener('submit', handleChatSubmit);

  // Add initial greeting message
  setTimeout(() => {
    addBotMessage("Hello! I'm your AI assistant. How can I help you with your coding problem?");
  }, 1000);
});

// Toggle chat window
function toggleChatWindow() {
  chatWindow.classList.toggle('open');
  if (chatWindow.classList.contains('open')) {
    chatInput.focus();
  }
}

// Handle chat form submission
function handleChatSubmit(e) {
  e.preventDefault();
  const message = chatInput.value.trim();
  if (!message) return;

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
  
  // Get the problem description
  const resultElement = document.getElementById('result');
  const currentProblem = resultElement ? resultElement.innerHTML : '';
  
  // Make sure we're getting the code from the global CodeMirror instance
  let currentCode = '';
  if (typeof codeEditor !== 'undefined' && codeEditor) {
    currentCode = codeEditor.getValue();
    console.log('Got code from editor:', currentCode.substring(0, 100) + '...');
  } else {
    console.warn('CodeMirror editor not found!');
  }

  // Get syllabus content (if available)
  let syllabus = '';
  // We'll try to get the syllabus for the current lesson
  fetchSyllabus(currentCourse, currentLesson)
    .then(syllabusContent => {
      console.log('Got syllabus:', syllabusContent ? 'yes' : 'no');
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

// Add bot message to chat window
function addBotMessage(message) {
  // Remove typing indicator if present
  const typingIndicator = document.querySelector('.typing-indicator');
  if (typingIndicator) {
    typingIndicator.remove();
  }

  const messageElement = document.createElement('div');
  messageElement.className = 'message bot-message';
  messageElement.textContent = message;
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
    
    const response = await fetch('/chatbot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        query,
        course,
        lesson,
        problem,
        code,
        syllabus,
        conversation_id: conversationId
      })
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
