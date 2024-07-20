document.addEventListener('DOMContentLoaded', (event) => {
    const startButton = document.getElementById('startButton');
    const loadingContainer = document.getElementById('loadingContainer');
    const nameContainer = document.querySelector('.phone-name');
    const imageContainer = document.querySelector('.phone-image');
    const featuresList = document.querySelector('.features-list');
    const priceContainer = document.querySelector('.price');
    const chatContainer = document.getElementById('chatContainer');
    const userFeedback = document.getElementById('userFeedback');
    const chatButton = document.getElementById('chatButton');
    const chatAnswer = document.getElementById('chatAnswer');

    let currentPhoneInfo = null;
    const pingInterval = 15000; // 15 seconds

    const socket = new WebSocket('/api/recommend-me-a-phone/ws');

    const sendPing = function() {
        const pingMessage = JSON.stringify({ action: 'ping' });
        socket.send(pingMessage);
        setInterval(sendPing, pingInterval);
    };

    socket.onopen = function() {
        console.log('WebSocket connection established.');
        setInterval(sendPing, pingInterval);
    };

    socket.onclose = function() {
        console.log('WebSocket connection closed.');
        clearInterval(sendPing);
    }

    socket.onerror = function(error) {
        console.error('WebSocket error:', error);
        clearInterval(sendPing);
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (data.action === "ping") {
            socket.send(JSON.stringify({ action: 'pong' }));
        } else {
            if (data.status === 'done') {
              loadingContainer.style.display = "none"; // Hide loading
              chatContainer.style.display = "inline"; // Show chat

              // Update image, features list, and price dynamically
              nameContainer.innerHTML = data.data.name;
              imageContainer.src = data.data.picture_link;

              // Clear previous list
              featuresList.innerHTML = '';
              data.data.specifications.forEach(feature => {
                const li = document.createElement('li');
                li.textContent = feature;
                featuresList.appendChild(li);
              });

              // Update price
              priceContainer.textContent = `${data.data.price}`;

              // Update chat answer
              chatAnswer.textContent = data.data.justification;

              currentPhoneInfo = data.data;
            }
        }
    };

    function sendFeedback() {
        loadingContainer.style.display = "inline"; // Show loading
        const message = JSON.stringify({ action: 'start' , feedback: userFeedback.value, currentPhoneInfo });
        userFeedback.placeholder = userFeedback.value;
        userFeedback.value = '';
        socket.send(message);
    }

    // Listen for Enter key within the input field
    userFeedback.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
          sendFeedback();
        }
    });

    // Listen for button click
    chatButton.addEventListener('click', () => {
        sendFeedback();
    });

    startButton.addEventListener('click', () => {
        startButton.hidden = true;
        loadingContainer.style.display = "inline"; // Show loading
        const message = JSON.stringify({ action: 'start' });
        socket.send(message);
    });
});
