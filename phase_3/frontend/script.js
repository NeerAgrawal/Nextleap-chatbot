// Nextleap RAG Chatbot - Frontend JavaScript

const chatContainer = document.getElementById('chatContainer');
const chatForm = document.getElementById('chatForm');
const queryInput = document.getElementById('queryInput');
const sendBtn = document.getElementById('sendBtn');
const statusElement = document.getElementById('status');

// Auto-resize textarea
queryInput.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Handle Enter key (send on Enter, new line on Shift+Enter)
queryInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

// Quick question buttons
document.querySelectorAll('.quick-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        const query = this.dataset.query;
        queryInput.value = query;
        chatForm.dispatchEvent(new Event('submit'));
    });
});

// Handle form submission
chatForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    const query = queryInput.value.trim();
    if (!query) return;

    // Hide welcome message
    const welcomeMsg = document.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.style.display = 'none';
    }

    // Add user message
    addMessage(query, 'user');

    // Clear input
    queryInput.value = '';
    queryInput.style.height = 'auto';

    // Disable send button
    sendBtn.disabled = true;
    updateStatus('Thinking...', false);

    // Show loading indicator
    const loadingId = addLoadingMessage();

    try {
        // Call API
        const response = await fetch('http://localhost:5000/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });

        if (!response.ok) {
            throw new Error('Failed to get response');
        }

        const data = await response.json();

        // Remove loading indicator
        removeMessage(loadingId);

        // Add bot response
        addMessage(data.answer, 'bot', data.sources, data.metadata);

        updateStatus('Ready', true);

    } catch (error) {
        console.error('Error:', error);
        removeMessage(loadingId);
        addMessage('Sorry, I encountered an error. Please make sure the API server is running and try again.', 'bot', null, null, true);
        updateStatus('Error', false);
    } finally {
        sendBtn.disabled = false;
    }
});

function addMessage(text, sender, sources = null, metadata = null, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? 'You' : 'NL';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.textContent = text;

    contentDiv.appendChild(textDiv);

    // Metadata hidden per user request - shows only clean response
    /*
    // Add sources and metadata for bot messages
    if (sender === 'bot' && sources && sources.length > 0 && !isError) {
        const metaDiv = document.createElement('div');
        metaDiv.className = 'message-meta';

        const sourcesText = sources.slice(0, 3).map(s => {
            const badge = document.createElement('span');
            badge.className = 'source-badge';
            badge.textContent = `${s.category} (${(s.similarity * 100).toFixed(0)}%)`;
            return badge.outerHTML;
        }).join('');

        metaDiv.innerHTML = sourcesText;

        if (metadata) {
            const tokensSpan = document.createElement('span');
            tokensSpan.style.color = 'var(--text-secondary)';
            tokensSpan.style.fontSize = '11px';
            tokensSpan.textContent = `• ${metadata.tokens_used} tokens`;
            metaDiv.appendChild(tokensSpan);
        }

        contentDiv.appendChild(metaDiv);
    }
    */

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);

    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    return messageDiv;
}

function addLoadingMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    messageDiv.id = 'loading-' + Date.now();

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = 'NL';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading';
    loadingDiv.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';

    contentDiv.appendChild(loadingDiv);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);

    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    return messageDiv.id;
}

function removeMessage(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

function updateStatus(text, isReady) {
    const statusDot = statusElement.querySelector('.status-dot');
    const statusText = statusElement.querySelector('span:last-child');

    statusText.textContent = text;

    if (isReady) {
        statusDot.style.background = 'var(--success)';
    } else {
        statusDot.style.background = '#f59e0b';
    }
}

// Check API health on load
async function checkHealth() {
    try {
        const response = await fetch('http://localhost:5000/api/health');
        if (response.ok) {
            updateStatus('Ready', true);
        } else {
            updateStatus('API Offline', false);
        }
    } catch (error) {
        updateStatus('API Offline', false);
        console.error('Health check failed:', error);
    }
}

// Check health on page load
checkHealth();
