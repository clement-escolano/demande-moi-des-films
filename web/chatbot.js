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
            url: "/message?message=" + message,
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

            submit.addClass('disabled');
            submit.attr('disabled', 'disabled');

            setTimeout(function() {
                botPre     = '<span class="message">Chatflix écrit... <i class="glyphicon glyphicon-pencil"></i></span>';
                botVal     = message;
                botMessage = chatbotMessage.html() + '<p class="from-bot"><span class="user">Chatflix: </span>' + botPre + '</p>';
                chatbotMessage.html(botMessage);
                scrollToMessage();
                input.select();
            }, 50);

            setTimeout(function() {
                botMessageReplace = $('#chatbot-message .from-bot:last-child()');
                botMessage = '<span class="user">Chatflix: </span>' + botVal;
                botMessageReplace.html(botMessage);
                scrollToMessage();
                submit.removeClass('disabled');
                submit.removeAttr('disabled');
                input.select();
            }, 500);

        } else {

            userVal     = input.val();
            userMessage = chatbotMessage.html() + '<p class="from-user"><span class="user">Vous: </span>' + userVal + '</p>';
            chatbotMessage.html(userMessage);
            scrollToMessage();
            input.val('');
            input.select();
        }
    }
});