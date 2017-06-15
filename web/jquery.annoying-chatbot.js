$(document).ready(function() {

    // Annoying Chatbot
    //==================================================================================================================

    $('#chatbot').on('click', '#chatbot-submit', function(e) {
        e.preventDefault();

        message = $('#chatbot-input').val();
        message = message.toLowerCase();
        if (!message) {
            return;
        }
        sendMessage();
        bot(message);
    });

    function bot(message) {
        $.ajax({
            type: 'GET',
            url: "http://localhost:5000/message?message=" + message,
            dataType: 'json',
            success: function (data) {
                sendMessage(data.message);
            }
        });
    }

    // scroll to the bottom of chat box
    function scrollToMessage() {
        var msgBox = $('#chatbot-message');
        var height = msgBox[0].scrollHeight;
        msgBox.scrollTop(height);
    }

    // sending message
    function sendMessage(message) {
        var input = $('#chatbot-input');
        var submit = $('#chatbot-submit');
        var chatbotMessage = $('#chatbot-message');

        if (message) {

            input.addClass('disabled');
            input.attr('disabled', 'disabled');
            submit.addClass('disabled');
            submit.attr('disabled', 'disabled');

            setTimeout(function() {
                botPre     = '<span class="message">Chatflix écrit... <i class="glyphicon glyphicon-pencil"></i></span>';
                botVal     = message;
                botMessage = chatbotMessage.html() + '<p class="from-bot"><span class="user">Chatflix: </span>' + botPre + '</p>';
                input.attr('placeholder', 'Chatflix écrit...');
                chatbotMessage.html(botMessage);
                scrollToMessage();
            }, 50);

            setTimeout(function() {
                botMessageReplace = $('#chatbot-message .from-bot:last-child()');
                botMessage = '<span class="user">Chatflix: </span>' + botVal;
                input.attr('placeholder', 'Écrivez votre message');
                botMessageReplace.html(botMessage);
                scrollToMessage();
                input.removeClass('disabled');
                input.removeAttr('disabled');
                submit.removeClass('disabled');
                submit.removeAttr('disabled');
            }, 500);

        } else {

            userVal     = input.val();
            userMessage = chatbotMessage.html() + '<p class="from-user"><span class="user">Vous: </span>' + userVal + '</p>';
            chatbotMessage.html(userMessage);
            scrollToMessage();
            input.val('');

        }
    }
});