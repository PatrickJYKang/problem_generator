# Problem Generator

A web application that dynamically generates coding problems based on your current learning progress in Python. This tool helps you practice and reinforce your programming skills with targeted exercises.

## Features

- **Dynamic Problem Generation**: Select your current lesson and get a problem tailored to your learning progress
- **Interactive Code Editor**: Write and test your Python code directly in the browser
- **Real Terminal Environment**: Execute code in a true interactive terminal with full input/output support
- **Automatic Feedback**: Check your solutions against test cases
- **Progressive Learning**: The app builds a custom syllabus based on your current lesson, including all previous lessons
- **Intuitive Lesson Selection**: Easy-to-use dropdown menu organized by learning categories

## How It Works

1. Select your course and current lesson from the dropdown menus
2. Click "Generate Problem" to receive a problem tailored to your current knowledge
3. Write your solution in the code editor
4. Run your code to test it
5. Check your answer against the provided test cases

## Technical Details

- **Frontend**: HTML, CSS, JavaScript with CodeMirror for the code editor and xterm.js for the terminal
- **Backend**: Flask (Python) with Flask-SocketIO for real-time terminal communication
- **Problem Generation**: Uses OpenAI models in Dify to generate problems based on the syllabus
- **Terminal Implementation**: Full PTY-based terminal using Socket.IO for bidirectional communication
- **Syllabus Management**: Dynamic syllabus generation based on the user's current lesson progress

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## Deployment Notes

When deploying to a production environment, ensure proper configuration of WebSocket support:

- Use the eventlet worker with Gunicorn:
  ```bash
  gunicorn --worker-class eventlet -w 1 app:app
  ```
- Configure your web server to support WebSocket connections for the real terminal functionality

## Attribution

The syllabus and curriculum content used in this project is derived from the [Interactive Tutorials](https://github.com/ronreiter/interactive-tutorials/tree/master) project by Ron Reiter. The original content is used under the Apache License 2.0.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
