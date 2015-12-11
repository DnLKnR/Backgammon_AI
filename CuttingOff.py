'''The CuttingOff class acts as a wrapper for the
CuttingOff Search algorithm implemented.  The CuttingOff Search
algorithm is constructed from the Alpha-Beta Search algorithm with
a special modification.  This modificaiton is that it chooses a depth
at which to stop searching in the tree.  The purpose of this is to
speed up evaluation time.'''

class CuttingOff:
    def __init__(self, alpha, beta, max_depth):
        self.alpha   = alpha
        self.beta    = beta
        self.max_depth = max_depth
        self.count  = 0
        
    def Search(self, state, player, diceroll):
        '''This function serves as the entry point for the Min-Max value
        recursion search.  This function instantiates/resets values that
        will be used throughout the recursion'''
        #Set attributes to store player index and enemy index for boards
        self.player = player
        self.enemy  = int(not player)
        #Reset action to None
        self.action = None
        #Begin the minimax search
        v = self.Max_Value(state, self.alpha, self.beta, 1, diceroll)
        #Return the stored action from the search
        return self.action
            
    def Max_Value(self, state, alpha, beta, depth, diceroll):
        '''This function finds the action that leads to the overall
        best actions sets for the player'''
        self.count += 1
        if self.Cuttoff_Test(state, depth):
            value = state.score(self.player)
            return value
        v     = -100000
        v_max = -100000
        if diceroll == None:
            for actions in state.actions(self.player, diceroll):
                total_value = 0
                for die1 in range(len(actions)):
                    for die2 in range(len(actions[die1])):
                        if len(actions[die1][die2]) == 0:
                            continue
                        #Perform actions and get the resulting UNDO actions
                        undo_actions = state.result(actions[die1][die2], self.player)
                        value = self.Min_Value(state, alpha, beta, depth + 1)
                        #Use the undo actions to restore the state
                        state.undo(undo_actions)
                        probability = 1/18
                        if die1 == die2:
                            probability = 1/36
                        total_value += probability * value
                #Increment the node count by 1 since this action is being evaluated
                #self.node_count += 1
                v = max(v, total_value)
                #v,action = max([v], self.Min_Value(self.Result(state, action), alpha, beta, depth + 1), key=lambda x: x[0])
                if v >= beta:
                    return v
                alpha = max(alpha, v)
        else:
            die1,die2 = diceroll
            for action in state.actions(self.player, diceroll):
                undo_actions = state.result(action, self.player)
                total_value = self.Min_Value(state, alpha, beta, depth + 1)
                state.undo(undo_actions)
                v = max(v, total_value)
                
                #v,action = max([v], self.Min_Value(self.Result(state, action), alpha, beta, depth + 1), key=lambda x: x[0])
                if v >= beta:
                    self.action = action
                    return v
                elif v > v_max:
                    v_max = v
                    self.action = action
                    
                alpha = max(alpha, v)
            
        return v
    
    def Min_Value(self, state, alpha, beta, depth):
        '''This function attempts to find the enemy's moves
        by minimizing the player's score.'''
        self.count += 1
        if self.Cuttoff_Test(state, depth):
            #Always produce score based off AI side
            value = state.score(self.player)
            return value
        v     = 10000
        #Produce the enemy's actions
        for actions in state.actions(self.enemy, None):
            total_value = 0
            for die1 in range(len(actions)):
                for die2 in range(len(actions[die1])):
                    #Perform actions and get the resulting UNDO actions
                    undo_actions = state.result(actions[die1][die2], self.enemy)
                    value        = self.Max_Value(state, alpha, beta, depth + 1, None)
                    #Use the undo actions to restore the state
                    state.undo(undo_actions)
                    probability = 1/18
                    if die1 == die2:
                        probability = 1/36
                    total_value += probability * value
                    
            v = min(v, total_value)
            
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
    
    def Cuttoff_Test(self, state, depth):
        '''returns true for all nodes greater than some fixed nodes limit
        OR if the state is terminal'''
        if state == None:
            print("In Cutoff_Test: State is of NoneType, returning True")
            return True
        elif depth > self.max_depth:
            return True
        elif state.isGameOver():
            return True
        else:
            return False
        
    def printArray(self, array):
        '''Special actions array print function for debugging purposes'''
        for i,row in enumerate(array):
            for j,row2 in enumerate(row):
                print("------------- Dice Roll {0},{1} or {1},{0} -------------".format(i + 1,j + 1))
                for index,actionset in enumerate(row2):
                    print("Option {0}:\t{1}".format(index + 1,actionset))
