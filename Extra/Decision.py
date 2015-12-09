
'''This class is the very basic Minimax algorithm provided in the book.
We will obviously be implementing the alpha-beta pruning minimax algorithm
for our project, but it might be good start off with atleast a simple
algorithm for testing and experimentation.  I will set up the alpha-beta
pruning template next.'''

class Decision:
    def __init__(self, initial, player):
        self.initial = initial
        self.player  = player
    
    def Minimax(self, state):
        v = -1
        for action in self.Actions(state):
            v = max(v, self.Min_Value(self.Result(state, action)))
        return v
    
    def Max_Value(self,state):
        if self.Terminal_Test(state):
            return self.Utility(state)
        v = -1
        for action in self.Actions(state):
            v = min(v, self.Min_Value(self.Result(state, action)))
        return v
        
    def Min_Value(self,state):
        if self.Terminal_Test(state):
            return self.Utility(state)
        v = 193
        for action in self.Actions(state):
            v = min(v, self.Max_Value(self.Result(state, action)))
        return v
    
    def Actions(self, state):
        '''Returns the set of legal moves in a state. A move can
        represented whichever way seems fit.  This function will return
        the list of all those moves which can be applied to the state.'''
        return state.actions()
    
    def Terminal_Test(self, state):
        '''Returns true is the game is over based on the state,
        otherwise this function returns false. States where the
        game has ended are known as terminal states.'''
        return state.isGameOver()
    
    def Result(self, state, action):
        '''Transitional model which returns the 
        result of making that action on the state'''
        return state.result(action)
    
    def Utility(self, state, player):
        '''this function defines a numeric value for a game.  
        Note: in the book, this function sometimes includes an 
        extra parameter "p", which is the defined player.  The 
        book states that backgammon has payoff ranges from 0 to 
        +192.'''
        return state.score(player)