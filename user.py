import globalVar
class user:
    def __init__(self, userID):
        self.userID = userID
        self.testvar = 'test'
        self.currState = 'initial'
        self.websites = []

    def updateState(self, newState):
        self.currState = newState

def resetState():
    globalVar.userState.clear()

def createUser(userID):
    globalVar.userState[userID] = user
    print('Create new user!')