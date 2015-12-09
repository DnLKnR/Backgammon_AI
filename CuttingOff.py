'''Note: These will have to be modified for
node counting instead.  We can have cutting
off search do node counting instead of depth'''

class CuttingOff:
    def __init__(self, alpha, beta, max_depth):
        self.alpha   = alpha
        self.beta    = beta
        self.max_depth = max_depth
        self.action = None
        
    def Search(self, state, player, diceroll):
        #Begin the minimax search
        v = self.Max_Value(state, self.alpha, self.beta, 0, player, diceroll)
        #Need a pick best first move if self.action is still Null...
        
        
        #Need a way to return the action that results in v
        return self.action
            
    def Max_Value(self, state, alpha, beta, depth, player, diceroll):
        if self.Cuttoff_Test(state, depth + 1):
            value = state.score(player)
            return value
        v = -193
        enemy  = int(not player)
        if diceroll == None:
            """actionss = state.actions(player, diceroll)
            self.printArray(actionss)"""
            for actions in state.actions(player, diceroll):
                
                total_value = 0
                #print("All actions: " + str(actions))
                for die1 in range(len(actions)):
                    for die2 in range(len(actions[die1])):
                        undo_actions = state.result(actions[die1][die2], player)
                        temp = self.Min_Value(state, alpha, beta, depth + 1, enemy)
                        state.undo(undo_actions)
                        total_value += (1/18) * temp
                #Increment the node count by 1 since this action is being evaluated
                #self.node_count += 1
                v = max(v, total_value)
                #v,action = max([v], self.Min_Value(self.Result(state, action), alpha, beta, depth + 1), key=lambda x: x[0])
                if v >= beta:
                    return v
                alpha = max(alpha, v)
        else:
            die1,die2 = diceroll
            actions = state.actions(player, diceroll)
            for action in actions:
                print("Action return from roll: " + str(action))
                undo_actions = state.result(action, player)
                total_value = self.Min_Value(state, alpha, beta, depth + 1, enemy)
                state.undo(undo_actions)
                
                v = max(v, total_value)
                print("New V is: " + str(v))
                #v,action = max([v], self.Min_Value(self.Result(state, action), alpha, beta, depth + 1), key=lambda x: x[0])
                if v >= beta:
                    self.action = action
                    return v
                alpha = max(alpha, v)
            
        return v
    
    def Min_Value(self, state, alpha, beta, depth, player):
        if self.Cuttoff_Test(state, depth + 1):
            value = state.score(player)
            return value
        v     = 193
        enemy = int(not player)
        for actions in state.actions(player, None):
            total_value = 0
            for die1 in range(len(actions)):
                for die2 in range(len(actions[die1])):
                    undo_actions = state.result(actions[die1][die2], player)
                    value        = self.Max_Value(state, alpha, beta, depth + 1, enemy, None)
                    state.undo(undo_actions)
                    total_value += (1/18) * value
                    
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
        for i,row in enumerate(array):
            for j,row2 in enumerate(row):
                print("------------- Dice Roll {0},{1} or {1},{0} -------------".format(i + 1,j + 1))
                for index,actionset in enumerate(row2):
                    print("Option {0}:\t{1}".format(index + 1,actionset))
