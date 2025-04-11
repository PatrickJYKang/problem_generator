# Dify Workflows Documentation

This document provides a detailed explanation of the Dify API workflows used in the Problem Generator application. Since these workflows are not open-source, this documentation serves as a reference for understanding how the backend AI processes work.

## Table of Contents
- [Problem Generator Workflow](#problem-generator-workflow)
- [Chat Assistant Workflow](#chat-assistant-workflow)

## Problem Generator Workflow

The Problem Generator workflow takes syllabus content and generates customized programming problems with test cases.

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart LR
    Start([Start]) --> Syllabi
    
    Syllabi["Syllabi Extractor"] --> Generate
    Generate["Problem Generator"] --> Testcases
    Testcases["Test Cases"] --> Code
    Code["Solution Generator"] --> End([End])
    
    classDef default fill:#1A365D,stroke:#4299E1,color:#EBF8FF
    classDef startend fill:#744210,stroke:#F6E05E,color:#FFFFF0
    
    class Start,End startend
    class Syllabi,Generate,Testcases,Code default
```

### Workflow Steps

#### 1. Start
The workflow begins when a user requests a new problem through the application interface, specifying a course and lesson.

##### Inputs:
- **Course**: The selected course (Plaintext)
- **CurrentLesson**: The selected lesson (Plaintext)
- **Syllabus**: The provided syllabus content (Markdown)
- **Language**: The selected programming language (Plaintext)

#### 2. Syllabi Extractor
**Process**: Parses the syllabus content to a format readable by the LLM.

#### 3. Generate
**Process**: Generates a programming problem based on the syllabus content.

**Prompt Description**: The prompt provides the syllabus content to the LLM (GPT-4o) along with instructions to (bolded instructions should be emphasised to the LLM):
- Be sure not to involve any concepts outside of what the user has learnt
- **Delimit test cases properly with whitespace**
- **Avoid generating test cases with inputs literally in list, dictionary, or similar format (e.g. `['input1', 'input2']`)**
- Limit the problem to be solvable in a reasonable number of lines
- Not give away the solution or give any sample code
- Be clear what language should be used
- Only output the problem statement and sample test cases and nothing more
- **When inserting LaTeX, to only use the `$$%Your LaTeX here%$$` delimiter, and never the `\[\]` or `\(\)` delimiters**.

#### 4. Testcases
**Process**: Creates test cases to validate user solutions using the GPT-4o model.

**Prompt Description**: Using the generated problem as context, this prompt asks the LLM to:
- Output the test cases in a JSON array as follows
```json
[
  {
    "input": "5",
    "output": "25"
  },
  {
    "input": "10",
    "output": "100"
  }
]
```
- Only output one test case if the problem is a single input problem or does not require input
- Only output the raw JSON array, no additional text

#### 5. Title
**Process**: Generates a title for the problem using the GPT-4-turbo model.

**Prompt Description**: This prompt instructs the LLM to, for the given problem, generate a concise title for it, and output it without any quotes or explanatory text.

#### 6. End
The complete problem package (problem statement, test cases, and title) is returned to the application and presented to the user.

##### Outputs:
- **Problem**: The generated programming problem (Markdown)
- **Testcases**: The generated test cases (JSON)
- **Title**: The generated problem title (Plaintext)

## Chat Assistant Workflow

The Chat Assistant workflow provides conversational help related to programming problems and code.

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart LR
    Start([Start]) --> Syllabus
    
    Syllabus["Syllabus Extractor"] --> Problem
    Problem["Problem Extractor"] --> Code
    Code["Code Extractor"] --> Answer1
    
    Answer1["Answer Generator"] --> Answer2([Answer])
    
    classDef default fill:#1A365D,stroke:#4299E1,color:#EBF8FF
    classDef startend fill:#744210,stroke:#F6E05E,color:#FFFFF0
    classDef answer fill:#742A2A,stroke:#FC8181,color:#FFF5F5
    
    class Start startend
    class Syllabus,Problem,Code default
    class Answer1 answer
    class Answer2 startend
```

### Workflow Steps

#### 1. Start
The workflow begins when a user sends a message to the chat assistant, asking for help with their programming problem.

##### Inputs:
- **Syllabus**: The provided syllabus content (Markdown)
- **Course**: The selected course (Plaintext)
- **Lesson**: The selected lesson (Plaintext)
- **Problem**: The user's current problem (Markdown)
- **Code**: The user's current code (Plaintext)
- **Query**: The user's query (Plaintext)
- Parameters such as conversation ID are automatically populated and passed

#### 2. Syllabi Extractor
**Process**: Parses the syllabus content to a format readable by the LLM.

#### 3. Problem Extractor
**Process**: Parses the problem content to a format readable by the LLM.

#### 4. Code Extractor
**Process**: Parses the code content to a format readable by the LLM.

#### 5. Answer Generator
**Process**: Generates a helpful response based on all the contextual information.

**Prompt Description**: This prompt sends all the collected context (syllabus, problem, code, conversation history) to the LLM (GPT-4o) with instructions to (bolded instructions should be emphasised to the LLM):
- Help the user to the best of their ability
- Not go beyond the user's current knowledge
- Not write code or solutions
- **When inserting LaTeX, to only use the `$$%Your LaTeX here%$$` delimiter, and never the `\[\]` or `\(\)` delimiters**.

#### 6. Answer
The assistant's response is returned to the application and displayed to the user in the chat interface.

##### Output:
- **Answer**: The assistant's response (Markdown)

## Implementation Notes

- Both workflows use the Dify API as a management layer for interactions with underlying language models
- The primary model used is GPT-4 (gpt-4-1106) for its reasoning capabilities and code generation quality
- Workflows include context management to maintain coherence across interactions
- Responses are structured for proper markdown rendering in the application interface
- Error handling is implemented at each step to gracefully handle API failures or unexpected outputs

---

*Note: This documentation describes the Dify workflows as implemented in Problem Generator version 0.2.1. Future versions may include workflow enhancements or additional features. Updates to the Dify workflows are scheduled separate to the main application updates, so a major change may not be reflected in a major release or in the [Changelog](./CHANGELOG.md).*
