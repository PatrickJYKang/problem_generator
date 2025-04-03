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

# Get Dify API key from environment variables
CHATBOT_API_KEY = os.getenv('DIFY_API_KEY', 'app-rDDSJ8nmFBq2bDxQ2j4oFQsw')

# The app ID for the Dify chatbot
APP_ID = 'd91beb8e-72c6-4aec-be40-6165f64d9222'

# The correct API URL for Dify
# Direct API endpoint based on the documentation at http://47.251.117.165/app/d91beb8e-72c6-4aec-be40-6165f64d9222/develop
CHATBOT_API_URL = f"http://47.251.117.165/v1/chat-messages"

# Debug logging for API requests
import logging
logging.basicConfig(level=logging.INFO)

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

        # Create temporary files for documents
        files = []
        file_paths = []

        # Create temporary file for code if provided
        if code:
            temp_code = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
            temp_code.write(code.encode('utf-8'))
            temp_code.close()
            file_paths.append(temp_code.name)
            files.append(
                ('files', ('code.txt', open(temp_code.name, 'rb'), 'text/plain'))
            )

        # Create temporary file for syllabus if provided
        if syllabus:
            temp_syllabus = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
            temp_syllabus.write(syllabus.encode('utf-8'))
            temp_syllabus.close()
            file_paths.append(temp_syllabus.name)
            files.append(
                ('files', ('syllabus.txt', open(temp_syllabus.name, 'rb'), 'text/plain'))
            )

        # Prepare the payload for Dify API
        payload = {
            'inputs': {
                'course': course,
                'lesson': lesson,
            },
            'query': user_query,
            'user': 'end_user',  # Required parameter per API error
            'response_mode': 'blocking',  # Use blocking instead of streaming for simplicity
            'conversation_id': conversation_id,
            'app_id': APP_ID  # Include app_id in payload
        }
        
        # Add code and syllabus to inputs if available
        if code:
            payload['inputs']['code'] = code
            
        if syllabus:
            payload['inputs']['syllabus'] = syllabus

        # Add problem to inputs if available
        if problem:
            payload['inputs']['problem'] = problem

        # Set up headers for the API request
        headers = {
            'Authorization': f'Bearer {CHATBOT_API_KEY}'
        }

        # Make API request to Dify
        # The correct format for Dify API
        logging.info(f"Sending request to: {CHATBOT_API_URL}")
        logging.info(f"Headers: {headers}")
        logging.info(f"Payload: {json.dumps(payload)[:500]}..." if len(json.dumps(payload)) > 500 else f"Payload: {json.dumps(payload)}")
        
        try:
            if files:
                # When sending files, we need to use multipart/form-data
                multipart_data = {
                    'query': (None, user_query),
                    'user': (None, 'end_user'),  # Required parameter per API error
                    'response_mode': (None, 'blocking'),  # Use blocking instead of streaming for simplicity
                    'app_id': (None, APP_ID)  # Include app_id in form data
                }
                
                # Add inputs as separate fields
                for key, value in payload.get('inputs', {}).items():
                    multipart_data[f'inputs[{key}]'] = (None, value)
                
                # Add conversation_id if present
                if conversation_id:
                    multipart_data['conversation_id'] = (None, conversation_id)
                
                # Add the files
                multipart_data.update(files)
                
                response = requests.post(
                    CHATBOT_API_URL,
                    headers=headers,
                    files=multipart_data
                )
            else:
                # When not sending files, we can send JSON directly
                response = requests.post(
                    CHATBOT_API_URL,
                    headers=headers,
                    json=payload
                )
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
            except:
                pass
            
            return jsonify({"error": f"API error", "answer": error_message}), 200  # Return 200 to client with error message

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error processing chatbot request: {str(e)}"}), 500
