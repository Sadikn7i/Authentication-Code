From flask import Flask, request, jsonify
import hmac
import hashlib
import base64
import os  # <-- ADDED: Import the 'os' library

# --- Server Configuration ---
app = Flask(__name__)

# --- MODIFIED: Securely get the secret key from an environment variable ---
SECRET_KEY = os.environ.get('MY_SECRET_KEY')

# Check if the environment variable was found. If not, exit with an error.
if not SECRET_KEY:
    raise ValueError("Error: MY_SECRET_KEY environment variable is not set.")
# --- END OF MODIFICATION ---


@app.route('/api/v1/payment', methods=['POST'])
def validate_payment_request():
    """This endpoint mimics the real server, validating the MAC signature."""
    
    # --- 1. Get data from the incoming request ---
    received_signature = request.headers.get('ME-NOWAY-SIGNATURE')
    timestamp = request.headers.get('X-Timestamp')
    
    # The raw request body in bytes, then decoded to a string
    request_body_str = request.data.decode('utf-8')
    
    print("--- Received Request ---")
    print(f"Timestamp Header: {timestamp}")
    print(f"Signature Header: {received_signature}")
    print(f"Request Body: {request_body_str}")
    
    # Check if headers are present
    if not received_signature or not timestamp:
        return jsonify({"error": "Missing required signature headers"}), 400

    # --- 2. Re-create the signature on the server side ---
    # The server must construct the *exact* same string the client did.
    string_to_sign = f"{request.method}\n{request.path}\n{timestamp}\n{request_body_str}"
    
    print(f"\nRe-created String to Sign on Server:\n---\n{string_to_sign}\n---")
    
    # Calculate what the signature should be
    secret_key_bytes = SECRET_KEY.encode('utf-8')
    string_to_sign_bytes = string_to_sign.encode('utf-8')
    
    expected_hash = hmac.new(secret_key_bytes, string_to_sign_bytes, hashlib.sha256)
    expected_signature = base64.b64encode(expected_hash.digest()).decode('utf-8')
    
    print(f"Server-Calculated Signature: {expected_signature}")

    # --- 3. Compare the signatures securely ---
    # Use hmac.compare_digest() to prevent timing attacks.
    is_valid = hmac.compare_digest(expected_signature, received_signature)
    
    if is_valid:
        print("\n SIGNATURE VALID\n")
        return jsonify({"message": "Success! Signature is valid."}), 200
    else:
        print("\n SIGNATURE INVALID\n")
        return jsonify({"message": "Forbidden. Invalid signature."}), 403

if __name__ == '__main__':
    # Runs the server on http://127.0.0.1:5000
    app.run(port=5000, debug=True)
