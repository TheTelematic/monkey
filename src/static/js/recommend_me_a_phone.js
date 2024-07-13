document.addEventListener('DOMContentLoaded', (event) => {
    const startButton = document.getElementById('startButton');
    const loadingContainer = document.getElementById('loadingContainer');
    const nameContainer = document.querySelector('.phone-name');
    const imageContainer = document.querySelector('.phone-image');
    const featuresList = document.querySelector('.features-list');
    const priceContainer = document.querySelector('.price');

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
          loadingContainer.style.display = "none"; // Hide loading

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
        }
    };

    startButton.addEventListener('click', () => {
        startButton.disabled = true;
        loadingContainer.style.display = "inline"; // Show loading
        const message = JSON.stringify({ action: 'start' });
        socket.send(message);
    });
});