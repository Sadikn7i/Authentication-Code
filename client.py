import requests
import hmac
import hashlib
import base64
import json
import os
from datetime import datetime, timezone

def create_hmac_signature(secret_key: str, http_method: str, request_uri: str, timestamp: str, request_body: str) -> str:
    """Generates a Base64-encoded HMAC-SHA256 signature."""
    string_to_sign = f"{http_method}\n{request_uri}\n{timestamp}\n{request_body}"
    secret_key_bytes = secret_key.encode('utf-8')
    string_to_sign_bytes = string_to_sign.encode('utf-8')
    signature_hash = hmac.new(secret_key_bytes, string_to_sign_bytes, hashlib.sha256)
    binary_signature = signature_hash.digest()
    base64_signature = base64.b64encode(binary_signature)
    return base64_signature.decode('utf-8')

# --- Main execution part ---
if __name__ == "__main__":
    # --- 1. Get configuration from environment variables ---
    
    # Get the API endpoint from an environment variable
    API_ENDPOINT = os.environ.get('API_ENDPOINT')
    
    # Get the secret key from an environment variable
    SECRET_KEY = os.environ.get('MY_SECRET_KEY')
    
    # Check if the environment variables were found
    if not API_ENDPOINT:
        raise ValueError("Error: The API_ENDPOINT environment variable is not set.")
    if not SECRET_KEY:
        raise ValueError("Error: The MY_SECRET_KEY environment variable is not set.")

    # --- 2. Define the request payload ---
    HTTP_METHOD = "POST"
    # The request URI is derived from the full endpoint URL
    REQUEST_URI = "/" + "/".join(API_ENDPOINT.split('/')[3:])
    
    payload = {
        "amount": 5000, 
        "currency": "JPY"
    }
    request_body_str = json.dumps(payload, separators=(',', ':'))
    
    # --- 3. Generate a current timestamp in UTC ---
    timestamp_str = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # --- 4. Create the signature ---
    signature = create_hmac_signature(
        secret_key=SECRET_KEY,
        http_method=HTTP_METHOD,
        request_uri=REQUEST_URI,
        timestamp=timestamp_str,
        request_body=request_body_str
    )
    
    # --- 5. Construct headers and send the request ---
    headers = {
        'Content-Type': 'application/json',
        'ME-NOWAY-SIGNATURE': signature,
        'X-Timestamp': timestamp_str 
    }
    
    print(f"🚀 Sending request to {API_ENDPOINT}...")
    try:
        response = requests.post(
            url=API_ENDPOINT,
            headers=headers,
            data=request_body_str
        )
        
        # --- 6. Print the server's response ---
        print(f"\nStatus Code: {response.status_code}")
        try:
            print("Response JSON:", response.json())
        except json.JSONDecodeError:
            print("Response Text:", response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
