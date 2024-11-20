import os
import config
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, disconnect
import jwt
from datetime import datetime, timedelta


app = Flask(__name__)
socketio = SocketIO(app)


# Secret key for JWT encoding and decoding (in a real app, store this securely)
app.config = config.Config


# A simple function to verify the JWT token
def verify_token(token):
    try:
        # Decode the JWT token and check for validity
        decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        return decoded

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None


# Event handler for client connections
@socketio.on("connect")
def on_connect():
    # Get the token from the query parameters or the headers (you can customize this)
    token = request.args.get("token")  # or request.headers.get('Authorization')
    if token:
        # Verify the token
        user_data = verify_token(token)
        if user_data:
            print(f"Client connected with user data: {user_data}")
            return True  # Allow the connection to continue
        else:
            print("Invalid or expired token.")
            disconnect()  # Disconnect the client if the token is invalid or expired
            return False  # Reject the connection
    else:
        print("No token provided.")
        disconnect()  # Disconnect the client if no token is provided
        return False  # Reject the connection


@socketio.on('connect')
def on_connect():
    # Get session data from Flask's `session` object (if using Flask sessions)
    session_token = request.cookies.get('session_id')

    if session_token:
        # Check if the session is valid
        user_data = verify_session(session_token)
        if user_data:
            print(f"Client authenticated as {user_data}")
            return True  # Allow connection
        else:
            print("Invalid session.")
            disconnect()  # Disconnect the client
            return False
    else:
        print("No session token found.")
        disconnect()  # Disconnect the client
        return False


# Example route to issue a JWT token (for testing purposes)
@app.route("/login", methods=["POST"])
def login():
    # Normally, you would verify username and password here
    username = request.json.get("username")
    if username:
        # Create a JWT token with an expiration time
        token = jwt.encode(
            {"sub": username, "exp": datetime.utcnow() + timedelta(hours=1)},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Missing username"}), 400


# Event handler for custom message (after connection)
@socketio.on("message")
def handle_message(message):
    print(f"Received message: {message}")
    emit("response", {"data": "Message received"})

if __name__ == "__main__":
    socketio.run(app)
