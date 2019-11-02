class user:
    def __init__(self, userID):
        self.userID = userID
        self.testvar = 'test'
        self.currState = 'initial'
        self.websites = []

    def updateState(self, newState):
        self.currState = newState

def resetState(state):
    state.clear()

def createUser(userID, state):
    state[userID] = user
    print('Create new user!')