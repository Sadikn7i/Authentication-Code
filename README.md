This project provides a simple yet complete demonstration of how to secure an API endpoint using a Hash-based Message Authentication Code (HMAC) signature. It includes a Python client that generates a signature and sends a request, and a Flask server that validates the signature.

This is a common technique used to ensure that API requests are both authentic (they come from a known source) and have integrity (they were not tampered with in transit).

Features
Secure Authentication: Implements HMAC with SHA-256 to create a secure signature.

Client & Server Included: Provides both a client.py to send requests and a test_server.py to validate them.

Best Practices: Uses environment variables to handle the secret key, preventing it from being hardcoded and exposed in the source code.

Pure Python: Built with standard Python libraries (hmac, hashlib) and two common packages (requests, Flask).

How to Use
1. Prerequisites
Make sure you have Python installed. Then, install the necessary libraries:

Bash

pip install requests flask

2. Set Environment Variables
This project requires two environment variables to be set before running. Open your terminal and set the following:

Bash

# For Windows Command Prompt
set MY_SECRET_KEY="your-chosen-secret-key"

set API_ENDPOINT="///////////////////"

# For macOS/Linux or Git Bash
export MY_SECRET_KEY="your-chosen-secret-key"

export API_ENDPOINT="///////////"
(Replace "your-chosen-secret-key" with any secret phrase you like.)

3. Run the Server
In your first terminal window, start the Flask server. It will begin listening for requests.

Bash

python test_server.py

4. Run the Client
Open a second terminal window and set the same environment variables from Step 2. Then, run the client script to send the authenticated request to the server.

Bash

python client.py
Expected Outcome
The client terminal will show a Status Code: 200 and a success message.

The server terminal will print the details of the incoming request and confirm that the signature is ✅ SIGNATURE VALID.
