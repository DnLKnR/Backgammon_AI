'''This class holds a state of the backgammon board as well
as operations that can be performed on the state'''

class State:
    def __init__(self, redBoard, whiteBoard):
        self.redBoard = redBoard
        self.whiteBoard = whiteBoard
        #The last action performed on the state
        self.action     = None
        
    def copy(self):
        '''creates a copy of this object'''
        copy_redBoard = list(self.redBoard)
        copy_whiteBoard = list(self.whiteBoard)
        
        return State(copy_redBoard, copy_whiteBoard)
    
    def evaluate(self, action, player):
        return self.result(action).score(player)
    
    def result(self, action):
        '''Returns a copy of the state with the action performed'''
        self.action = action
        pass
    
    def actions(self):
        '''Returns a list of all possible actions from this state'''
        pass
    
    def score(self, player):
        '''Computes/returns the score for the specified player (r or w)'''
        pass
    
    def isGameOver(self):
        '''returns true if the state is terminal (game over), else false'''
        pass