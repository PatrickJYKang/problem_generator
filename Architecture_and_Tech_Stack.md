# Problem Generator - Architecture & Tech Stack

## System Architecture

```mermaid
flowchart TB
    subgraph Client["Client (Web Browser)"]
        ProblemDisplay["Problem Display\nHTML/CSS"] 
        CodeEditor["Code Editor\nCodeMirror"] 
        TestResults["Test Results\nHTML/CSS"]
        JavaScript["JavaScript\nscript.js"]
        API["Problem Generator\nREST API"]
        Chat["AI Assistant Chat\nchatbot.js"]
        
        ProblemDisplay --> JavaScript
        CodeEditor --> JavaScript
        TestResults --> JavaScript
        JavaScript --> API
        JavaScript --> Chat
    end
    
    API --> Server
    Chat --> Server
    
    subgraph Server["Server (Flask)"]
        AppPy["app.py\nMain Server"]
        GitHubUtils["github_utils.py\nGitHub Fetcher"]
        RunPy["run.py\nCode Runner"]
        DbPy["db.py\nSQLite"]
        GitHubAPI["GitHub API\nFetch Syllabus"]
        Checker["Problem Checker\ncheck.py"]
        
        AppPy --> GitHubUtils
        AppPy --> RunPy
        AppPy --> DbPy
        GitHubUtils --> GitHubAPI
        RunPy --> Checker
    end
    
    GitHubAPI --> External
    Checker --> DifyAPI
    
    subgraph External["External Resources"]
        GitHubRepo["GitHub Repo\nSyllabus"]
        DifyAPI["Dify API\nChat AI"]
    end
    
    classDef clientNodes fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef serverNodes fill:#e6f3ff,stroke:#333,stroke-width:1px;
    classDef externalNodes fill:#f0fff0,stroke:#333,stroke-width:1px;
    
    class ProblemDisplay,CodeEditor,TestResults,JavaScript,API,Chat clientNodes;
    class AppPy,GitHubUtils,RunPy,DbPy,GitHubAPI,Checker serverNodes;
    class GitHubRepo,DifyAPI externalNodes;
```

## Tech Stack Overview

### Frontend
- **HTML/CSS/JavaScript**: Core web technologies for UI and functionality
- **CodeMirror**: Advanced code editor with syntax highlighting for multiple languages
- **Markdown-it**: For rendering problem descriptions in markdown format
- **Fetch API**: For making AJAX requests to the backend

### Backend
- **Flask**: Python web framework for serving the application
- **SQLite**: Lightweight database for storing problems and solutions
- **GitHub API**: For fetching syllabus content and lessons

### Code Execution
- **Python Interpreter**: For running Python code submissions
- **Java Compiler & JVM**: For compiling and running Java code
- **G++ Compiler**: For compiling and running C++ code

### AI Assistant
- **Dify API**: AI platform for the embedded chatbot assistant

## Key User Flows

### 1. Problem Generation Flow

```mermaid
flowchart LR
    A["Select\nCourse"] --> B["Select\nLesson"]
    B --> C["Click\nGenerate"]
    C --> D["Problem\nDisplayed"]
    C --> E["API Request\nto Backend"]
    E --> F["Problem Saved\nto Database"]
    
    classDef userActions fill:#f5f5ff,stroke:#333,stroke-width:1px;
    classDef systemActions fill:#f0f8ff,stroke:#333,stroke-width:1px;
    
    class A,B,C,D userActions;
    class E,F systemActions;
```

### 2. Code Checking Flow

```mermaid
flowchart LR
    A["Write\nCode"] --> B["Select\nLanguage"]
    B --> C["Click Check\nAnswer"]
    C --> D["Results\nDisplayed"]
    C --> E["Code Sent\nfor Testing"]
    E --> F["Test Results\n& Solution\nSaved"]
    
    classDef userActions fill:#f5f5ff,stroke:#333,stroke-width:1px;
    classDef systemActions fill:#f0f8ff,stroke:#333,stroke-width:1px;
    
    class A,B,C,D userActions;
    class E,F systemActions;
```

### 3. Chat Assistant Flow

```mermaid
flowchart LR
    A["Open\nChat"] --> B["Send Message\nwith Question"]
    B --> C["Response\nGenerated"]
    B --> D["Context\nGathered"]
    D --> E["Dify API\nRequest"]
    E --> C
    
    classDef userActions fill:#f5f5ff,stroke:#333,stroke-width:1px;
    classDef systemActions fill:#f0f8ff,stroke:#333,stroke-width:1px;
    
    class A,B,C userActions;
    class D,E systemActions;
```

## Database Schema

```mermaid
erDiagram
    problems ||--o{ testcases : has
    problems ||--o{ solutions : has
    
    problems {
        int id PK
        string title
        text problem_text
        string course
        string lesson
        datetime created_at
    }
    
    testcases {
        int id PK
        int problem_id FK
        text input
        text expected_output
    }
    
    solutions {
        int id PK
        int problem_id FK
        string language
        text code
        int passed_testcases
        int total_testcases
        datetime submitted_at
    }
```

## Programming Languages Support

The application supports multiple programming languages:

1. **Python**
   - File type: `.py`
   - Execution: Direct interpreter execution
   - Libraries: Standard Python libraries

2. **Java**
   - File type: `.java`
   - Execution: Compilation with `javac` and execution with `java`
   - Entry point: Main class with main method

3. **C++**
   - File type: `.cpp`
   - Execution: Compilation with `g++` and execution of binary
   - Standard: C++17

## Environment Configuration

The application uses:
- Environment variables for API keys and configuration
- Local SQLite database for persistent storage
- Browser localStorage for user preferences (theme, etc.)

## Dark/Light Theme Support

The application implements theme switching with:
- CSS variables for theming
- CodeMirror themes that match the overall UI
- Local storage to remember user theme preferences

## GitHub Integration

The application fetches learning materials from GitHub, specifically:
- Lesson indices for navigation
- Syllabus content in Markdown format
- Organized by programming language and difficulty level

---

*Created: April 4, 2025*
