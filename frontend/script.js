/* Add your JavaScript code here */

let lastMessage = '';

function sendMessage() {
    const chatBox = document.getElementById('chat-box');
    const inputMessage = document.getElementById('input-message');
    const messageText = inputMessage.value.trim();

    if (messageText !== '') {
        // Create a user message bubble
        const userBubble = document.createElement('div');
        userBubble.classList.add('user-message');
        userBubble.innerText = messageText;
        chatBox.appendChild(userBubble);

        lastMessage = messageText; // Save the last message
        inputMessage.value = '';
        chatBox.scrollTop = chatBox.scrollHeight; // Auto scroll to the bottom

        // Send the message to Rasa
        sendToRasa(messageText);
    }
}

function resendLastMessage() {
    const inputMessage = document.getElementById('input-message');
    inputMessage.value = lastMessage;
}

function clearChatHistory() {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = '';
}

var input = document.getElementById("input-message");

// Execute a function when the user presses a key on the keyboard
input.addEventListener("keypress", function (event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        document.getElementById("mybttn").click();
    }
});

// Function to send the user's message to Rasa
async function sendToRasa(userMessage) {
    const response = await fetch('http://localhost:5005/webhooks/rest/webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sender: 'user', message: userMessage })
    });

    const responseData = await response.json();
    if (responseData && responseData.length > 0) {
        addToChatBox('Bot', responseData[0].text);
    }
}

// Function to add a message to the chat box
function addToChatBox(sender, message) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('bot-message');
    messageDiv.innerHTML = `${sender}: ${message}`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Add an event listener to the "Clear Chat" button
document.getElementById("clearChatButton").addEventListener("click", clearChatHistory);

function openLoginWindow() {
    document.getElementById("loginWindow").style.left = "0";
}

function closeLoginWindow() {
    document.getElementById("loginWindow").style.left = "-300px";
}

// Close the login window if the user clicks outside of it
window.onclick = function (event) {
    if (event.target == document.getElementById("loginWindow")) {
        closeLoginWindow();
    }
};

