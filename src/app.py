import hmac
import hashlib
from flask import request, abort
import os
from dotenv import load_dotenv



@app.route('/webhook', methods=['POST'])
def github_webhook():
    # Get secret from environment
    secret = b"your_github_webhook_secret"
    
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

    # For now, just return a success response
    return {"message": f"Received {event} event", "payload": payload_json}, 200

load_dotenv()
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET").encode()