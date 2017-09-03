# coding: utf-8

# Main file. It assigns the endpoints of the server to the logic.
# It also links the web assets (chat, style, images) to their URL.

import os
from flask import Flask, request, jsonify, send_from_directory
from random import randint

from app import chatbot

app = Flask(__name__)

bot = None


@app.route('/message', methods=['GET'])
def receive_message():
    sender = request.cookies["user_id"]
    message = request.args.get('message')

    input_log = u"Incoming from %s: %s" % (sender, message)
    print(input_log)

    response = bot.respond_to(sender, message)

    output_log = u"Outgoing to %s: %s" % (sender, response)
    print(output_log)

    return jsonify({"message": response})


@app.route("/", methods=['GET'])
def index():
    response = send_from_directory('web', "index.html")
    response.set_cookie("user_id", str(randint(1, 10000000)))
    return response


@app.route("/web/<filename>", methods=['GET'])
def static_files(filename=None):
    return send_from_directory('web', filename)


if __name__ == '__main__':
    bot = chatbot.Bot()
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT)
