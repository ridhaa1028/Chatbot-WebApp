# chat/chatapi.py

from flask import request, jsonify
from rasa.core.agent import Agent

# Import the Flask app instance created in app.py
from app import app

agent = Agent.load("path_to_your_model_directory")

# Define a route for handling incoming messages
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the user's message from the request
    user_message = request.json['message']

    # Pass the user's message to the Rasa chatbot for processing
    response = agent.handle_text(user_message)

    # Extract the chatbot's response from the Rasa response
    chatbot_response = response[0]['text']

    # Return the chatbot's response as JSON
    return jsonify({"message": chatbot_response})
