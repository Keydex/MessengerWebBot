import globalVar

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