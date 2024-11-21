import os
import uuid

from flask_restx import Api, Resource, fields
from config import Config
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, disconnect
import jwt
from datetime import datetime, timedelta


app = Flask(__name__)
socketio = SocketIO(app)


# Secret key for JWT encoding and decoding (in a real app, store this securely)
app.config.from_object(Config)

api = Api(
    app,
    version="1.0",
    title="Chat Application API",
    description="API documentation for a Flask-SocketIO Chat Application",
    doc="/doc/swagger"  # Serve Swagger UI at /doc/swagger
)
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
    # Retrieve the session_id and token from the query parameters
    session_token = request.args.get('session_id')
    token = request.args.get('token')

    if token and session_token:
        # Verify the token
        user_data = verify_token(token)
        if user_data:
            # Verify the session_id
            session_data = verify_session(token, session_token)
            if session_data:
                print(f"Client authenticated as {user_data['sub']}")
                return True  # Allow connection
            else:
                print("Invalid session_id.")
                disconnect()  # Disconnect the client
                return False
        else:
            print("Invalid or expired token.")
            disconnect()  # Disconnect the client
            return False
    else:
        print("No token or session_id provided.")
        disconnect()  # Disconnect the client
        return False

ns = api.namespace("auth", description="Authentication APIs")
login_model = api.model("Login", {
    "username": fields.String(description="Username for login", required=True)
})

token_response = api.model("TokenResponse", {
    "session_id": fields.String(description="Session ID (JWT token)"),
    "token": fields.String(description="Authentication token")
})

# Example route to issue a JWT token (for testing purposes)
@ns.route("/login")
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, "Success", token_response)
    @api.response(400, "Validation Error")
    def post(self):
        """Authenticate user and return session ID and token"""
        username = request.json.get("username")
        if username:
            # Generate a unique session_id (this could be a UUID or any unique identifier)
            session_id = str(uuid.uuid4())  # Generate a unique session ID

            # Create the JWT token with session_id included
            token = jwt.encode(
                {"sub": username, "session_id": session_id, "exp": datetime.now() + timedelta(hours=1)},
                Config.SECRET_KEY,
                algorithm="HS256",
            )

            return jsonify({"session_id": session_id, "token": token})
        return {"error": "Missing username"}, 400



def verify_session(token, session_id):
    """
    Verifies the JWT token and checks if the session_id matches.
    """
    try:
        # Decode the token using the secret key
        decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])

        # Verify if the session_id matches
        if decoded.get("session_id") == session_id:
            return {"username": decoded["sub"], "session_id": decoded["session_id"]}
        else:
            return None  # Invalid session_id
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
    
@app.route('/home')
def index():
    print("rendering index.html")
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

api.add_namespace(ns, path='/auth')
# Event handler for custom message (after connection)
# @socketio.on("message")
# def handle_message(message):
#     print(f"Received message: {message}")
#     emit("response", {"data": "Message received"})

# Listen for connection events
# @socketio.on('connect')
# def handle_connect():
#     print("Client connected")

# Listen for disconnection events
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

# Handle incoming messages
@socketio.on('message')
def handle_message(data):
    try:
        print("Received message:", data)
        # Process the message
    except KeyError as e:
        print("Error processing message:", e)

if __name__ == "__main__":
    socketio.run(app)
