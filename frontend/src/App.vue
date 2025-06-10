<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import { marked } from 'marked'

// Configure marked for better security and formatting
marked.setOptions({
  breaks: true,
  gfm: true
})

const wsUrl = ref(import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws')
const socket = ref(null)
const isConnected = ref(false)
const isWaitingForResponse = ref(false)
const message = ref('')
const messages = reactive([])

const connect = () => {
  try {
    socket.value = new WebSocket(wsUrl.value)
    
    socket.value.onopen = () => {
      isConnected.value = true
      addMessage('Connected to server', 'system')
    }
    
    socket.value.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data)
        if (parsed.type && parsed.message) {
          addMessage(parsed.message, parsed.type)
          // Turn off loading indicator for server responses
          if (parsed.type === 'server') {
            isWaitingForResponse.value = false
          }
        } else {
          addMessage(event.data, 'server')
          isWaitingForResponse.value = false
        }
      } catch (e) {
        addMessage(event.data, 'server')
        isWaitingForResponse.value = false
      }
    }
    
    socket.value.onclose = () => {
      isConnected.value = false
      addMessage('Disconnected from server', 'system')
    }
    
    socket.value.onerror = (error) => {
      addMessage('Connection error', 'error')
    }
  } catch (error) {
    addMessage('Failed to connect', 'error')
  }
}

const disconnect = () => {
  if (socket.value) {
    socket.value.close()
  }
}

const sendMessage = () => {
  if (!isConnected.value) {
    connect()
    return
  }
  
  if (socket.value && isConnected.value && message.value.trim()) {
    socket.value.send(message.value)
    addMessage(message.value, 'user')
    isWaitingForResponse.value = true
    message.value = ''
  }
}

const messagesContainer = ref(null)

const addMessage = (text, type) => {
  // If this is a server response, hide any pending info messages (but not query messages)
  if (type === 'server') {
    // Find and hide info messages that came after the last user message
    const lastUserIndex = messages.findLastIndex(msg => msg.type === 'user')
    if (lastUserIndex !== -1) {
      for (let i = lastUserIndex + 1; i < messages.length; i++) {
        if (messages[i].type === 'info') {
          messages[i].hidden = true
        }
        // Note: query messages (type === 'query') are NOT hidden
      }
    }
  }
  
  // Render markdown for server responses and query messages
  const isMarkdown = type === 'server' || type === 'query'
  const renderedText = isMarkdown ? marked(text) : text
  
  messages.push({
    id: Date.now(),
    text,
    renderedText,
    type,
    timestamp: new Date().toLocaleTimeString(),
    hidden: false,
    isMarkdown
  })
  
  // Scroll to bottom after message is added
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

onMounted(() => {
  // Auto-connect removed - only connect when button is clicked
})

const clearMessages = () => {
  messages.length = 0
}

onUnmounted(() => {
  disconnect()
})
</script>

<template>
  <div class="app">
    <header class="header">
      <h1>Connect & Converse</h1>
      <div class="connection-status">
        <span :class="['status-indicator', isConnected ? 'connected' : 'disconnected', { 'pulsing': isConnected && isWaitingForResponse }]"></span>
        <span>{{ isConnected ? 'Connected' : 'Disconnected' }}</span>
        <input v-model="wsUrl" placeholder="WebSocket URL" :disabled="isConnected" />
        <button @click="isConnected ? disconnect() : connect()">
          {{ isConnected ? 'Disconnect' : 'Connect' }}
        </button>
        <button @click="clearMessages" class="clear-button">
          Clear
        </button>
      </div>
    </header>

    <main class="main">
      <div class="messages" ref="messagesContainer">
        <div 
          v-for="msg in messages" 
          :key="msg.id" 
          v-show="!msg.hidden"
          :class="['message', `message-${msg.type}`]"
        >
          <span class="timestamp">{{ msg.timestamp }}</span>
          <div 
            v-if="msg.isMarkdown" 
            class="content markdown-content" 
            v-html="msg.renderedText"
          ></div>
          <span v-else class="content">{{ msg.text }}</span>
        </div>
      </div>

      <form @submit.prevent="sendMessage" class="input-form">
        <div class="input-container">
          <textarea 
            v-model="message" 
            placeholder="Type your message... (Cmd+Enter to send)" 
            rows="3"
            @keydown.meta.enter.prevent="sendMessage"
          ></textarea>
          <button type="submit" :disabled="!isConnected || !message.trim()" class="send-button">
            <span class="send-icon">→</span>
          </button>
        </div>
      </form>
    </main>
  </div>
</template>

<style scoped>
.app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.header {
  margin-bottom: 20px;
}

.header h1 {
  margin: 0 0 15px 0;
  color: #ffffff;
  font-weight: 600;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #ffffff;
}

.status-indicator {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.status-indicator.connected {
  background: #22c55e;
  box-shadow: 0 0 8px rgba(34, 197, 94, 0.5);
}

.status-indicator.disconnected {
  background: #ef4444;
  box-shadow: 0 0 8px rgba(239, 68, 68, 0.5);
}

.status-indicator.pulsing {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}

.connection-status input {
  flex: 1;
  padding: 5px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.connection-status button {
  padding: 5px 15px;
  border: none;
  border-radius: 4px;
  background: #007bff;
  color: white;
  cursor: pointer;
}

.connection-status button:hover {
  background: #0056b3;
}

.clear-button {
  background: #6c757d !important;
}

.clear-button:hover {
  background: #5a6268 !important;
}

.main {
  display: flex;
  flex-direction: column;
  height: 600px;
}

.messages {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  overflow-y: auto;
  margin-bottom: 15px;
  background: white;
  min-height: 480px;
  max-height: 480px;
}

.message {
  margin-bottom: 10px;
  padding: 8px 12px;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
}

.message-user {
  background: #007bff;
  color: white;
  align-self: flex-end;
  max-width: 70%;
}

.message-server {
  background: #e9ecef;
  color: #333;
  align-self: flex-start;
  max-width: 70%;
}

.message-system {
  background: #fff3cd;
  color: #856404;
  align-self: flex-start;
  max-width: 100%;
  font-style: italic;
}

.message-system .timestamp,
.message-error .timestamp,
.message-info .timestamp,
.message-query .timestamp {
  display: none;
}

.message-error {
  background: #f8d7da;
  color: #721c24;
  align-self: flex-start;
  max-width: 100%;
}

.message-info {
  background: #d1ecf1;
  color: #0c5460;
  align-self: flex-start;
  max-width: 100%;
  font-style: italic;
}

.message-query {
  background: #f8f9fa;
  color: #495057;
  border: 1px solid #dee2e6;
  border-left: 4px solid #6f42c1;
  align-self: flex-start;
  max-width: 90%;
  margin: 8px 0;
  font-family: monospace;
}

.timestamp {
  font-size: 0.75em;
  opacity: 0.7;
  margin-bottom: 2px;
}

.content {
  word-wrap: break-word;
}

.markdown-content {
  line-height: 1.6;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  margin: 16px 0 8px 0;
  font-weight: 600;
}

.markdown-content h1 {
  font-size: 1.5em;
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
}

.markdown-content h2 {
  font-size: 1.3em;
  border-bottom: 1px solid #eee;
  padding-bottom: 4px;
}

.markdown-content h3 {
  font-size: 1.1em;
}

.markdown-content p {
  margin: 8px 0;
}

.markdown-content ul,
.markdown-content ol {
  margin: 8px 0;
  padding-left: 24px;
}

.markdown-content li {
  margin: 4px 0;
}

.markdown-content blockquote {
  margin: 12px 0;
  padding: 8px 16px;
  border-left: 4px solid #ddd;
  background: rgba(0, 0, 0, 0.05);
  font-style: italic;
}

.markdown-content code {
  background: rgba(0, 0, 0, 0.1);
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.9em;
}

.markdown-content pre {
  background: rgba(0, 0, 0, 0.1);
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 12px 0;
}

.markdown-content pre code {
  background: none;
  padding: 0;
}

.markdown-content table {
  border-collapse: collapse;
  margin: 12px 0;
  width: 100%;
}

.markdown-content th,
.markdown-content td {
  border: 1px solid #ddd;
  padding: 8px 12px;
  text-align: left;
}

.markdown-content th {
  background: rgba(0, 0, 0, 0.1);
  font-weight: 600;
}

.markdown-content strong {
  font-weight: 600;
}

.markdown-content em {
  font-style: italic;
}

/* Improve readability for server responses */
.message-server .markdown-content {
  max-width: none;
}

.message-server .markdown-content h1:first-child,
.message-server .markdown-content h2:first-child,
.message-server .markdown-content h3:first-child {
  margin-top: 0;
}

.message-server .markdown-content p:last-child {
  margin-bottom: 0;
}

.input-form {
  display: flex;
}

.input-container {
  position: relative;
  width: 100%;
}

.input-form textarea {
  width: 100%;
  padding: 12px 60px 12px 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  resize: none;
  font-family: inherit;
  background: rgba(255, 255, 255, 0.05);
  color: #ffffff;
  font-size: 14px;
  box-sizing: border-box;
}

.input-form textarea::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.input-form textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.input-form textarea:disabled {
  background: rgba(255, 255, 255, 0.02);
  cursor: not-allowed;
  opacity: 0.5;
}

.send-button {
  position: absolute;
  right: 8px;
  top: 5px;
  bottom: 11px;
  width: 44px;
  padding: 0;
  border: none;
  border-radius: 6px;
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  cursor: pointer;
  font-weight: 600;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.3);
  user-select: none;
}

.send-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #0056b3, #004085);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.4);
}

.send-button:active:not(:disabled) {
  transform: translateY(0);
}

.send-button:disabled {
  background: #6c757d;
  cursor: not-allowed;
  opacity: 0.5;
  transform: none;
  box-shadow: none;
}

.send-icon {
  font-size: 28px;
  font-weight: bold;
  transition: transform 0.2s ease;
}

.send-button:hover:not(:disabled) .send-icon {
  transform: translateX(2px);
}
</style>
