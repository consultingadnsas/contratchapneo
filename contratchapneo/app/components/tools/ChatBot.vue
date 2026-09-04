<template>
    <div class="chatbot-container">
        <!-- Fenêtre de chat -->
        <div v-if="chatStore.isOpen" class="chat-window">
            <div class="chat-header">
                <div class="header-info">
                    <span class="status-dot"></span>
                    <h3>Assistant Juridique</h3>
                </div>
                <button @click="chatStore.toggleChat" class="btn-close">✕</button>
            </div>
            
            <div class="chat-messages" ref="messagesContainer">
                <div 
                    v-for="(msg, index) in chatStore.messages" 
                    :key="index"
                    :class="['message', msg.sender === 'bot' ? 'bot-msg' : 'user-msg']"
                >
                    {{ msg.text }}
                </div>
                
                <div v-if="chatStore.isTyping" class="message bot-msg typing-indicator">
                    <span>.</span><span>.</span><span>.</span>
                </div>
            </div>

            <!-- Barre de saisie -->
            <div class="chat-input-area">
                <input 
                    type="text" 
                    v-model="userInput" 
                    @keyup.enter="handleSend"
                    placeholder="Écrivez votre message..." 
                    :disabled="chatStore.isTyping"
                />
                <button @click="handleSend" :disabled="!userInput.trim() || chatStore.isTyping">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="send-icon">
                      <path d="M3.478 2.404a.75.75 0 0 0-.926.941l2.432 7.905H13.5a.75.75 0 0 1 0 1.5H4.984l-2.432 7.905a.75.75 0 0 0 .926.94 60.519 60.519 0 0 0 18.445-8.986.75.75 0 0 0 0-1.218A60.517 60.517 0 0 0 3.478 2.404Z" />
                    </svg>
                </button>
            </div>
        </div>

        <button @click="chatStore.toggleChat" class="chat-fab">
            <svg v-if="!chatStore.isOpen" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="fab-icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-.065 4.48 4.48 0 0 0 .978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z" />
            </svg>
            <!-- Icône de fermeture (affichée si ouvert) -->
            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="fab-icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
        </button>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch, nextTick } from 'vue';
import { useChatStore } from '../../stores/chatStore';

export default defineComponent({
    name: 'Chatbot',
    setup() {
        const chatStore = useChatStore();
        const messagesContainer = ref<HTMLElement | null>(null);
        const userInput = ref('');

        const handleSend = () => {
            if (userInput.value.trim() && !chatStore.isTyping) {
                chatStore.analyzeInput(userInput.value);
                userInput.value = ''; // Vider le champ
            }
        };

        watch(() => chatStore.messages.length, async () => {
            await nextTick();
            if (messagesContainer.value) {
                messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
            }
        });

        return { chatStore, messagesContainer, userInput, handleSend };
    }
});
</script>

<style scoped>
.chatbot-container {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    z-index: 9999;
    font-family: 'Inter', sans-serif;
}

.chat-fab {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: #0f172a;
    color: white;
    font-size: 1.5rem;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: transform 0.2s;
}
.chat-fab:hover {
    transform: scale(1.05);
}

.chat-window {
    position: absolute;
    bottom: 80px;
    right: 0;
    width: 350px;
    height: 500px;
    
    /* ⚡️ LA CORRECTION EST ICI : 
       La hauteur maximale sera égale à 100% de la hauteur de l'écran 
       moins 120 pixels (pour laisser de la marge en haut et en bas) */
    max-height: calc(100vh - 120px); 
    
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    border: 1px solid #e5e7eb;
}

.chat-fab {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: #0f172a;
    color: white;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: transform 0.2s;
    
    /* Centrage de l'icône SVG */
    display: flex;
    justify-content: center;
    align-items: center;
}

.chat-fab:hover {
    transform: scale(1.05);
}

.fab-icon {
    width: 28px;
    height: 28px;
}

.chat-header {
    background: #0f172a;
    color: white;
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.chat-header h3 {
    width: fit-content;
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
}
.btn-close {
    background: transparent;
    border: none;
    margin: -9rem;
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
}

.chat-messages {
    flex: 1;
    padding: 1rem;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
    background: #f8f9fa;
}

.message {
    padding: 0.8rem 1rem;
    border-radius: 12px;
    max-width: 80%;
    font-size: 0.9rem;
    line-height: 1.4;
}
.bot-msg {
    background: #e2e8f0;
    color: #0f172a;
    align-self: flex-start;
    border-bottom-left-radius: 2px;
}
.user-msg {
    background: #3b82f6;
    color: white;
    align-self: flex-end;
    border-bottom-right-radius: 2px;
}

.chat-options {
    padding: 1rem;
    background: #ffffff;
    border-top: 1px solid #e5e7eb;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}
.btn-option {
    background: #ffffff;
    border: 1px solid #3b82f6;
    color: #3b82f6;
    padding: 0.6rem 1rem;
    border-radius: 20px;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 500;
    transition: all 0.2s;
    text-align: left;
}
.btn-option:hover {
    background: #eff6ff;
}

.typing-indicator span {
    animation: blink 1.4s infinite both;
    font-weight: bold;
    font-size: 1.2rem;
}
.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

@keyframes blink {
    0% { opacity: 0.2; }
    20% { opacity: 1; }
    100% { opacity: 0.2; }
}
.header-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.status-dot {
    width: 8px;
    height: 8px;
    background-color: #10b981; /* Vert "En ligne" */
    border-radius: 50%;
}

.chat-input-area {
    display: flex;
    padding: 1rem;
    background: #ffffff;
    border-top: 1px solid #e5e7eb;
    gap: 0.5rem;
}

.chat-input-area input {
    flex: 1;
    padding: 0.8rem 1rem;
    border: 1px solid #d1d5db;
    border-radius: 20px;
    outline: none;
    font-size: 0.9rem;
    transition: border-color 0.2s;
}

.chat-input-area input:focus {
    border-color: #3b82f6;
}

.chat-input-area input:disabled {
    background: #f3f4f6;
    cursor: not-allowed;
}

.chat-input-area button {
    background: #3b82f6;
    color: white;
    border: none;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transition: background 0.2s;
}

.chat-input-area button:disabled {
    background: #9ca3af;
    cursor: not-allowed;
}

.send-icon {
    width: 18px;
    height: 18px;
}
</style>