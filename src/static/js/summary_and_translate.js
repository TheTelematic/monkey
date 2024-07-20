document.addEventListener('DOMContentLoaded', (event) => {
    const inputText = document.getElementById('inputText');
    const responseText = document.getElementById('responseText');
    const summaryText = document.getElementById('summaryText');
    const submitButton = document.getElementById('submitButton');
    const translateButton = document.getElementById('translateButton');
    const loadingContainer1 = document.getElementById('loadingContainer1');
    const loadingContainer2 = document.getElementById('loadingContainer2');
    const historyContent = document.getElementById('historyContent');
    const languageSelector = document.getElementById('languageSelector');
    const newQueryButton = document.getElementById('newQueryButton');

    let currentQuery = null;
    let activeHistoryItem = null;
    const pingInterval = 15000; // 15 seconds

    const socket = new WebSocket('/api/summary-and-translate/ws');

    const sendPing = function() {
        const pingMessage = JSON.stringify({ action: 'ping' });
        socket.send(pingMessage);
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
             if (data.response_raw !== undefined && data.response_summary !== undefined) {
                inputText.value = data.response_query;
                responseText.value = data.response_raw;
                summaryText.value = data.response_summary;
                addToHistory(data.response_query, data.response_raw, data.response_summary);
            }
            newQueryButton.disabled = false;
            translateButton.disabled = false;
            loadingContainer1.style.display = "none";  // Hide loading
            loadingContainer2.style.display = "none";  // Hide loading
        }
    };

    submitButton.addEventListener('click', () => {
        const text = inputText.value;
        if (text.trim() === '') {
            alert('Please enter some text.');
            return;
        }
        submitButton.disabled = true;
        translateButton.disabled = true;
        inputText.readOnly = true;
        loadingContainer1.style.display = "inline";  // Show loading

        const message = JSON.stringify({ action: 'submit', text });
        socket.send(message);
        currentQuery = text;
    });

    translateButton.addEventListener('click', () => {
        const text = currentQuery;
        const targetLanguage = languageSelector.value;
        if (text.trim() === '') {
            alert('Please enter some text.');
            return;
        }
        submitButton.disabled = true;
        translateButton.disabled = true;
        inputText.readOnly = true;
        loadingContainer2.style.display = "inline";  // Show loading

        const message = JSON.stringify({ action: 'translate', text, originLanguage: "ENGLISH", targetLanguage });
        socket.send(message);
    });

    newQueryButton.addEventListener('click', () => {
        currentQuery = null;
        inputText.value = '';
        responseText.value = '';
        summaryText.value = '';
        translateButton.disabled = true;
        submitButton.disabled = false;
        inputText.readOnly = false;
    });

    function addToHistory(query, response, summary) {
        const newItem = document.createElement('div');
        newItem.classList.add('history-item');
        const timestamp = new Date().toLocaleString();  // Add timestamp
        newItem.innerHTML = `<strong>Query:</strong> ${query} <br><small>${timestamp}</small>`;

        // Create details section
        const details = document.createElement('div');
        details.classList.add('history-details');
        details.innerHTML = `
            <strong>Response:</strong> ${response}<br>
            <strong>Summary:</strong> ${summary}
        `;
        newItem.appendChild(details);

        // Add click event to toggle details display
        newItem.addEventListener('click', () => {
            if (activeHistoryItem && activeHistoryItem !== newItem) {
                activeHistoryItem.querySelector('.history-details').style.display = 'none';
            }
            const isDisplayed = details.style.display === 'block';
            details.style.display = isDisplayed ? 'none' : 'block';
            activeHistoryItem = newItem;
        });

        historyContent.prepend(newItem);
    }
});