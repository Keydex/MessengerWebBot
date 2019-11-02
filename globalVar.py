import os
import json
# Store Conversation State here
userState = {}

locale = "en"

with open('locale.json') as json_file:
    localdata = json.load(json_file)