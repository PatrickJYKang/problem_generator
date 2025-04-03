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
CHATBOT_API_URL = os.getenv('DIFY_API_URL', 'http://47.251.117.165/api/chat-messages')

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
            'response_mode': 'streaming',
            'conversation_id': conversation_id
        }

        # Add problem to inputs if available
        if problem:
            payload['inputs']['problem'] = problem

        # Set up headers for the API request
        headers = {
            'Authorization': f'Bearer {CHATBOT_API_KEY}'
        }

        # Make API request to Dify
        response = requests.post(
            CHATBOT_API_URL,
            headers=headers,
            data={'request': json.dumps(payload)},
            files=files if files else None
        )

        # Clean up temporary files
        for file_path in file_paths:
            try:
                os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting temporary file {file_path}: {str(e)}")

        # Process response
        if response.status_code == 200:
            response_data = response.json()
            return jsonify(response_data)
        else:
            print(f"Dify API error: {response.status_code} - {response.text}")
            return jsonify({"error": f"Dify API returned status code {response.status_code}"}), 500

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error processing chatbot request: {str(e)}"}), 500
