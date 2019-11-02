#Python libraries that we need to import for our bot
import random
import os
from dotenv import load_dotenv
from flask import Flask, request
from pymessenger.bot import Bot
import json
from user import user, resetState, createUser
from helper import get_message, send_message
from website import website, product

with open('locale.json') as json_file:
    localdata = json.load(json_file)


load_dotenv()
app = Flask(__name__)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
bot = Bot(ACCESS_TOKEN)


# Store Conversation State here
userState = {}

def sendInitialMessage(userID):
    response = 'This should be the first message I send you back!'
    bot.send_text_message(userID, response)


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
    print('Received Message')
    # get whatever message a user sent the bot
    output = request.get_json()
    for event in output['entry']:
        if (event['messaging'] is None):
            print('No messages in event')
            return "Message Processed"
        messaging = event['messaging']
        for message in messaging:
        # Check if user exists in state management, if not create user
            if message.get('message'):
                recipient_id = message['sender']['id']
                print("Processing Message")
                if message['message'].get('text') == 'debugReset':
                    resetState(userState)
                    send_message(recipient_id, 'Debug: Your State should now be reset!', bot)
                    print('Resetting State')
                    return "Message Processed"
                if (recipient_id not in userState):
                    createUser(recipient_id, userState)
                    sendInitialMessage(recipient_id)
                    print('Sending initial Message')
                else: 
                    if message.get('message'):
                        print(message['message'].get('text'))
                        send_message(recipient_id, 'This should be the same message now', bot)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    print(token_sent)
    return 'Invalid verification token, you shouldn\'t be able to access this page'

if __name__ == "__main__":
    app.run()