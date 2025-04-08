# Problem Generator - Architecture & Tech Stack

## System Architecture

```mermaid
%%{init: {'theme': 'dark'}}%%
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
    
    subgraph External["External Services"]
        DifyAPI["Dify AI API"] 
    end
    
    GitHubAPI --> External
    Checker --> DifyAPI
    
    %% Styling
    style Client fill:#1A365D,stroke:#4299E1,color:#EBF8FF
    style Server fill:#1C4532,stroke:#68D391,color:#F0FFF4
    style External fill:#3C366B,stroke:#B794F4,color:#FAF5FF
    
    style ProblemDisplay fill:#2C5282,stroke:#90CDF4,color:#EBF8FF
    style CodeEditor fill:#2C5282,stroke:#90CDF4,color:#EBF8FF
    style TestResults fill:#2C5282,stroke:#90CDF4,color:#EBF8FF
    style JavaScript fill:#2C5282,stroke:#90CDF4,color:#EBF8FF
    style API fill:#2C5282,stroke:#90CDF4,color:#EBF8FF
    style Chat fill:#2C5282,stroke:#90CDF4,color:#EBF8FF
    
    style AppPy fill:#22543D,stroke:#9AE6B4,color:#F0FFF4
    style GitHubUtils fill:#22543D,stroke:#9AE6B4,color:#F0FFF4
    style RunPy fill:#22543D,stroke:#9AE6B4,color:#F0FFF4
    style DbPy fill:#22543D,stroke:#9AE6B4,color:#F0FFF4
    style GitHubAPI fill:#553C9A,stroke:#B794F4,color:#FAF5FF
    style Checker fill:#22543D,stroke:#9AE6B4,color:#F0FFF4
    style DifyAPI fill:#553C9A,stroke:#B794F4,color:#FAF5FF
    
    subgraph ExternalResources["External Resources"]
        GitHubRepo["GitHub Repo\nSyllabus"]
        Dify["Dify AI\nCharacter"]
    end
    
    %% Using colors optimized for dark mode readability
    classDef clientNodes fill:#5762d5,stroke:#fff,stroke-width:1px,color:#fff;
    classDef serverNodes fill:#d5654b,stroke:#fff,stroke-width:1px,color:#fff;
    classDef externalNodes fill:#2d9d5c,stroke:#fff,stroke-width:1px,color:#fff;
    
    class ProblemDisplay,CodeEditor,TestResults,JavaScript,API,Chat clientNodes;
    class AppPy,GitHubUtils,RunPy,DbPy,GitHubAPI,Checker serverNodes;
    class GitHubRepo,DifyAPI externalNodes;
```

## Tech Stack Overview

### Frontend
- **HTML/CSS/JavaScript**: Core web technologies for UI and functionality
- **CodeMirror**: Advanced code editor with syntax highlighting for multiple languages
- **Marked.js**: For rendering markdown content in problems and help documentation
- **KaTeX**: For rendering LaTeX mathematical formulas in problem descriptions and AI responses
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
%%{init: {'theme': 'dark'}}%%
flowchart LR
    A["Select\nCourse"] --> B["Select\nLesson"]
    B --> C["Click\nGenerate"]
    C --> D["Problem\nDisplayed"]
    C --> E["API Request\nto Backend"]
    E --> F["Problem Saved\nto Database"]
    
    %% Using colors optimized for dark mode readability
    classDef userActions fill:#2C5282,stroke:#90CDF4,stroke-width:1px,color:#EBF8FF;
    classDef systemActions fill:#22543D,stroke:#9AE6B4,stroke-width:1px,color:#F0FFF4;
    
    class A,B,C,D userActions;
    class E,F systemActions;
```

### 2. Code Checking Flow

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart LR
    A["Write\nCode"] --> B["Select\nLanguage"]
    B --> C["Click Check\nAnswer"]
    C --> D["Results\nDisplayed"]
    C --> E["Code Sent\nfor Testing"]
    E --> F["Test Results\n& Solution\nSaved"]
    
    %% Using colors optimized for dark mode readability
    classDef userActions fill:#2C5282,stroke:#90CDF4,stroke-width:1px,color:#EBF8FF;
    classDef systemActions fill:#22543D,stroke:#9AE6B4,stroke-width:1px,color:#F0FFF4;
    
    class A,B,C,D userActions;
    class E,F systemActions;
```

### 3. Chat Assistant Flow

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart LR
    A["Open\nChat"] --> B["Send Message\nwith Question"]
    B --> C["Response\nGenerated"]
    B --> D["Context\nGathered"]
    D --> E["Dify API\nRequest"]
    E --> C
    
    %% Using colors optimized for dark mode readability
    classDef userActions fill:#5b6abf,stroke:#fff,stroke-width:1px,color:#fff;
    classDef systemActions fill:#458b55,stroke:#fff,stroke-width:1px,color:#fff;
    
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
