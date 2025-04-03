# Problem Generator

A web application that dynamically generates coding problems based on your current learning progress. This tool helps you practice and reinforce your programming skills with targeted exercises that match your knowledge level.

## Features

- **Multi-language Support**: Write and test code in Python, Java, and C++
- **Dynamic Problem Generation**: Select your current lesson and get a problem tailored to your learning progress
- **Interactive Code Editor**: Write and test your code directly in the browser with syntax highlighting
- **Input/Output Testing**: Provide input to your programs and see the output in real-time
- **Automatic Feedback**: Check your solutions against test cases with detailed results
- **Progressive Learning**: The app builds a custom syllabus based on your current lesson, including all previous lessons
- **Problem History**: Review and reload previously generated problems
- **Dark/Light Mode**: Toggle between themes for comfortable coding in any environment
- **Database Storage**: All problems and solutions are stored for future reference
- **Clean UI**: Focused interface that hides unnecessary elements when working on problems
- **Consistent Course Structure**: Lessons are displayed in proper pedagogical order across all languages

## How It Works

1. Select your course and current lesson from the dropdown menus
2. Click "Generate Problem" to receive a problem tailored to your current knowledge
3. Choose your preferred programming language (Python, Java, or C++)
4. Write your solution in the code editor
5. Run your code to test it with custom input
6. Check your answer against the provided test cases
7. Access your problem history to review previous exercises

## System Architecture

### Frontend
- **HTML/CSS/JavaScript**: Responsive UI with dynamic content loading and a clean grayscale design
- **CodeMirror**: Feature-rich code editor with syntax highlighting for Python, Java, and C++
- **Marked.js**: Markdown rendering for problem descriptions
- **Light/Dark Theme**: Toggle between color schemes with persistent user preference storage
- **Adaptive UI**: Interface elements that adapt based on the current context (e.g., hiding course selectors when viewing a problem)

### Backend
- **Flask**: Python web framework handling HTTP requests and serving content
- **SQLite Database**: Stores generated problems, test cases, and user solutions
- **Multi-language Execution**: Supports running code in Python, Java, and C++
- **Error Handling**: Robust handling of compilation and runtime errors
- **Dynamic Syllabus Generation**: Creates targeted problems based on learning progress
- **Input Management**: Special handling of input() prompts in Python to ensure accurate test case validation
- **Consistent Course Structure**: Custom course structures for languages without index.json files

### Database Schema
- **Problems**: Stores problem title, description, course, and lesson
- **Testcases**: Linked to problems, contains input and expected output for validation
- **Solutions**: Tracks user solution attempts, language used, and test results

## Installation and Setup

### Prerequisites
- Python 3.6+
- Java JDK 11+ (for Java execution)
- g++ with C++17 support (for C++ execution)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PatrickJYKang/problem_generator.git
   cd problem_generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Access the web interface at http://localhost:5000

## Deployment

### Local Development
For local development, run the application using Flask's built-in server:
```bash
python app.py
```
Or use the debug server for additional logging:
```bash
python debug_server.py
```

### Production Deployment

#### Using Gunicorn (Recommended)
For production environments, we recommend using Gunicorn as a WSGI server:

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Start the server:
   ```bash
   gunicorn -c gunicorn_config.py app:app
   ```

   The included `gunicorn_config.py` file contains optimized settings for production.

#### Deploying on a VPS/Dedicated Server

1. Clone the repository to your server
2. Set up a virtual environment and install dependencies
3. Configure the database path in `db.py` to a persistent location
4. Set up a systemd service for automatic startup:

   Create `/etc/systemd/system/problem-generator.service`:
   ```
   [Unit]
   Description=Problem Generator Application
   After=network.target

   [Service]
   User=your_username
   WorkingDirectory=/path/to/problem_generator
   ExecStart=/path/to/venv/bin/gunicorn -c gunicorn_config.py app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. Enable and start the service:
   ```bash
   sudo systemctl enable problem-generator
   sudo systemctl start problem-generator
   ```

6. Set up Nginx as a reverse proxy:

   ```
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

7. Obtain SSL certificates with Let's Encrypt:
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```

#### Deploying on PythonAnywhere

1. Create a PythonAnywhere account
2. Upload your code or clone from GitHub
3. Create a virtual environment and install requirements
4. Set up a web app with the following configuration:
   - Framework: Flask
   - Path to source code: `/path/to/problem_generator`
   - Working directory: `/path/to/problem_generator`
   - WSGI configuration file: Edit to point to your app

5. Configure the database path in `db.py` to a location in your user directory

#### Deploying with Docker

1. Build the Docker image:
   ```bash
   docker build -t problem-generator .
   ```

2. Run the container:
   ```bash
   docker run -d -p 8000:8000 -v data:/var/lib/problem_generator problem-generator
   ```

   This mounts a volume for persistent database storage.

## API Endpoints

- **GET /** - Serves the main application interface
- **POST /generate** - Generates a new problem based on course and lesson
- **POST /run_code** - Executes user code in the specified language
- **POST /check_code** - Validates user code against test cases
- **GET /problems** - Retrieves all stored problems or filters by course/lesson
- **GET /problems/:id** - Gets a specific problem by ID with test cases
- **GET /problems/:id/solutions** - Gets all solutions for a specific problem

## Project Structure

- **app.py**: Main Flask application with route handlers
- **db.py**: Database interaction module for storing and retrieving problems
- **run.py**: Handles code execution for different programming languages
- **check.py**: Validates code against test cases with detailed feedback
- **request.py**: Interfaces with external API for problem generation
- **static/**: Frontend assets (HTML, CSS, JavaScript)
- **syllabi/**: Curriculum content organized by course and lesson

## Customization

The application can be customized in several ways:

1. **Add New Languages**: Extend `run.py` and `check.py` with additional language support
2. **Custom Courses**: Add new curriculum content to the syllabi directory
3. **UI Customization**: Modify the CSS variables in `style.css` and `dark-mode.css`
4. **Database Location**: Configure the database path in `db.py`

## Attribution

The syllabus and curriculum content used in this project is derived from the [Interactive Tutorials](https://github.com/ronreiter/interactive-tutorials/tree/master) project by Ron Reiter. The original content is used under the Apache License 2.0.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
