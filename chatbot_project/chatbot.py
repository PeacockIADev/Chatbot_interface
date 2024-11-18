from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Configure your Azure OpenAI endpoint and API key
AZURE_OPENAI_ENDPOINT = "https://YOUR_RESOURCE_NAME.openai.azure.com/openai/deployments/YOUR_MODEL_NAME/chat/completions?api-version=2023-03-15-preview"
AZURE_OPENAI_API_KEY = "YOUR_API_KEY"

# Function to interact with Azure OpenAI API
def query_openai(prompt):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(AZURE_OPENAI_ENDPOINT, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()
        # Get the chatbot's response from the API
        chatbot_response = response_json['choices'][0]['message']['content']
        return chatbot_response
    else:
        return f"Error: {response.status_code}, {response.text}"

# Define the main route for the chatbot UI
@app.route("/")
def index():
    return render_template("chat.html")

# Endpoint for the chatbot to process user input
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["prompt"]
    chatbot_response = query_openai(user_input)
    return jsonify({"response": chatbot_response})

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
