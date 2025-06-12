$(document).ready(function() {
    const chatBox = $('#chat-box');
    const messageInput = $('#message-input');
    const chatForm = $('#chat-form');
    const startRecordBtn = $('#start-record');
    const sendAudioBtn = $('#send-audio');
    let recorder, audioBlob;

    chatForm.on('submit', function(event) {
        event.preventDefault();
        const userMessage = messageInput.val();
        if (userMessage.trim() !== '') {
            appendMessage('user', userMessage);
            messageInput.val('');
            getBotResponse(userMessage);
        }
    });

    startRecordBtn.on('click', function() {
        if (recorder && recorder.state === 'recording') {
            recorder.stop();
            startRecordBtn.find('i').removeClass('fas fa-stop').addClass('fas fa-microphone');
        } else {
            startRecording();
            startRecordBtn.find('i').removeClass('fas fa-microphone').addClass('fas fa-stop');
        }
    });

    sendAudioBtn.on('click', function() {
        if (audioBlob) {
            appendAudioMessage('user', audioBlob);
            getBotResponseFromAudio(audioBlob);
        }
    });

    function appendMessage(sender, message) {
        const messageElement = $('<div>').addClass('chat-message').addClass(sender).append(
            $('<div>').addClass('alert').addClass(sender === 'user' ? 'alert-primary' : 'alert-secondary').text(message)
        );
        chatBox.append(messageElement);
        chatBox.scrollTop(chatBox[0].scrollHeight);
    }

    function appendAudioMessage(sender, audioBlob) {
        const audioUrl = URL.createObjectURL(audioBlob);
        const messageElement = $('<div>').addClass('chat-message').addClass(sender).addClass('audio').append(
            $('<audio controls>').attr('src', audioUrl)
        );
        chatBox.append(messageElement);
        chatBox.scrollTop(chatBox[0].scrollHeight);
    }

    function getBotResponse(message) {
        $.ajax({
            type: 'POST',
            url: '/get_response',
            contentType: 'application/json',
            data: JSON.stringify({ message: message }),
            success: function(response) {
                appendMessage('bot', response.response);
            },
            error: function() {
                appendMessage('bot', 'An error occurred. Please try again later.');
            }
        });
    }

    function getBotResponseFromAudio(audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob);
        $.ajax({
            type: 'POST',
            url: '/get_response',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                appendMessage('bot', response.response);
            },
            error: function() {
                appendMessage('bot', 'An error occurred. Please try again later.');
            }
        });
    }

    async function startRecording() {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        recorder = new MediaRecorder(stream);
        recorder.start();

        const audioChunks = [];
        recorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };
        recorder.onstop = () => {
            audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        };
    }
});
