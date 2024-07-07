document.addEventListener('DOMContentLoaded', (event) => {
    const startButton = document.getElementById('startButton');
    const loadingContainer = document.getElementById('loadingContainer');
    const resultContainer = document.getElementById('resultContainer');

    const socket = new WebSocket('/api/recommend-me-a-phone/ws');

    socket.onopen = function() {
        console.log('WebSocket connection established.');
    };

    socket.onerror = function(error) {
        console.error('WebSocket error:', error);
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.status === 'done') {
            resultContainer.innerText = data.data;

            startButton.disabled = false;
            loadingContainer.style.display = "none";  // Hide loading
        }
    };

    startButton.addEventListener('click', () => {
        startButton.disabled = true;
        loadingContainer.style.display = "inline";  // Show loading
        const message = JSON.stringify({ action: 'start' });
        socket.send(message);
    });
});