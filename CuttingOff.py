'''Note: These will have to be modified for
node counting instead.  We can have cutting
off search do node counting instead of depth'''

class CuttingOff:
    def __init__(self, initial, player, node_limit):
        self.initial = initial
        self.player  = player
        self.node_limit = node_limit
        self.node_count = 0
        
    def Search(self, state):
        #Reset the node count
        self.node_count = 0
        #Begin the minimax search
        v,action = self.Max_Value(state, -1, 193)
        #Need a way to return the action that results in v
        return action
            
    def Max_Value(self, state, alpha, beta):
        if self.Cuttoff_Test(state):
            return [self.Utility(state),state.action]
        v = -1
        for action in self.Actions(state):
            #Increment the node count by 1 since this action is being evaluated
            self.node_count += 1
            v = max([v], self.Min_Value(self.Result(state, action), alpha, beta), key=lambda x: x[0])
            if v >= beta:
                return [v,action]
            alpha = max(alpha, v)
        return [v,None]
    
    def Min_Value(self, state, alpha, beta):
        if self.Cuttoff_Test(state):
            return [self.Utility(state),state.action]
        v = 193
        for action in self.Actions(state):
            #Increment the node count by 1 since this action is being evaluated
            self.node_count += 1
            v = min([v], self.Max_Value(self.Result(state, action), alpha, beta), key=lambda x: x[0])
            if v <= alpha:
                return [v,action]
            beta = min(beta, v)
        return [v,None]
    
    def Cuttoff_Test(self, state):
        '''returns true for all nodes greater than some fixed nodes limit
        OR if the state is terminal'''
        if state == None:
            print("In Cutoff_Test: State is of NoneType, returning True")
            return True
        elif self.node_limit < self.node_count:
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
