document.getElementById("chatbot-icon").addEventListener("click", function() {
    var chatbox = document.getElementById("chatbox");
    chatbox.style.display = chatbox.style.display === "none" ? "block" : "none";
});

document.getElementById("user-input").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        var userMessage = this.value;
        if (userMessage.trim() !== "") {
            addMessage(userMessage, "user");
            setTimeout(function() {
                addMessage("Sorry, I'm just a demo chatbot.", "bot");
            }, 1000);
        }
        this.value = "";
    }
});

function addMessage(message, type) {
    var chatContent = document.getElementById("chat-content");
    var messageElement = document.createElement("div");
    messageElement.className = "message " + type;
    messageElement.innerText = message;
    chatContent.appendChild(messageElement);
    chatContent.scrollTop = chatContent.scrollHeight;
}

function toggleChatbot() {
    const chatbot = document.getElementById('chatbot');
    chatbot.style.display = (chatbot.style.display === 'none' || chatbot.style.display === '') ? 'block' : 'none';
}

async function sendMessage() {
    const userMessageInput = document.getElementById('userMessage');
    const chatboxMessages = document.getElementById('chatboxMessages');
    
    if (userMessageInput.value.trim()) {    
        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user-message');
        userMessage.textContent = userMessageInput.value;
        chatboxMessages.appendChild(userMessage);
        chatboxMessages.scrollTop = chatboxMessages.scrollHeight;

        // Fetch response from the dynamic chatbot backend
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage.textContent })
        });

        const result = await response.json();

        // Display bot response
        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'bot-message');
        botMessage.textContent = result.reply;
        chatboxMessages.appendChild(botMessage);
        chatboxMessages.scrollTop = chatboxMessages.scrollHeight;

        userMessageInput.value = '';
    }
}

function sendSampleMessage(sampleMessage) {
const userMessageInput = document.getElementById('userMessage');

// Set the input field value to the provided sample message
userMessageInput.value = sampleMessage;

// Call the existing sendMessage function to process the sample message
sendMessage();
}

//         function sendSampleMessage() {
//     const sampleMessage = "This is a sample message";
//     const userMessageInput = document.getElementById('userMessage');

//     // Set the input field value to the sample message
//     userMessageInput.value = sampleMessage;

//     // Call the existing sendMessage function to process the sample message
//     sendMessage();
// }

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

 // Text-to-Speech Function to read out the bot's responses (optional)
function speakText(text) {
const synth = window.speechSynthesis;
const utterance = new SpeechSynthesisUtterance(text);
utterance.lang = 'en-US';
synth.speak(utterance);  // Speak the text
console.log("Speaking text:", text);  // Log spoken text
}

// Speech recognition functionality for voice input
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
alert("Your browser does not support speech recognition. Please try using Chrome or another supported browser.");
} else {
const recognition = new SpeechRecognition();
recognition.lang = 'en-US';  // Set the language
recognition.interimResults = false;  // Only return final results
recognition.maxAlternatives = 1;  // Only one alternative result

// Start speech recognition
function startSpeechRecognition() {
    recognition.start();
    console.log("Speech recognition started...");

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        console.log("Recognized text:", transcript);  // Log recognized text
        document.getElementById('userMessage').value = transcript;  // Set input value
        sendMessage();  // Automatically send the message after recognition
    };

    recognition.onerror = function(event) {
        console.error("Speech recognition error:", event.error);  // Log errors
    };

    recognition.onend = function() {
        console.log("Speech recognition ended");
    };
}

// Function to trigger voice assistant when the microphone button is clicked
function startVoiceAssistant() {
    console.log('Microphone button clicked, starting voice assistant...');
    startSpeechRecognition();  // Start voice recognition
}
}

//         async function submitFeedback() {
//     const userFeedback = document.getElementById('userFeedback').value.trim();

//     if (userFeedback) {
//         // Fetch response from the dynamic chatbot backend for feedback submission
//         const response = await fetch('/feedback', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({ feedback: userFeedback })
//         });

//         const result = await response.json();
//         alert(result.message);  // Show a simple alert message for feedback confirmation

//         // Clear the feedback input box
//         document.getElementById('userFeedback').value = '';
//     } else {
//         alert('Please provide your feedback before submitting.');
//     }
// }

// Toggle the visibility of the feedback form
function toggleFeedbackForm() {
const feedbackSection = document.getElementById('feedbackSection');
const showFeedbackBtn = document.getElementById('showFeedbackBtn');

if (feedbackSection.style.display === 'none') {
    feedbackSection.style.display = 'block'; // Show the form
    showFeedbackBtn.style.display = 'none'; // Hide the "Give Feedback" button
}
}

async function submitFeedback() {
const feedbackMessage = document.getElementById('feedbackMessage').value;

if (feedbackMessage.trim()) {
    const response = await fetch('/submit_feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ feedback: feedbackMessage }),
    });

    const result = await response.json();
    alert(result.message);
    document.getElementById('feedbackMessage').value = ''; // Clear input after submission
} else {
    alert('Please enter feedback');
}

    // Existing functions here, like toggleChatbot, sendMessage, etc.

    // Voice Assistant Code (paste here)
    
        // Check for browser support of SpeechRecognition API
    // Check for browser support of SpeechRecognition API
    }

    function toggleGrid(gridId) {
        var grid = document.getElementById(gridId);
        if (grid.classList.contains('hidden')) {
            grid.classList.remove('hidden');
        } else {
            grid.classList.add('hidden');
        }
    }

    function scrollPage(amount) {
        const chatbotBody = document.querySelector('.chatbox-messages');
        chatbotBody.scrollBy({ top: amount, behavior: 'smooth' });
    }
    const chatboxMessages = document.getElementById("chatboxMessages");
        chatboxMessages.scrollTop = chatboxMessages.scrollHeight;
