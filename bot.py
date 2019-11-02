#Python libraries that we need to import for our bot
import random
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from pymessenger.bot import Bot
import json
from user import user, resetState, createUser
from helper import get_message, send_message
from website import website, product
import facebook
from debugtools import middleWare
import globalVar
import buttons

load_dotenv()
app = Flask(__name__)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
bot = Bot(ACCESS_TOKEN)
graph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version="2.12")
buildJson = {}

def sendInitialMessage(userID):
    response = globalVar.localdata["initial_msg"][globalVar.locale]
    bot.send_button_message(userID, response, buttons.initial)

def getPayload(message):
    return (message['postback']['payload'])

def startWebsite(userID, message, type='text'):
    response_yes = globalVar.localdata["product_page"][globalVar.locale]
    if type == 'payload' and getPayload(message) == 'yes':
        bot.send_button_message(userID, response_yes, buttons.business_type)
        return
    elif type == 'payload' and getPayload(message) == 'no':
        response_no = "Todo fill this later"
        send_message(userID, response_no,bot)
        return


@app.route("/testuser", methods=['GET'])
def sendJson():
    return jsonify(buildJson)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET'])
def verify_message():
    """Before allowing people to message your bot, Facebook has implemented a verify token
    that confirms all requests that your bot receives came from Facebook.""" 
    token_sent = request.args.get("hub.verify_token")
    return verify_fb_token(token_sent)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['POST'])
def receive_message():
    try:
        print('Received Message')
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            if ("messaging" not in event):
                print('No messages in event')
                return "Message Processed"
            messaging = event['messaging']
            for message in messaging:
            # Check if user exists in state management, if not create user
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    print("Processing Message")
                    if (middleWare(message, recipient_id, bot) == True):
                        return "Message Processed"
                    if (recipient_id not in globalVar.userState):
                        createUser(recipient_id)
                        sendInitialMessage(recipient_id)
                        print('Created user with id ', recipient_id)
                        return "Messaged Processed"
                    else: 
                        if globalVar.userState[recipient_id].currState == 'initial':
                            startWebsite(recipient_id, message['message'].get('text'), 'text')
                            if(message['message'].get('text') == 'yes'):
                                return "test"
                if message.get('postback'):
                    recipient_id = message['sender']['id']
                    if globalVar.userState[recipient_id].currState == 'initial':
                        startWebsite(recipient_id, message, 'payload')

        return "Message Processed"
    except:
        print("There was an error bug I'm ignoring it")
        return "Errored out!"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    print(token_sent)
    return 'Invalid verification token, you shouldn\'t be able to access this page'

if __name__ == "__main__":
    app.run()