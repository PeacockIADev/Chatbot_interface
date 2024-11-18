// Function to send the message
function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;

    var chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += "<div class='chat-message user-message'><strong>You:</strong> " + userInput + "</div>";

    // Clear input field
    document.getElementById("user-input").value = "";

    // Send user input to the Flask backend
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({prompt: userInput})
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += "<div class='chat-message bot-message'><strong>Bot:</strong> " + data.response + "</div>";
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
    })
    .catch(error => {
        console.error("Error:", error);
        chatBox.innerHTML += "<div class='chat-message bot-message'><strong>Bot:</strong> Sorry, there was an error processing your message.</div>";
    });
}

// Function to handle the "Enter" key
document.getElementById("user-input").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
