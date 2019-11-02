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
import requests 

finalJson = {}
load_dotenv()
app = Flask(__name__)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
bot = Bot(ACCESS_TOKEN)
graph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version="2.12")

def generateJson(user):
    jsonObj = {}
    jsonObj["title"] = globalVar.userState[user].websiteName
    jsonObj["jumboText1"] = globalVar.userState[user].slogan
    jsonObj["jumboText2"] = globalVar.userState[user].slogan2
    jsonObj["phoneNumber"] = globalVar.userState[user].phoneNumber
    jsonObj["address"] = globalVar.userState[user].address
    jsonObj["email"] = globalVar.userState[user].email
    return jsonObj

def sendInitialMessage(userID):
    response = globalVar.localdata["initial_msg"][globalVar.locale]
    bot.send_button_message(userID, response, buttons.initial)

def getPayload(message):
    return (message['postback']['payload'])

def startWebsite(userID, message, type='text'):
    response_yes = globalVar.localdata["product_page"][globalVar.locale]
    if type == 'payload' and getPayload(message) == 'yes':
        bot.send_button_message(userID, response_yes, buttons.business_type)
        globalVar.userState[userID].currState = 'selectingType'
        return
    elif type == 'payload' and getPayload(message) == 'no':
        response_no = "Todo fill this later"
        send_message(userID, response_no,bot)
        return

def startBusiness(userID, message, type='text'):
    response = globalVar.localdata["template"][globalVar.locale]
    if type == 'payload' and (getPayload(message) in {'business','community'}):
        globalVar.userState[userID].currState = 'insertName'
        globalVar.userState[userID].businessType = getPayload(message)
        send_message(userID, response, bot)
        buttons.send_carousel(userID, ACCESS_TOKEN)
        return
    elif type == 'payload':
        send_message(userID, "Sorry, that's not a valid option! Please try again!", bot)
        buttons.send_carousel(userID, ACCESS_TOKEN)
        return


@app.route("/testuser", methods=['GET'])
def sendJson():
    return jsonify(generateJson(user))

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
                    print(recipient_id)
                    print(message)
                    print("Processing Message")
                    if (middleWare(message, recipient_id, bot) == True):
                        return "Message Processed"
                    if (recipient_id not in globalVar.userState):
                        createUser(recipient_id)
                        sendInitialMessage(recipient_id)
                        print('Created user with id ', recipient_id)
                        return "Messaged Processed"
                    else: 
                        currState = globalVar.userState[recipient_id].currState
                        if currState == 'initial':
                            startWebsite(recipient_id, message['message'].get('text'), 'text')
                            if(message['message'].get('text') == 'yes'):
                                return "test"
                        elif currState == 'insertName':
                            send_message(recipient_id, "Sorry, that's not a valid option! Please try again!", bot)
                            buttons.send_carousel(recipient_id, ACCESS_TOKEN)
                        elif currState == 'insertName2':
                            # You can validate name here
                            businessName = message['message'].get('text')
                            globalVar.userState[recipient_id].websiteName = businessName
                            responseTemp = "Your business name is " + businessName
                            send_message(recipient_id, responseTemp, bot)
                            send_message(recipient_id, globalVar.localdata["business_address"][globalVar.locale], bot)
                            globalVar.userState[recipient_id].currState = 'insertAddress'
                        elif currState == 'insertAddress':
                            addressName = message['message'].get('text')
                            globalVar.userState[recipient_id].address = addressName
                            responseTemp = "Your business address is " + addressName
                            send_message(recipient_id, responseTemp, bot)
                            send_message(recipient_id, globalVar.localdata["business_email"][globalVar.locale], bot)
                            globalVar.userState[recipient_id].currState = 'insertEmail'
                        elif currState == 'insertEmail':
                            emailName = message['message'].get('text')
                            globalVar.userState[recipient_id].email = emailName
                            responseTemp = "Your email address is " + emailName
                            send_message(recipient_id, responseTemp, bot)
                            send_message(recipient_id, globalVar.localdata["business_phoneNumber"][globalVar.locale], bot)
                            globalVar.userState[recipient_id].currState = 'insertNumber'
                        elif currState == 'insertNumber':
                            numberName = message['message'].get('text')
                            globalVar.userState[recipient_id].phoneNumber = numberName
                            responseTemp = "Your phone number is " + numberName
                            send_message(recipient_id, responseTemp, bot)
                            generateJson(recipient_id)
                            send_message(recipient_id, "Done! We have generated your site!", bot)
                            test = 'https://dynamic-website-builder.herokuapp.com'
                            send_message(recipient_id, test, bot)
                            globalVar.userState[recipient_id].currState = 'free'
                        elif currState == 'free':
                            nlp = message["message"].get("nlp")
                            entities = nlp.get("entities")
                            intent = entities.get("Intent")[0].get("value")
                            website_feat = entities.get("website_feature")[0].get("value")
                            if website_feat == "phone number":
                                web_feat_val = entities.get("phone_number")[0].get("value")
                                globalVar.userState[recipient_id].phoneNumber = web_feat_val
                                responseNLP = "Sure thing! Changing your phoneNumber"
                                send_message(recipient_id, responseNLP, bot)
                            elif website_feat == "address":
                                web_feat_val =entities.get("location")[0].get("value")
                                globalVar.userState[recipient_id].address = web_feat_val
                                responseNLP = "Sure thing! Changing your address!"
                                send_message(recipient_id, responseNLP, bot)
                            elif website_feat == "email":
                                web_feat_val =entities.get("email")[0].get("value")
                                globalVar.userState[recipient_id].email = web_feat_val
                                responseNLP = "Sure thing! Changing your email!"
                                send_message(recipient_id, responseNLP, bot)
                            elif website_feat == "title":
                                web_feat_val =entities.get("title")[0].get("value")
                                globalVar.userState[recipient_id].websiteName = web_feat_val
                                responseNLP = "Sure thing! Changing your business name!"
                                send_message(recipient_id, responseNLP, bot)
                            elif website_feat == "description":
                                web_feat_val =entities.get("slogan")[0].get("value")
                                globalVar.userState[recipient_id].slogan = web_feat_val
                                responseNLP = "Sure thing! Changing your slogan!"
                                send_message(recipient_id, responseNLP, bot)
                            finalJson = generateJson(recipient_id)
                            return "banana"
                            # Do analysis here for NLP
                if message.get('postback'):
                    recipient_id = message['sender']['id']
                    currState = globalVar.userState[recipient_id].currState
                    print(currState)
                    if currState == 'initial':
                        startWebsite(recipient_id, message, 'payload')
                    elif currState == 'selectingType':
                        startBusiness(recipient_id, message, 'payload')
                    elif currState == 'insertName':
                        print('test')
                        send_message(recipient_id, globalVar.localdata["business_name"][globalVar.locale], bot)
                        globalVar.userState[recipient_id].currState = 'insertName2'

        return "Message Processed"
    except Exception as e:
        print("There was an error bug I'm ignoring it")
        print(e)
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