import globalVar
class user:
    def __init__(self, userID):
        self.userID = userID
        self.testvar = 'test'
        self.currState = 'initial'
        self.websites = []
        self.websiteName = ''
        self.slogan = ''
        self.slogan2 = "Another Text"
        self.address = ''
        self.phoneNumber = ''
        self.email = ''

    def updateState(self, newState):
        self.currState = newState

def resetState():
    globalVar.userState.clear()

def createUser(userID):
    globalVar.userState[userID] = user(userID)
    print('Create new user!')