'''This is the template for the minimax with alpha-beta
pruning.  this is closer the actual search that we have
to implement.  However, there would still be some other
altercations that would have to be made.  Also, there
is probably optimizations that we can to this since it
seems like the base algorithm is going to involve a lot
of state copying.'''


class AlphaBeta:
    def __init__(self, initial, player):
        self.initial = initial
        self.player  = player
    
    def Search(self,state):
        v = self.Max_Value(state, -1, -1)
        for action in self.Actions(state):
            if action.value(v):
                return action
            
    def Max_Value(self, state, alpha, beta):
        if self.Terminal_Test(state):
            return self.Utility(state)
        v = -1
        for action in self.Actions(state):
            v = max(v, self.Min_Value(self.Result(state, action), alpha, beta))
            if v >= beta:
                return v
            a = max(alpha, v)
        return v
    
    def Min_Value(self, state, alpha, beta):
        if self.Terminal_Test(state):
            return self.Utility(state)
        v = 193
        for action in self.Actions(state):
            v = min(v, self.Max_Value(self.Result(state, action), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
    
    def Terminal_Test(self, state):
        '''returns true if the game is over, otherwise return
        false'''
        pass
    
    def Utility(self, state):
        '''this function assigns a value to a state, based on the
        player, which can be passed to this object at the start
        and checked via self.player'''
        pass
    
    def Actions(self, state):
        '''this function returns a list of all possible
        actions that can be applied to a state'''
        pass
    
    def Result(self, state, action):
        '''This function returns a state with the action
        applied to it'''
        pass
    
    def Player(self, state):
        '''decides which player has the move on the current
        state.  We can probably figure out a different way
        of doing this'''
        pass
    
    