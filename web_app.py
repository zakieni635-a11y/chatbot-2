from flask import Flask, render_template, request, jsonify, make_response
import logging
import logging.handlers
import os
import webbrowser
import threading
import shutil
import uuid
from core import bot_reply

# Templates folder is named 'Templates' in this project
app = Flask(__name__, template_folder="Templates")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "")
    reply = bot_reply(user_message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
    from telegram.ext import Updater, MessageHandler, Filters
from core import get_reply
