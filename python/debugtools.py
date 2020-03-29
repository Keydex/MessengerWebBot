from user import resetState
from helper import get_message, send_message
import globalVar

def middleWare(message, recipient_id, bot):
    if message['message'].get('text') == 'debug reset':
        resetState()
        send_message(recipient_id, 'Debug: Your State should now be reset!', bot)
        print('Resetting State')
        return True

    if message['message'].get('text') == 'debug toggle':
        if globalVar.locale == "cn":
            globalVar.locale = "en"
        elif globalVar.locale == "en":
            globalVar.locale = "cn"
        else:
            print("error")
        message = 'Debug' + 'Toggling Language To ' + globalVar.locale
        print(message)
        send_message(recipient_id, message, bot)
        return True

    return False