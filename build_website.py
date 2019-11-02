#Python libraries that we need to import for our bot
from dotenv import load_dotenv
from flask import Flask, request
from helper import get_message, send_message
import json


load_dotenv()
app = Flask(__name__)

@app.route("/build", methods=["POST"])
def build_website():
    req_message = request.args.get("message")
    if(req_message == "Website ready"):
        send_message(recipient_id, "Check out your website: https://dynamic-website-builder.herokuapp.com/", bot)