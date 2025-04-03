"""
Chatbot functionality for the Problem Generator application.
This module handles the Dify API integration for the AI assistant.
"""

import os
import json
import requests
import tempfile
from flask import jsonify, request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get chatbot API key from environment variables
CHATBOT_API_KEY = os.getenv('CHATBOT_API_KEY', 'app-rDDSJ8nmFBq2bDxQ2j4oFQsw')

# The app ID for the chatbot
APP_ID = 'd91beb8e-72c6-4aec-be40-6165f64d9222'

# Get the API URL from environment variables
# Using the proper API endpoint from .env
CHATBOT_API_URL = os.getenv('CHATBOT_API_URL', 'http://47.251.117.165/v1/chat-messages')

# Debug logging for API requests
import logging
logging.basicConfig(level=logging.INFO)

def upload_file(file_path, filename=None, user="end_user"):
    """ Uploads a file to the API and returns the file ID """
    # Use the API URL from environment variable, extracting the base URL
    base_api_url = "http://47.251.117.165/v1"
    upload_url = f"{base_api_url}/files/upload"
    logging.info(f"Using file upload URL: {upload_url}")
    headers = {"Authorization": f"Bearer {CHATBOT_API_KEY}"}
    
    try:
        logging.info(f"Uploading file: {file_path}")
        if not os.path.exists(file_path):
            logging.error(f"Error: File not found: {file_path}")
            return None
        
        # Determine the MIME type based on filename extension
        mime_type = "text/plain"  # Default
        if filename and filename.lower().endswith('.md'):
            mime_type = "text/markdown"
        elif filename and filename.lower().endswith('.py'):
            mime_type = "text/x-python"
        elif filename and filename.lower().endswith('.java'):
            mime_type = "text/x-java"
        elif filename and filename.lower().endswith('.cpp'):
            mime_type = "text/x-c++src"
            
        # Use provided filename or default to basename of the file
        display_name = filename if filename else os.path.basename(file_path)
        
        # Prepare the multipart/form-data request exactly as specified in the API docs
        with open(file_path, 'rb') as file:
            # Important: this matches the API docs exactly - 'file' as the field name (not 'files')
            files = {'file': (display_name, file, mime_type)}
            # The user identifier is required by the API
            data = {"user": user}
            
            logging.info(f"Making file upload API request to: {upload_url}")
            logging.info(f"File: {display_name}, MIME type: {mime_type}")
            
            # Make the multipart/form-data request
            response = requests.post(upload_url, headers=headers, files=files, data=data)
            
            logging.info(f"File upload response status: {response.status_code}")
            if response.status_code == 201:
                # Parse the response to get the file ID
                response_data = response.json()
                file_id = response_data.get("id")
                logging.info(f"File uploaded successfully, ID: {file_id}")
                return file_id
            else:
                logging.error(f"File upload failed: {response.text}")
                return None
    except Exception as e:
        logging.error(f"Error during file upload: {str(e)}")
        return None

def handle_chatbot_request():
    """ Handle chatbot requests through Dify API """
    try:
        data = request.get_json()
        user_query = data.get('query', '')
        problem = data.get('problem', '')
        course = data.get('course', '')
        lesson = data.get('lesson', '')
        code = data.get('code', '')
        syllabus = data.get('syllabus', '')
        conversation_id = data.get('conversation_id', None)

        # Initialize temporary file cleanup list
        file_paths = []

        # Prepare the payload for Dify API with CAPITALIZED input keys
        payload = {
            'inputs': {
                'Course': course,  # Capitalized as required
                'Lesson': lesson,  # Capitalized as required
            },
            'query': user_query,
            'user': 'end_user',  # Required parameter per API error
            'response_mode': 'blocking',  # Use blocking instead of streaming for simplicity
            'conversation_id': conversation_id,
        }
        
        # Create a list to store file paths for cleanup later
        file_paths = []

        # Handle code upload if code is provided
        if code:
            # Create temporary file for code
            temp_code = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
            temp_code.write(code.encode('utf-8'))
            temp_code.close()
            file_paths.append(temp_code.name)
            
            # Upload the code file using proper multipart/form-data request
            code_file_id = upload_file(temp_code.name, "code.txt", "end_user")
            if code_file_id:
                # Format Code (capitalized) properly as an object with transfer_method
                payload['inputs']['Code'] = {
                    'transfer_method': 'local_file',
                    'upload_file_id': code_file_id,
                    'type': 'document'
                }
                logging.info(f"Code file uploaded with ID: {code_file_id}")
            else:
                logging.error("Failed to upload code file")
            
        # Handle syllabus upload if provided
        if syllabus:
            # Create a temporary file for syllabus
            temp_syllabus = tempfile.NamedTemporaryFile(suffix='.md', delete=False)
            temp_syllabus.write(syllabus.encode('utf-8'))
            temp_syllabus.close()
            file_paths.append(temp_syllabus.name)
            
            # Upload the syllabus file using proper multipart/form-data request
            syllabus_file_id = upload_file(temp_syllabus.name, "syllabus.md", "end_user")
            if syllabus_file_id:
                # Format Syllabus (capitalized) properly as an object with transfer_method
                payload['inputs']['Syllabus'] = {
                    'transfer_method': 'local_file',
                    'upload_file_id': syllabus_file_id,
                    'type': 'document'
                }
                logging.info(f"Syllabus file uploaded with ID: {syllabus_file_id}")
            else:
                logging.error("Failed to upload syllabus file")

        # Handle problem file upload if provided
        if problem:
            # Create a temporary file for the problem
            temp_problem = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
            temp_problem.write(problem.encode('utf-8'))
            temp_problem.close()
            file_paths.append(temp_problem.name)
            
            # Upload the problem file
            problem_file_id = upload_file(temp_problem.name, "problem.txt", "end_user")
            if problem_file_id:
                # Format Problem (capitalized) properly with the correct transfer_method
                payload['inputs']['Problem'] = {
                    'transfer_method': 'local_file',
                    'upload_file_id': problem_file_id,
                    'type': 'document'
                }
                logging.info(f"Problem file uploaded with ID: {problem_file_id}")
            else:
                # Fallback to plaintext if file upload fails
                logging.warning("Failed to upload problem file, using plaintext instead")
                payload['inputs']['Problem'] = problem

        # Set up headers for the API request
        # Make sure we're using the correct authorization format
        headers = {
            'Authorization': f'Bearer {CHATBOT_API_KEY}',
            'Content-Type': 'application/json'
        }

        # Make API request to Dify
        # The correct format for Dify API
        logging.info(f"Sending request to: {CHATBOT_API_URL}")
        logging.info(f"Headers: {headers}")
        logging.info(f"Payload: {json.dumps(payload)[:500]}..." if len(json.dumps(payload)) > 500 else f"Payload: {json.dumps(payload)}")
        
        try:
            # Construct the correct URL with app_id as a query parameter
            api_url = f"{CHATBOT_API_URL}?app_id={APP_ID}"
            logging.info(f"Using API URL: {api_url}")
            
            # Ensure conversation_id is properly formatted (should be None or a valid string, not empty string)
            if 'conversation_id' in payload and not payload['conversation_id']:
                del payload['conversation_id']
            
            # Log complete request data for debugging
            logging.info(f"Complete request: URL={api_url}, Headers={headers}, Payload={json.dumps(payload, default=str)[:200]}...")
            
            # For simplicity, always use JSON - ensure code is included
            # Syllabus should already be properly formatted above - do not add it as plain text here
            if code and 'code' not in payload['inputs']:
                payload['inputs']['code'] = code
            
            # Send the request with JSON content
            response = requests.post(
                api_url,
                headers=headers,
                json=payload
            )
            
            logging.info(f"Request sent with Content-Type: {headers.get('Content-Type')}")
        except Exception as req_error:
            logging.error(f"Request error: {str(req_error)}")
            raise

        # Clean up temporary files
        for file_path in file_paths:
            try:
                os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting temporary file {file_path}: {str(e)}")

        # Process response
        logging.info(f"Dify API response status: {response.status_code}")
        
        # Log the response content for debugging
        try:
            response_text = response.text
            logging.info(f"Response content (first 500 chars): {response_text[:500]}..." if len(response_text) > 500 else f"Response content: {response_text}")
        except Exception as log_error:
            logging.error(f"Error logging response: {str(log_error)}")
        
        # Print full details of the request for debugging
        logging.info(f"Full request details:")
        logging.info(f"URL: {api_url}")
        logging.info(f"Headers: {headers}")
        logging.info(f"Payload size: {len(json.dumps(payload))} bytes")
        logging.info(f"Payload keys: {payload.keys()}")
        if 'inputs' in payload:
            logging.info(f"Input keys: {payload['inputs'].keys()}")
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                logging.info(f"Successfully parsed JSON response with keys: {list(response_data.keys())}")
                return jsonify(response_data)
            except Exception as e:
                logging.error(f"Error parsing JSON response: {str(e)}")
                return jsonify({"error": "Failed to parse API response", "answer": "Sorry, there was an error communicating with the AI assistant. Please try again later."}), 500
        else:
            logging.error(f"Dify API error: {response.status_code} - {response.text}")
            # Return a more specific error message if possible
            error_message = "Sorry, there was an error communicating with the AI assistant. Please try again later."
            try:
                error_data = response.json()
                if 'message' in error_data:
                    logging.error(f"API error message: {error_data['message']}")
                    error_message = f"API error: {error_data['message']}"
                elif 'detail' in error_data:
                    logging.error(f"API error detail: {error_data['detail']}")
                    error_message = f"API error: {error_data['detail']}"
                elif 'error' in error_data:
                    logging.error(f"API error description: {error_data['error']}")
                    error_message = f"API error: {error_data['error']}"
            except Exception as e:
                logging.error(f"Error parsing error response: {str(e)}")
            
            return jsonify({"error": f"API error", "answer": error_message}), 200  # Return 200 to client with error message

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error processing chatbot request: {str(e)}"}), 500
