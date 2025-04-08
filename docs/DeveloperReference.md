# Developer Reference

This document serves as a comprehensive technical reference for the Problem Generator application.

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Backend Components](#backend-components)
- [Frontend Components](#frontend-components)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [External Integrations](#external-integrations)
- [Development Workflow](#development-workflow)
- [Deployment Guide](#deployment-guide)

## Architecture Overview

### High-Level Architecture

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart TD
    User([User]) <--> WebUI[Web Interface]    
    
    subgraph Frontend
        WebUI --> CodeEditor[CodeMirror Editor]
        WebUI --> ChatInterface[AI Assistant UI]
        WebUI --> ProblemDisplay[Problem Display]
        WebUI --> ResultsViewer[Results Viewer]
    end
    
    subgraph Backend
        API[Flask API] --> ProblemGenerator[Problem Generator]
        API --> CodeExecutor[Code Executor]
        API --> TestRunner[Test Runner]
        API --> GitHubFetcher[GitHub Fetcher]
        API --> ChatbotHandler[Chatbot Handler]
        
        ProblemGenerator --> AIService[AI Service]
        ChatbotHandler --> AIService
    end
    
    WebUI <--> API
    
    classDef userNode fill:#4A5568,stroke:#CBD5E0,color:#E2E8F0
    classDef frontendNode fill:#2C5282,stroke:#90CDF4,color:#EBF8FF
    classDef backendNode fill:#22543D,stroke:#9AE6B4,color:#F0FFF4
    classDef aiNode fill:#6B46C1,stroke:#D6BCFA,color:#FAF5FF
    
    class User userNode
    class WebUI,CodeEditor,ChatInterface,ProblemDisplay,ResultsViewer frontendNode
    class API,ProblemGenerator,CodeExecutor,TestRunner,GitHubFetcher,ChatbotHandler backendNode
    class AIService aiNode
    
    style Frontend fill:#1A365D,stroke:#4299E1,color:#EBF8FF
    style Backend fill:#1C4532,stroke:#68D391,color:#F0FFF4
    
    subgraph Storage
        API --> Database[(SQLite DB)]
        GitHubFetcher --> Cache[(File Cache)]
    end
    
    subgraph External
        GitHubFetcher <--> GitHub[(GitHub API)]
        AIService <--> DifyAPI[(Dify API)]
    end
    
    style Storage fill:#2D3748,stroke:#CBD5E0,color:#E2E8F0
    style External fill:#553C9A,stroke:#B794F4,color:#FAF5FF
```

The Problem Generator is a web application built with a Flask backend and vanilla JavaScript frontend. It uses SQLite for data persistence and integrates with external services for AI-powered problem generation and assistant features.

### Component Interactions

```mermaid
%%{init: {'theme': 'dark'}}%%
sequenceDiagram
    actor User
    participant UI as Frontend
    participant API as Flask Backend
    participant DB as SQLite
    participant GH as GitHub API
    participant AI as Dify AI
    
    User->>UI: Select course/lesson
    UI->>API: Request problem generation
    API->>GH: Fetch lesson content
    GH-->>API: Return lesson data
    API->>AI: Send lesson context
    AI-->>API: Return generated problem
    API->>DB: Store problem
    API-->>UI: Return problem data
    UI->>User: Display problem
    
    User->>UI: Submit solution
    UI->>API: Send code for checking
    API->>API: Execute code & validate
    API->>DB: Store solution
    API-->>UI: Return results
    UI->>User: Display results
    
    User->>UI: Open chatbot
    UI->>API: Send chat message
    API->>AI: Forward message with context
    AI-->>API: Return AI response
    API-->>UI: Return chat response
    UI->>User: Display message
```

### Key Components
- **Flask Backend**: Handles API requests, code execution, and problem generation
- **JavaScript Frontend**: Manages the UI, code editor, and user interactions
- **SQLite Database**: Stores problems, solutions, and user history
- **GitHub Integration**: Fetches lesson content from tutorial repositories
- **Dify API**: Provides AI assistant functionality
- **Style Checker**: Provides style checking and code formatting functionality

## Backend Components

### Core Modules

#### `app.py`
The main Flask application that defines routes, initializes the database, and handles requests.

**Key Functions:**
- `serve_index()`: Serves the main application HTML.
- `get_lessons()`: Fetches available lessons from GitHub.
- `generate()`: Generates programming problems using AI.
- `run_code_endpoint()`: Executes user code in various languages.
- `check_code_endpoint()`: Validates user code against test cases.
- `chatbot_endpoint()`: Handles AI assistant interactions.
- `style_check_endpoint()`: Runs style checks on user code.

#### `db.py`
Database interaction layer responsible for data persistence.

**Key Functions:**
- `init_db()`: Initializes the database schema.
- `get_db_connection()`: Creates a connection to the SQLite database.
- `store_problem()`: Saves generated problems.
- `get_problem_by_id()`: Retrieves specific problems.
- `get_problems()`: Lists all stored problems.
- `store_solution()`: Saves user solutions.

#### `github_utils.py`
Utility for fetching content from GitHub repositories.

**Key Functions:**
- `get_file_content()`: Fetches file content with caching.
- `get_lessons()`: Retrieves lesson structure for different languages.
- `build_syllabus()`: Creates a syllabus from multiple lesson files.

#### `chatbot.py`
Integrates with the Dify API for AI assistant functionality.

**Key Functions:**
- `handle_chatbot_request()`: Processes chat messages and returns AI responses.
- `prepare_context()`: Formats problem and code context for the AI.

#### `style_check.py`
Provides style checking and code formatting functionality for all supported languages.

**Key Functions:**
- `check_style()`: Main function that routes to language-specific style checkers.
- `check_python_style()`: Uses flake8 to check Python code style.
- `check_java_style()`: Uses PMD to check Java code style.
- `check_cpp_style()`: Uses clang-tidy to check C++ code style.
- `format_java_code()`: Formats Java code with custom rules for spacing and indentation.
- `format_cpp_code()`: Formats C++ code using clang-format.

### Language Support

The application supports multiple programming languages through a unified interface:

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart LR
    subgraph LanguageSelection["Language Selection"]
        Python["Python"]
        Java["Java"]
        CPP["C++"]
    end

    subgraph CodeExecution["Code Execution"]
        Runner["run_code()"]
        Runner --> PyRunner["Python Interpreter"]
        Runner --> JavaRunner["Java Compiler & JVM"]
        Runner --> CPPRunner["C++ Compiler & Executable"]
    end
    
    Python ---> |Selected| PyRunner
    Java ---> |Selected| JavaRunner
    CPP ---> |Selected| CPPRunner
    
    subgraph TestCaseValidation["Test Case Validation"]
        T1["Parse JSON Test Cases"] --> T2["Execute Code with Test Inputs"]
        T2 --> T3["Compare Outputs"]
        T3 --> T4["Return Results"]
    end
    
    PyRunner --> TestCaseValidation
    JavaRunner --> TestCaseValidation
    CPPRunner --> TestCaseValidation
    
    style LanguageSelection fill:#1A365D,stroke:#4299E1,color:#EBF8FF
    style CodeExecution fill:#1C4532,stroke:#68D391,color:#F0FFF4
    style TestCaseValidation fill:#2D3748,stroke:#CBD5E0,color:#E2E8F0
    
    style Python fill:#2C5282,stroke:#90CDF4,color:#EBF8FF
    style Java fill:#2C5282,stroke:#90CDF4,color:#EBF8FF
    style CPP fill:#2C5282,stroke:#90CDF4,color:#EBF8FF
    style Runner fill:#22543D,stroke:#9AE6B4,color:#F0FFF4
    style PyRunner fill:#22543D,stroke:#9AE6B4,color:#F0FFF4
    style JavaRunner fill:#22543D,stroke:#9AE6B4,color:#F0FFF4
    style CPPRunner fill:#22543D,stroke:#9AE6B4,color:#F0FFF4
    style T1 fill:#4A5568,stroke:#CBD5E0,color:#E2E8F0
    style T2 fill:#4A5568,stroke:#CBD5E0,color:#E2E8F0
    style T3 fill:#4A5568,stroke:#CBD5E0,color:#E2E8F0
    style T4 fill:#4A5568,stroke:#CBD5E0,color:#E2E8F0
```

The application supports multiple programming languages through a unified interface:

- **Python**: Direct execution using the Python interpreter. Style checking with flake8.
- **Java**: Compilation and execution using JDK. Style checking with PMD and custom formatting.
- **C++**: Compilation with g++ and execution of the resulting binary. Style checking with clang-tidy and formatting with clang-format.

Each language implements:
- Code execution with input/output handling
- Syntax highlighting in the editor
- Test case validation with JSON format

## Frontend Components

### Core Files

#### `index.html`
Main HTML structure of the application.

**Key Elements:**
- Course and lesson selection forms
- Code editor container
- Results display area
- Chat UI for the AI assistant
- History modal

#### `script.js`
Core JavaScript functionality for the application.

**Key Functions:**
- `generateProblem()`: Requests problem generation from the backend.
- `runCode()`: Sends code to the backend for execution.
- `checkAnswer()`: Validates user solutions against test cases.
- `loadLessons()`: Populates the lesson dropdown from the GitHub API.
- `setupEventListeners()`: Sets up all UI interaction handlers.
- `toggleTheme()`: Manages theme switching between light and dark modes.
- `openHelpModal()`: Displays the help guide with LaTeX support.
- `renderMarkdown()`: Renders markdown content with HTML.

#### `style-check.js`
JavaScript for the style checking and code formatting functionality.

**Key Functions:**
- `addStyleCheckButton()`: Adds the style check button when viewing a problem.
- `runStyleCheck()`: Sends code to the server for style checking.
- `displayStyleResults()`: Shows style errors with line highlighting.
- `formatCode()`: Requests code formatting from the server.
- `removeStyleCheckButton()`: Removes the button when returning to generate page.

#### `chatbot.js`
JavaScript for the AI assistant functionality.

**Key Functions:**
- `toggleChatWindow()`: Controls chat UI visibility.
- `handleChatSubmit()`: Processes user messages.
- `sendChatRequest()`: Communicates with the backend chatbot endpoint.
- `addBotMessage()`: Renders AI responses with markdown and LaTeX support.

### CSS Styles

#### `style-check.css`
Styles for the code style checking UI.

**Key Features:**
- `.error-highlight`: Highlights lines with style errors.
- `.error-tooltip`: Shows detailed error information on hover.
- `.style-check-container`: Contains the style check results.
- `.format-button`: Style for the code formatting button.

- `style.css`: Main styling for the application.
- `dark-mode.css`: Dark theme styling.
- `chatbot.css`: Styling for the chat interface.

### Code Editor

The application uses CodeMirror for the code editor with:
- Syntax highlighting for Python, Java, and C++
- Custom themes (darcula for dark mode, idea for light mode)
- Tab handling and indentation
- Line numbering

## Database Schema

### Entity Relationship Diagram

```mermaid
erDiagram
    PROBLEMS ||--o{ SOLUTIONS : "has many"
    
    PROBLEMS {
        integer id PK
        text title
        text problem "Markdown description"
        text testcases "JSON array"
        text course
        text lesson
        timestamp created_at
        text language "python/java/cpp"
    }
    
    SOLUTIONS {
        integer id PK
        integer problem_id FK "References PROBLEMS.id"
        text solution "Code solution"
        text language
        timestamp created_at
    }
```

### Schema Details

#### Problems Table
The `problems` table stores all generated programming challenges with their descriptions, test cases, and metadata.

```mermaid
classDiagram
    class problems {
        +INTEGER id
        +TEXT title
        +TEXT problem
        +TEXT testcases
        +TEXT course
        +TEXT lesson
        +TIMESTAMP created_at
        +TEXT language
    }
```

#### Solutions Table
The `solutions` table tracks user-submitted solutions to problems, including the programming language used.

```mermaid
classDiagram
    class solutions {
        +INTEGER id
        +INTEGER problem_id
        +TEXT solution
        +TEXT language
        +TIMESTAMP created_at
    }
```

## API Endpoints

```mermaid
classDiagram
    class ProblemGenerationAPI {
        GET /github/lessons
        POST /generate
    }
    
    class CodeExecutionAPI {
        POST /run_code
        POST /check_code
    }
    
    class ProblemManagementAPI {
        GET /problems
        GET /problems/~id~
        GET /problems/~id~/solutions
        DELETE /problems/~id~
    }
    
    class AIAssistantAPI {
        POST /chatbot
    }
    
    ProblemGenerationAPI -- CodeExecutionAPI
    ProblemGenerationAPI -- ProblemManagementAPI
    ProblemGenerationAPI -- AIAssistantAPI
```

### API Workflow

```mermaid
flowchart TD
    A[Client] --> B{"API Routes"}
    
    subgraph ProblemGeneration
        B -->|GET /github/lessons| C[Fetch Lessons]
        B -->|POST /generate| D[Generate Problem]
    end
    
    subgraph CodeExecution
        B -->|POST /run_code| E[Execute Code]
        B -->|POST /check_code| F[Validate Solution]
    end
    
    subgraph ProblemManagement
        B -->|GET /problems| G[List Problems]
        B -->|GET /problems/:id| H[Get Problem]
        B -->|GET /problems/:id/solutions| I[Get Solutions]
        B -->|DELETE /problems/:id| J[Delete Problem]
    end
    
    subgraph AIAssistant
        B -->|POST /chatbot| K[AI Chat]
    end
    
    C --> L[(Database)]
    D --> L
    E --> L
    F --> L
    G --> L
    H --> L
    I --> L
    J --> L
    K --> L
    
    style ProblemGeneration fill:#1A365D,stroke:#4299E1,stroke-width:1px
    style CodeExecution fill:#742A2A,stroke:#FC8181,stroke-width:1px
    style ProblemManagement fill:#22543D,stroke:#68D391,stroke-width:1px
    style AIAssistant fill:#744210,stroke:#F6E05E,stroke-width:1px
```

### Problem Generation
- `GET /github/lessons`: Retrieves available lessons.
- `POST /generate`: Generates a new programming problem.

### Code Execution
- `POST /run_code`: Executes user code and returns output.
- `POST /check_code`: Validates code against test cases.

### Code Style and Formatting
- `POST /check_style`: Checks code style using language-specific linters.
- `POST /format_code`: Formats code to follow language style guidelines.

### Problem Management
- `GET /problems`: Lists all saved problems.
- `GET /problems/<id>`: Retrieves a specific problem.
- `GET /problems/<id>/solutions`: Gets solutions for a problem.
- `DELETE /problems/<id>`: Deletes a problem.

### AI Assistant
- `POST /chatbot`: Sends a message to the AI assistant.

## External Integrations

### GitHub
Used to fetch lesson content and problem templates.

**Integration Points:**
- Retrieves lesson structure from index.json files
- Fetches individual lesson markdown content
- Uses caching to reduce API calls and handle rate limiting

### Dify API
Provides AI functionality for both problem generation and the assistant.

**Integration Points:**
- Problem generation with customized prompts
- AI assistant that understands code context
- Conversation history management

## Development Workflow

### Local Setup
1. Clone the repository
2. Install dependencies from requirements.txt
3. Configure environment variables in .env file
4. Run the development server with `python app.py`

### Environment Variables
- `API_KEY`: Authentication key for the AI service
- `API_URL`: Endpoint for the problem generation API
- `CHATBOT_API_URL`: Endpoint for the assistant API
- `CHATBOT_API_KEY`: Authentication key for the chatbot

## Deployment Guide

### Prerequisites
- Python 3.9+
- SQLite
- Web server (Nginx or similar)
- HTTPS certificate (Let's Encrypt recommended)

### Production Deployment
1. Set up a web server as a reverse proxy
2. Configure WSGI (Gunicorn recommended)
3. Set up HTTPS with Let's Encrypt
4. Configure proper file permissions
5. Set up a systemd service for automatic restart

### Systemd Service Example
```ini
[Unit]
Description=Problem Generator Flask Application
After=network.target

[Service]
User=username
WorkingDirectory=/path/to/problem_generator
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### Backup Strategy
- Regular SQLite database backups
- Configuration and environment variable backups
- Consider setting up periodic cache clearance for GitHub fetched content
