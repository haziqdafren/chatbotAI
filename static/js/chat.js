document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const menuContainer = document.getElementById('menu-container');
    const chatContainer = document.getElementById('chat-container');
    const statsContainer = document.getElementById('stats-container');
    const backToMenuBtn = document.getElementById('back-to-menu');
    const backToMenuStatsBtn = document.getElementById('back-to-menu-stats');
    const menuButtons = document.querySelectorAll('.menu-btn');

    // Flag to track if demo is running
    let isDemoRunning = false;
    let demoTimeout = null;

    // Emoji collections for different types of messages
    const emojiCollections = {
        greeting: ["👋", "😊", "🤝", "✨", "🌟", "🎯", "💫", "🌈"],
        investment: ["💰", "📈", "💎", "🚀", "💹", "📊", "🎯", "💡"],
        success: ["✅", "🎉", "🏆", "💪", "🌟", "✨", "🎯", "💫"],
        warning: ["⚠️", "⚡", "🔔", "💡", "📌", "❗", "🔍", "💭"],
        error: ["😅", "🤔", "❓", "💭", "🔧", "🔄", "📝", "💡"]
    };

    // Function to get random emoji from collection
    function getRandomEmoji(type = 'greeting') {
        const collection = emojiCollections[type] || emojiCollections.greeting;
        return collection[Math.floor(Math.random() * collection.length)];
    }

    // Function to clear chat and show welcome message
    function resetChat() {
        chatMessages.innerHTML = '';
        addMessage('Hai! Saya ProfitPal, sahabat investasi terpercaya Anda. Ada yang ingin ditanyakan?');
    }

    // Function to add a message to the chat
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `flex items-start message ${isUser ? 'user-message' : 'bot-message'}`;
        
        if (isUser) {
            messageDiv.innerHTML = `
                <div class="ml-auto flex items-start">
                    <div class="mr-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-2xl py-3 px-4 max-w-[80%] shadow-md">
                        <p>${message}</p>
                    </div>
                    <div class="flex-shrink-0">
                        <div class="w-10 h-10 rounded-full bg-gradient-to-r from-gray-500 to-gray-600 flex items-center justify-center text-white shadow-lg">
                            <span class="emoji">👤</span>
                        </div>
                    </div>
                </div>
            `;
        } else {
            const emoji = getRandomEmoji();
            messageDiv.innerHTML = `
                <div class="flex-shrink-0">
                    <div class="w-10 h-10 rounded-full bg-gradient-to-r from-blue-500 to-blue-600 flex items-center justify-center text-white shadow-lg">
                        <span class="emoji">${emoji}</span>
                    </div>
                </div>
                <div class="ml-3 bg-gradient-to-r from-blue-100 to-blue-50 rounded-2xl py-3 px-4 max-w-[80%] shadow-md">
                    <p class="text-gray-800">${message}</p>
                </div>
            `;
        }
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to show typing indicator
    function showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'flex items-start message bot-message';
        indicator.innerHTML = `
            <div class="flex-shrink-0">
                <div class="w-10 h-10 rounded-full bg-gradient-to-r from-blue-500 to-blue-600 flex items-center justify-center text-white shadow-lg">
                    <span class="emoji">${getRandomEmoji('greeting')}</span>
                </div>
            </div>
            <div class="ml-3">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        chatMessages.appendChild(indicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return indicator;
    }

    // Function to remove typing indicator
    function removeTypingIndicator(indicator) {
        if (indicator && indicator.parentNode) {
            indicator.parentNode.removeChild(indicator);
        }
    }

    // Function to handle API errors
    function handleApiError(error, message = 'Maaf, terjadi kesalahan. Silakan coba lagi.') {
        console.error('API Error:', error);
        addMessage(message);
    }

    // Function to make API calls with retry
    async function makeApiCall(url, options, retries = 3) {
        for (let i = 0; i < retries; i++) {
            try {
                const response = await fetch(url, options);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return await response.json();
            } catch (error) {
                if (i === retries - 1) throw error;
                await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
            }
        }
    }

    // Function to show demo mode
    async function runDemo() {
        isDemoRunning = true;
        resetChat();
        
        const demoConversations = [
            ["halo profitpal", "Greeting - Menyapa bot"],
            ["siapa kamu", "About Bot - Mengenal ProfitPal"],
            ["saya mau mulai investasi", "Start Investment - Panduan pemula"],
            ["berapa modal minimum", "Minimum Capital - Info modal"],
            ["aplikasi apa yang bagus", "Platform - Rekomendasi apps"],
            ["apa itu reksadana", "Mutual Funds - Edukasi produk"],
            ["investasi saham gimana", "Stocks - Info saham"],
            ["bahaya tidak investasi", "Risk - Manajemen risiko"],
            ["terima kasih ya", "Thanks - Apresiasi"],
            ["sampai jumpa", "Goodbye - Penutup"]
        ];

        for (const [message, description] of demoConversations) {
            if (!isDemoRunning) break;
            
            addMessage(message, true);
            const typingIndicator = showTypingIndicator();
            
            try {
                const data = await makeApiCall('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });

                removeTypingIndicator(typingIndicator);
                
                if (data.response) {
                    addMessage(data.response);
                }
                
                await new Promise(resolve => {
                    demoTimeout = setTimeout(resolve, 1500);
                });
            } catch (error) {
                console.error('Error:', error);
                removeTypingIndicator(typingIndicator);
                handleApiError(error);
                break;
            }
        }
        
        isDemoRunning = false;
    }

    // Function to stop demo mode
    function stopDemo() {
        isDemoRunning = false;
        if (demoTimeout) {
            clearTimeout(demoTimeout);
            demoTimeout = null;
        }
    }

    // Function to show statistics
    async function showStatistics() {
        try {
            const data = await makeApiCall('/api/statistics');
            
            // Animate statistics numbers
            animateNumber('total-intents', data.total_intents);
            animateNumber('total-keywords', data.total_keywords);
            animateNumber('total-responses', data.total_responses);
        } catch (error) {
            console.error('Error fetching statistics:', error);
            handleApiError(error, 'Gagal memuat statistik. Silakan coba lagi.');
        }
    }

    // Function to animate numbers
    function animateNumber(elementId, finalValue) {
        const element = document.getElementById(elementId);
        const duration = 1000; // 1 second
        const steps = 60;
        const stepValue = finalValue / steps;
        let currentValue = 0;
        
        const interval = setInterval(() => {
            currentValue += stepValue;
            if (currentValue >= finalValue) {
                element.textContent = finalValue;
                clearInterval(interval);
            } else {
                element.textContent = Math.floor(currentValue);
            }
        }, duration / steps);
    }

    // Menu navigation
    menuButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            // Add click animation
            button.style.transform = 'scale(0.95)';
            setTimeout(() => {
                button.style.transform = '';
            }, 100);

            switch(index) {
                case 0: // Chat
                    stopDemo(); // Stop any running demo
                    menuContainer.classList.add('hidden');
                    chatContainer.classList.remove('hidden');
                    resetChat(); // Reset chat with welcome message
                    break;
                case 1: // Demo
                    menuContainer.classList.add('hidden');
                    chatContainer.classList.remove('hidden');
                    runDemo();
                    break;
                case 2: // Statistics
                    stopDemo(); // Stop any running demo
                    menuContainer.classList.add('hidden');
                    statsContainer.classList.remove('hidden');
                    showStatistics();
                    break;
                case 3: // Exit
                    if (confirm('Apakah Anda yakin ingin keluar?')) {
                        window.close();
                    }
                    break;
            }
        });
    });

    // Back to menu buttons
    backToMenuBtn.addEventListener('click', () => {
        stopDemo(); // Stop any running demo
        chatContainer.classList.add('hidden');
        menuContainer.classList.remove('hidden');
    });

    backToMenuStatsBtn.addEventListener('click', () => {
        statsContainer.classList.add('hidden');
        menuContainer.classList.remove('hidden');
    });

    // Handle form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;

        // If demo is running, stop it
        if (isDemoRunning) {
            stopDemo();
            resetChat();
        }

        addMessage(message, true);
        userInput.value = '';

        const typingIndicator = showTypingIndicator();

        try {
            const data = await makeApiCall('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            removeTypingIndicator(typingIndicator);

            if (data.response) {
                addMessage(data.response);
            } else {
                handleApiError(new Error('No response from server'));
            }
        } catch (error) {
            console.error('Error:', error);
            removeTypingIndicator(typingIndicator);
            handleApiError(error);
        }
    });

    // Add hover effects to menu buttons
    menuButtons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', () => {
            button.style.transform = '';
        });
    });

    // Focus input on load
    userInput.focus();
}); 