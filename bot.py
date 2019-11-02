#Python libraries that we need to import for our bot
import random
import os
from dotenv import load_dotenv
from flask import Flask, request
from pymessenger.bot import Bot
import json


load_dotenv()
app = Flask(__name__)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
bot = Bot(ACCESS_TOKEN)


# Store Conversation State here
userState = {}

class user:
    def __init__(self, userID):
        self.userID = userID
        self.testvar = 'test'
        self.currState = 'initial'
        self.websites = []

    def updateState(self, newState):
        self.currState = newState

    # def websites():

class website:
    def __init__(self):
        self.websiteName = ''
        self.websiteDescription = ''
        self.productList = []

class product:
    def __init__(self, name, price = None, imageLink = None, productCategory = None):
        self.name = name
        self.price = price
        self.imageLink = imageLink
        self.productCategory = ''

def createUser(userID):
    userState[userID] = user
    print('Create new user!')

def sendInitialMessage(userID):
    response = 'This should be the first message I send you back!'
    bot.send_text_message(userID, response)

def resetState():
    userState.clear()

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
                    resetState()
                    send_message(recipient_id, 'Debug: Your State should now be reset!')
                    print('Resetting State')
                    return "Message Processed"
                if (recipient_id not in userState):
                    createUser(recipient_id)
                    sendInitialMessage(recipient_id)
                    print('Sending initial Message')
                else: 
                    if message.get('message'):
                        print(message['message'].get('text'))
                        send_message(recipient_id, 'This should be the same message now')
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    print(token_sent)
    return 'Invalid verification token, you shouldn\'t be able to access this page'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()