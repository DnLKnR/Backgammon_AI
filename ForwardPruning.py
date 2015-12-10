'''Note: These will have to be modified for
node counting instead.  We can have cutting
off search do node counting instead of depth'''
import sys, random
class RandomForwardPruning:
    def __init__(self, alpha, beta, max_depth, ratio):
        self.alpha        = alpha
        self.beta         = beta
        self.max_depth    = max_depth
        self.ratio        = ratio
        
    def Search(self, state, player, diceroll):
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
        if self.Cuttoff_Test(state, depth + 1):
            value = state.score(self.player)
            return value
        v     = -100000
        v_max = -100000
        if diceroll == None:
            actions = state.actions(self.player, diceroll)
            for action in self.Random_Remove(actions):
                total_value = 0
                #print("All actions: " + str(actions))
                for die1 in range(len(action)):
                    for die2 in range(len(action[die1])):
                        print("test")
                        if len(action[die1][die2]) == 0:
                            continue
                        undo_actions = state.result(action[die1][die2], self.player)
                        value = self.Min_Value(state, alpha, beta, depth + 1)
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
                print("For Action = {0}, V is: {1}".format(action, total_value))
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
        if self.Cuttoff_Test(state, depth + 1):
            #Always produce score based off AI side
            value = state.score(self.player)
            return value
        v     = 100000
        #Produce the enemy's actions and remove a ratio of them
        actions = state.actions(self.enemy, None)
        for action in self.Random_Remove(actions):
            total_value = 0
            #loop through possible die rolls
            for die1 in range(len(action)):
                for die2 in range(len(action[die1])):
                    undo_actions = state.result(action[die1][die2], self.enemy)
                    value        = self.Max_Value(state, alpha, beta, depth + 1, None)
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
        count = self.Count_Actions(actions)
        moves = (count * self.ratio)//1
        #print("Before Random Remove: {0}".format(count))
        while moves > 0:
            try:
                index = random.randint(0,len(actions) - 1)
                die1 = random.randint(0,len(actions[index]) - 1)
                die2 = random.randint(0,len(actions[index][die1]) - 1)
                del actions[index][die1][die2]
                moves -= 1
                #print(actions[index][die1].pop(die2))
            except:
                #Random function error (due to invalid range)
                moves -= 1
                continue
        #count = self.Count_Actions(actions)
        #print("After Random Remove: {0}".format(count))
        return actions
    
    def Count_Actions(self, actions):
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
        for i,row in enumerate(array):
            for j,row2 in enumerate(row):
                print("------------- Dice Roll {0},{1} or {1},{0} -------------".format(i + 1,j + 1))
                for index,actionset in enumerate(row2):
                    print("Option {0}:\t{1}".format(index + 1,actionset))