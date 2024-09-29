import os
import time

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Define the forwarding target IP and port (change this to your desired IP)
FORWARD_URL = "http://localhost:11434/v1/chat/completions"


@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    # Capture the incoming JSON request data
    incoming_data = request.get_json()
    incoming_data["model"] = "phi3"
    # Forward the data to the specified server
    try:
        print(incoming_data)
        forward_response = requests.post(FORWARD_URL, json=incoming_data, headers={"Content-Type": "application/json"})
        # Get the response from the forwarded server
        forward_response_content = forward_response.json()

        # Return the response back to the client with the status code from the target server
        print("full response")
        print(forward_response_content)
        print("response code")
        print(forward_response.status_code)
        return jsonify(forward_response_content), forward_response.status_code
    except requests.exceptions.RequestException as e:
        # Handle the case where the forwarding fails
        return jsonify({"error": "Failed to forward the request", "details": str(e)}), 500


if __name__ == "__main__":
    # Run the server on port 11435 to match the incoming curl request
    os.system("ollama serve &")
    time.sleep(1)
    print(os.system('curl http://localhost:11434/api/pull -d \'{"name": "phi3"}\''))
    app.run(host="0.0.0.0", port=11435)
