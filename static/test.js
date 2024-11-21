// Replace with your server URL (relative since served on the same domain)
const SERVER_URL = "/";

// Retrieve session_id and token from localStorage
const sessionId = localStorage.getItem("session_id");
const token = localStorage.getItem("token");

// Check if session_id and token exist in localStorage
if (!sessionId || !token) {
    console.log("Session ID or Token is missing. Please log in.");
    // Optionally, redirect to the login page or show an error message
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

    // Update connection status
    socket.on("connect", () => {
        statusElement.textContent = "Connected";
        console.log("Connected to the server");
    });

    socket.on("disconnect", () => {
        statusElement.textContent = "Disconnected";
        console.log("Disconnected from the server");
    });

    // Listen for server responses
    socket.on("response", (data) => {
        console.log("Received response from server:", data);
        alert("Server says: " + JSON.stringify(data));
    });

    // Send a test message to the server
    sendMessageButton.addEventListener("click", () => {
        const message = { text: "Hello from the client!" };
        console.log("Sending message:", message);
        socket.emit("message", message);
    });
}
