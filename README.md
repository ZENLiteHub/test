# Chat Application

This project is a real-time chat application built using Flask and Socket.IO. It allows users to connect, send messages to all connected users, and see who is currently online. The application also supports typing notifications, indicating when a user is typing a message.

## Features

- User authentication with JWT tokens.
- Real-time messaging between users.
- Display of connected users.
- Typing status notifications.

## Routes

### Authentication Routes

- **POST /auth/login**: Authenticates a user and returns a session ID and token.
  - **Request Body**:
    - `username`: The username for login (required).
  - **Response**:
    - `session_id`: The session ID (JWT token).
    - `token`: The authentication token.

### WebSocket Events

- **connect**: Triggered when a user connects to the WebSocket server.
- **disconnect**: Triggered when a user disconnects from the WebSocket server.
- **send_message**: Sends a message to all connected users.
  - **Data**:
    - `message`: The message content.
- **typing**: Notifies all connected users that a user is typing.
  - **Data**:
    - `username`: The username of the user who is typing.
- **user_list**: Broadcasts the list of currently connected users.
- **receive_message**: Receives messages sent by other users.

## Installation

1. Clone the repository.
2. Install the required packages using pip:

   ```sh
   pip install -r requirements.txt
   ```

3. Run the application:

   ```sh
   python app.py
   ```

## Usage

1. Open your browser and navigate to `http://localhost:5000/login` to log in.
2. Enter your username and click "Login".
3. After logging in, you will be redirected to the chat interface where you can send messages and see other connected users.
