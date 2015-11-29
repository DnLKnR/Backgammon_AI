'''Note: These will have to be modified for
node counting instead.  We can have cutting
off search do node counting instead of depth'''

class CuttingOff:
    def __init__(self, initial, player, node_limit):
        self.initial = initial
        self.player  = player
        self.node_limit = node_limit
        self.node_count = 0
        
    def Search(self, state, nodes):
        #Reset the node count
        self.node_count = 0
        #Begin the minimax search
        v = self.Max_Value(state, -1, 193)
        #Need a way to return the action that results in v
        return None
            
    def Max_Value(self, state, alpha, beta):
        if self.Cuttoff_Test(state, nodes):
            return self.Utility(state)
        v = -1
        for action in self.Actions(state):
            #Increment the node count by 1 since this action is being evaluated
            self.node_count += 1
            v = max(v, self.Min_Value(self.Result(state, action), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
    
    def Min_Value(self, state, alpha, beta):
        if self.Cuttoff_Test(state):
            return self.Utility(state)
        v = 193
        for action in self.Actions(state):
            #Increment the node count by 1 since this action is being evaluated
            self.node_count += 1
            v = min(v, self.Max_Value(self.Result(state, action), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
    
    def Cuttoff_Test(self, state):
        '''returns true for all depth greater than some fixed depth of d
        OR if the state is terminal'''
        if self.node_limit < self.node_count:
            return True
        elif state.isGameOver():
            return True
        else:
            return False
    
    def Utility(self, state):
        '''this function assigns a value to a state, based on the
        player, which can be passed to this object at the start
        and checked via self.player'''
        return state.score(self.player)
    
    def Actions(self, state):
        '''this function returns a list of all possible
        actions that can be applied to a state'''
        return state.actions()
    
    def Result(self, state, action):
        '''This function returns a state with the action
        applied to it'''
        return state.result(action)