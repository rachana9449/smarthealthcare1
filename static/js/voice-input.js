/**
 * MediConnect Voice Input Component
 * Adds voice-to-text functionality to any text input
 */

class VoiceInput {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.currentTarget = null;
        this.init();
    }

    init() {
        // Check if browser supports Speech Recognition
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            // Configure recognition
            this.recognition.continuous = true;
            this.recognition.interimResults = true;
            this.recognition.lang = 'en-US';
            
            // Set up event listeners
            this.setupEventListeners();
        } else {
            console.warn('Speech Recognition not supported in this browser');
        }
    }

    setupEventListeners() {
        if (!this.recognition) return;

        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateButtonState(true);
            this.showToast('Listening... Speak now', 'info');
        };

        this.recognition.onend = () => {
            this.isListening = false;
            this.updateButtonState(false);
        };

        this.recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }

            if (this.currentTarget) {
                const currentValue = this.currentTarget.value;
                const cursorPosition = this.currentTarget.selectionStart;
                
                if (finalTranscript) {
                    // Insert final transcript at cursor position
                    const newValue = currentValue.substring(0, cursorPosition) + 
                                   finalTranscript + 
                                   currentValue.substring(cursorPosition);
                    this.currentTarget.value = newValue;
                    
                    // Move cursor to end of inserted text
                    const newPosition = cursorPosition + finalTranscript.length;
                    this.currentTarget.setSelectionRange(newPosition, newPosition);
                    
                    // Trigger input event for any listeners
                    this.currentTarget.dispatchEvent(new Event('input', { bubbles: true }));
                }
            }
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.isListening = false;
            this.updateButtonState(false);
            
            let errorMessage = 'Voice input error';
            switch(event.error) {
                case 'no-speech':
                    errorMessage = 'No speech detected. Please try again.';
                    break;
                case 'audio-capture':
                    errorMessage = 'Microphone not found. Please check your device.';
                    break;
                case 'not-allowed':
                    errorMessage = 'Microphone access denied. Please allow microphone access.';
                    break;
            }
            this.showToast(errorMessage, 'error');
        };
    }

    start(targetElement) {
        if (!this.recognition) {
            this.showToast('Voice input not supported in this browser', 'warning');
            return;
        }

        if (this.isListening) {
            this.stop();
            return;
        }

        this.currentTarget = targetElement;
        
        try {
            this.recognition.start();
        } catch (error) {
            console.error('Error starting recognition:', error);
            this.showToast('Failed to start voice input', 'error');
        }
    }

    stop() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
            this.showToast('Voice input stopped', 'info');
        }
    }

    updateButtonState(listening) {
        const buttons = document.querySelectorAll('.voice-btn');
        buttons.forEach(btn => {
            if (listening) {
                btn.classList.add('listening');
                btn.innerHTML = '<i class="fas fa-stop"></i>';
                btn.title = 'Stop listening';
            } else {
                btn.classList.remove('listening');
                btn.innerHTML = '<i class="fas fa-microphone"></i>';
                btn.title = 'Start voice input';
            }
        });
    }

    showToast(message, type = 'info') {
        // Remove existing toasts
        const existingToasts = document.querySelectorAll('.voice-toast');
        existingToasts.forEach(toast => toast.remove());

        // Create toast
        const toast = document.createElement('div');
        toast.className = `voice-toast voice-toast-${type}`;
        toast.innerHTML = `
            <div class="voice-toast-content">
                <i class="fas fa-${this.getIconForType(type)}"></i>
                <span>${message}</span>
            </div>
        `;

        document.body.appendChild(toast);

        // Auto remove after 3 seconds
        setTimeout(() => {
            toast.classList.add('fade-out');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    getIconForType(type) {
        const icons = {
            'info': 'info-circle',
            'success': 'check-circle',
            'warning': 'exclamation-triangle',
            'error': 'times-circle'
        };
        return icons[type] || 'info-circle';
    }
}

// Initialize voice input
const voiceInput = new VoiceInput();

// Global function to start voice input
function startVoiceInput(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        voiceInput.start(element);
    }
}

// Add voice button to text inputs
function addVoiceButton(inputElement) {
    if (!inputElement || inputElement.dataset.voiceEnabled) return;
    
    // Mark as voice-enabled
    inputElement.dataset.voiceEnabled = 'true';
    
    // Wrap input if not already wrapped
    if (!inputElement.parentElement.classList.contains('voice-input-wrapper')) {
        const wrapper = document.createElement('div');
        wrapper.className = 'voice-input-wrapper';
        inputElement.parentNode.insertBefore(wrapper, inputElement);
        wrapper.appendChild(inputElement);
    }
    
    // Create voice button
    const voiceBtn = document.createElement('button');
    voiceBtn.type = 'button';
    voiceBtn.className = 'voice-btn';
    voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
    voiceBtn.title = 'Start voice input';
    voiceBtn.onclick = () => voiceInput.start(inputElement);
    
    // Add button to wrapper
    inputElement.parentElement.appendChild(voiceBtn);
}

// Auto-add voice buttons to textareas and text inputs with data-voice attribute
document.addEventListener('DOMContentLoaded', () => {
    // Add to elements with data-voice attribute
    const voiceElements = document.querySelectorAll('[data-voice="true"]');
    voiceElements.forEach(element => addVoiceButton(element));
    
    // Add CSS for toast notifications
    if (!document.getElementById('voice-toast-styles')) {
        const style = document.createElement('style');
        style.id = 'voice-toast-styles';
        style.textContent = `
            .voice-toast {
                position: fixed;
                top: 20px;
                right: 20px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
                padding: 16px 20px;
                z-index: 10000;
                animation: slideInRight 0.3s ease;
                min-width: 300px;
            }
            
            .voice-toast-content {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .voice-toast-content i {
                font-size: 20px;
            }
            
            .voice-toast-info {
                border-left: 4px solid #3b82f6;
            }
            
            .voice-toast-info i {
                color: #3b82f6;
            }
            
            .voice-toast-success {
                border-left: 4px solid #10b981;
            }
            
            .voice-toast-success i {
                color: #10b981;
            }
            
            .voice-toast-warning {
                border-left: 4px solid #f59e0b;
            }
            
            .voice-toast-warning i {
                color: #f59e0b;
            }
            
            .voice-toast-error {
                border-left: 4px solid #ef4444;
            }
            
            .voice-toast-error i {
                color: #ef4444;
            }
            
            .voice-toast.fade-out {
                animation: slideOutRight 0.3s ease;
            }
            
            @keyframes slideInRight {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOutRight {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }
            
            @media (max-width: 768px) {
                .voice-toast {
                    right: 10px;
                    left: 10px;
                    min-width: auto;
                }
            }
        `;
        document.head.appendChild(style);
    }
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { VoiceInput, startVoiceInput, addVoiceButton };
}
