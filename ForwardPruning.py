'''This one will be more difficult to implement.  At the simplest level,
we need to figure out some computable metric to decide if a route is going
nowhere so we can immediately prune it.  We will need to discuss how we want
to go about doing this.  This will be harder than implementing CuttingOff'''
    
class ForwardPruning:
    def __init__(self, initial, player):
        self.initial = initial
        self.player  = player
    
    def Search(self,state):
        v = self.Max_Value(state, -1, -1)
        for action in self.Actions(state):
            if action.value(v):
                return action
        return None
            
    def Max_Value(self, state, alpha, beta):
        if self.Probcut_Test(state):
            return self.Utility(state)
        v = -1
        for action in self.Actions(state):
            v = max(v, self.Min_Value(self.Result(state, action), alpha, beta))
            if v >= beta:
                return v
            a = max(alpha, v)
        return v
    
    def Min_Value(self, state, alpha, beta):
        if self.Probcut_Test(state):
            return self.Utility(state)
        v = -1
        for action in self.Actions(state):
            v = min(v, self.Max_Value(self.Result(state, action), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
    
    def Probcut_Test(self, state): #, alpha, beta):
        '''returns true for all depth greater than some fixed depth of d'''
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