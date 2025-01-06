// Replace with your server URL (relative since served on the same domain)
const SERVER_URL = "ws://92.205.25.58:5003";

// Retrieve session_id and token from localStorage
const sessionId = localStorage.getItem("session_id");
const token = localStorage.getItem("token");
const username = localStorage.getItem("username"); // Retrieve the username from localStorage

// Check if session_id and token exist in localStorage
if (!sessionId || !token) {
    console.log("Session ID or Token is missing. Please log in.");
    window.location.href = "/login";  // Redirecting to the login page
} else {
    // Connect to the server with query parameters for authentication
    const socket = io(SERVER_URL, {
        query: {
            session_id: sessionId,
            token: token,
        },
    });

    // DOM elements
    const statusElement = document.getElementById("status");
    const sendMessageButton = document.getElementById("sendMessage");
    const messageInput = document.getElementById("message-input");
    const userList = document.getElementById("user-list");
    const messageContainer = document.getElementById("messages");
    const feedbackElement = document.createElement('div'); // Create a feedback element
    feedbackElement.style.color = 'red'; // Style for feedback
    document.body.insertBefore(feedbackElement, messageContainer); // Insert feedback above messages
    const typingStatusElement = document.createElement('div'); // Create a typing status element
    typingStatusElement.style.fontStyle = 'italic'; // Style for typing status
    document.body.insertBefore(typingStatusElement, messageContainer); // Insert typing status above messages

    // Update connection status
    socket.on("connect", () => {
        statusElement.textContent = "Connected";
        console.log("Connected to the server");
    });

    socket.on("disconnect", () => {
        statusElement.textContent = "Disconnected";
        console.log("Disconnected from the server");
        // window.location.href ="/login";
    });

    // Listen for server responses
    socket.on("response", (data) => {
        console.log("Received response from server:", data);
        feedbackElement.textContent = "Server says: " + JSON.stringify(data); // Show server response
    });

    // Listen for the user list update
    socket.on("user_list", (users) => {
        userList.innerHTML = '';  // Clear the current list
        users.forEach(user => {
            const li = document.createElement('li');
            li.textContent = user;
            userList.appendChild(li);
        });
    });

    // Listen for incoming messages
    socket.on("receive_message", (data) => {
        const messageElement = document.createElement('div');
        messageElement.textContent = `${data.sender}: ${data.message}`; // Format: username: message
        messageContainer.appendChild(messageElement);
    });

    // Listen for typing status
    socket.on("typing", (username) => {
        typingStatusElement.textContent = `${username} is typing...`; // Update typing status
        setTimeout(() => {
            typingStatusElement.textContent = ''; // Clear typing status after a delay
        }, 2000); // Clear after 2 seconds
    });

    // Send a message to all connected users
    sendMessageButton.addEventListener("click", () => {
        const message = messageInput.value; // Get the message from the input box
        if (message) {
            socket.emit("send_message", { message: message }); // Emit the message to the server
            messageInput.value = '';  // Clear the input after sending
            feedbackElement.textContent = ''; // Clear feedback message
        } else {
            feedbackElement.textContent = "Please enter a message."; // Show feedback in the UI
        }
    });

    // Emit typing status when the user is typing
    messageInput.addEventListener("input", () => {
        
        socket.emit("typing", { username: username }); // Emit typing event to the server with username
    });
}
