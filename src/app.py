from flask import Flask, request, abort, jsonify
import hmac
import hashlib
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

app = Flask(__name__)

# Use relative import
from .routes import routes
app.register_blueprint(routes)

@app.route('/webhook', methods=['POST'])
def github_webhook():
    # Get secret from environment
    secret = os.getenv("GITHUB_WEBHOOK_SECRET").encode()
    
    # Verify payload signature
    signature = request.headers.get('X-Hub-Signature-256')
    if signature is None:
        abort(400, 'Missing signature')

    # Compute the expected signature
    payload = request.data
    expected_signature = 'sha256=' + hmac.new(secret, payload, hashlib.sha256).hexdigest()

    # Compare signatures
    if not hmac.compare_digest(signature, expected_signature):
        abort(403, 'Invalid signature')

    # Process webhook payload
    event = request.headers.get('X-GitHub-Event')
    payload_json = request.json

    # Placeholder for event processing
    process_github_event(event, payload_json)

    return {"message": f"Received {event} event", "payload": payload_json}, 200

def process_github_event(event, payload):
    """
    Process different GitHub webhook events
    """
    if event == 'push':
        # Handle push event
        print(f"Push event received: {payload}")
    elif event == 'pull_request':
        # Handle pull request event
        print(f"Pull request event received: {payload}")
    # Add more event handlers

if __name__ == '__main__':
    app.run(debug=True)