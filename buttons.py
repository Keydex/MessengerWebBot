import globalVar
import json
import requests

initial = [{
    "type": "postback",
    "title": globalVar.localdata["initial_msg_response1"][globalVar.locale],
    "payload": "yes"
    },
    {
    "type": "postback",
    "title": globalVar.localdata["initial_msg_response2"][globalVar.locale],
    "payload": "no"
    }]

business_type = [{
    "type": "postback",
    "title": globalVar.localdata["product_page_response1"][globalVar.locale],
    "payload": "business"
    },
    {
    "type": "postback",
    "title": globalVar.localdata["product_page_response2"][globalVar.locale],
    "payload": "community"
    }]

template_type = [{
    "type": "postback",
    "title": globalVar.localdata["product_page_response1"][globalVar.locale],
    "payload": "business"
    },
    {
    "type": "postback",
    "title": globalVar.localdata["product_page_response2"][globalVar.locale],
    "payload": "community"
    }]

def send_carousel(userID, ACCESS_TOKEN):
    API_ENDPOINT = "https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN
    tempData = {
    "recipient":{
        "id":userID
    },
    "message":{
        "attachment":{
        "type":"template",
        "payload":{
            "template_type":"generic",
            "elements":[
            {
                "title":"Fall Theme!",
                "image_url":"https://scontent-ort2-2.xx.fbcdn.net/v/t1.15752-9/74908125_1451408021681572_7970611728234840064_n.png?_nc_cat=106&_nc_oc=AQkv6ZaGppANVykINRFLmgJaQakLRETpRkK_FvHFHSHOOfCWZGLvYh4FFiMq7TTELiA&_nc_ht=scontent-ort2-2.xx&oh=60a1ef2ba3c9a80c8516afc1e88e4bbf&oe=5E1C14E6",
                "subtitle":"Moody vibes!",
                "buttons":[
                {
                    "type":"postback",
                    "title":"Use theme 1!",
                    "payload":"template_1"
                }    
                ]      
            },
                {
                "title":"Ocean Theme!",
                "image_url":"https://scontent-ort2-2.xx.fbcdn.net/v/t1.15752-9/76695139_934192943622917_2855665201821253632_n.png?_nc_cat=104&_nc_oc=AQmDaB_HKdKaJO_7g3gIgHKPmCRoQRoeKBffjMnaaTCrEic4oBewFBtmqmHh91I1fHA&_nc_ht=scontent-ort2-2.xx&oh=8ea34d5cbe4fd20c498fa203472486bb&oe=5E1AD3C0",
                "subtitle":"Seafood restaurant theme",
                "buttons":[
                {
                    "type":"postback",
                    "title":"Use theme 2!",
                    "payload":"template_2"
                }          
                ]      
            },
                
            {
            "title":"Jumbo Theme!",
            "image_url":"https://scontent.xx.fbcdn.net/v/t1.15752-0/p280x280/74890930_535592320349558_2024600939989565440_n.png?_nc_cat=110&_nc_oc=AQlFhQzythGi79yU5zJVe9hEsGIkTnvwPZFWg4w_hCALoBIVDJJlgcN6x0W8Eknmwt-ZNtyjoxGrIfIpY27-jmoU&_nc_ad=z-m&_nc_cid=0&_nc_zor=9&_nc_ht=scontent.xx&oh=032bc31a220f7e7e148b18fd6aca52d9&oe=5E177013",
            "subtitle":"Simplistic and elegant",
            "buttons":[
            {
                "type":"postback",
                "title":"Use theme 3!",
                "payload":"template_3"
            }          
            ]      
        }
            ]
        }
        }
    }
    }
    r = requests.post(url = API_ENDPOINT, data = json.dumps(tempData), headers={"Content-Type":"application/json"})
    return