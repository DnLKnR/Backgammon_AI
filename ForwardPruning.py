'''The RandomForwardPruning class acts as a wrapper for the
ForwardPruning algorithm implemented.  The random forward pruning
algorithms is constructed from the CuttingOff Search algorithm with
a special modification.  This modificaiton is that it chooses a ratio'd
amount of indexes to skip.  These indexes are selected at random'''
import sys, random

class RandomForwardPruning:
    def __init__(self, alpha, beta, max_depth, ratio):
        self.alpha        = alpha
        self.beta         = beta
        self.max_depth    = max_depth
        self.ratio        = ratio
        self.count        = 0
        
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
        v = self.Max_Value(state, self.alpha, self.beta, 0, diceroll)
        #Return the stored action from the search
        return self.action
            
    def Max_Value(self, state, alpha, beta, depth, diceroll):
        '''This function finds the action that leads to the overall
        best actions sets for the player'''
        self.count += 1
        if self.Cuttoff_Test(state, depth + 1):
            value = state.score(self.player)
            return value
        v     = -100000
        v_max = -100000
        if diceroll == None:
            actions = state.actions(self.player, diceroll)
            skip_index = self.Random_Remove(actions)
            for i,action in enumerate(actions): 
                total_value = 0
                for die1 in range(len(action)):
                    for die2 in range(len(action[die1])):
                        #Don't try to evaluate null indexes
                        if len(action[die1][die2]) == 0:
                            continue
                        #If the index is a skip_index, don't evaluate it
                        elif (i,die1,die2) in skip_index:
                            continue
                        undo_actions = state.result(action[die1][die2], self.player)
                        value = self.Min_Value(state, alpha, beta, depth + 1)
                        state.undo(undo_actions)
                        probability = 1/18
                        if die1 == die2:
                            probability = 1/36
                        total_value += probability * value
                
                v = max(v, total_value)
                if v >= beta:
                    return v
                alpha = max(alpha, v)
        else:
            die1,die2 = diceroll
            for action in state.actions(self.player, diceroll):
                undo_actions = state.result(action, self.player)
                total_value = self.Min_Value(state, alpha, beta, depth + 1)
                state.undo(undo_actions)
                #print("For Action = {0}, V is: {1}".format(action, total_value))
                v = max(v, total_value)
                
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
        if self.Cuttoff_Test(state, depth + 1):
            #Always produce score based off AI side
            value = state.score(self.player)
            return value
        v     = 100000
        #Produce the enemy's actions and remove a ratio of them
        actions = state.actions(self.enemy, None)
        skip_index = self.Random_Remove(actions)
        for i,action in enumerate(actions):
            total_value = 0
            #loop through possible die rolls
            for die1 in range(len(action)):
                for die2 in range(len(action[die1])):
                    #Don't try to evaluate null indexes
                    if len(action[die1][die2]) == 0:
                        continue
                    #If the index is a skip_index, don't evaluate it
                    elif (i,die1,die2) in skip_index:
                        continue
                    #Perform actions and get the resulting UNDO actions
                    undo_actions = state.result(action[die1][die2], self.enemy)
                    value        = self.Max_Value(state, alpha, beta, depth + 1, None)
                    #Use the undo actions to restore the state
                    state.undo(undo_actions)
                    probability = 1/18
                    if die1 == die2:
                        probability = 1/36
                    total_value += probability * value
            total_value *= (1/self.ratio)        
            v = min(v, total_value)
            
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
    
    def Random_Remove(self, actions):
        '''This function returns a list of random skip indices to be
        skipped in the actions.  The purpose of this function is to 
        trim down the search tree even further.'''
        count = self.Count_Actions(actions)
        moves = (count * self.ratio)//1
        skip_indexes = []
        #Store a random set of skip indices to help prune the search tree
        while moves > 0:
            for i in range(len(actions)):
                for j in range(len(actions[i])):
                    for k in range(len(actions[i][j])):
                        if moves == 0:
                            return skip_indexes
                        elif (i,j,k) in skip_indexes:
                            continue
                        elif not random.random()//self.ratio:
                            skip_indexes.append((i,j,k))
                            moves -= 1
            
       return skip_indexes
    
    def Count_Actions(self, actions):
        '''This function returns the number of actions
        that are in the actions multidimensional array.'''
        counter = 0
        for i in range(len(actions)):
            for j in range(len(actions[i])):
                for k in range(len(actions[i][j])):
                    counter += 1
        
        return counter  
    
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