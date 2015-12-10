'''Note: These will have to be modified for
node counting instead.  We can have cutting
off search do node counting instead of depth'''
import sys
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
            for actions in self.Random_Remove(state.actions(self.player, diceroll)):
                total_value = 0
                #print("All actions: " + str(actions))
                for die1 in range(len(actions)):
                    for die2 in range(len(actions[die1])):
                        if len(actions[die1][die2]) == 0:
                            continue
                        undo_actions = state.result(actions[die1][die2], self.player)
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
        v     = 10000
        #Produce the enemy's actions and remove a ratio of them
        for actions in self.Random_Remove(state.actions(self.enemy, None)):
            total_value = 0
            #loop through possible die rolls
            for die1 in range(len(actions)):
                for die2 in range(len(actions[die1])):
                    undo_actions = state.result(actions[die1][die2], self.enemy)
                    value        = self.Max_Value(state, alpha, beta, depth + 1, None)
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
    
    def Random_Remove(self, actions):
        counter = 0
        for i in range(actions):
            for j in range(actions[i]):
                for k in range(actions[i][j]):
                    counter += 1
        moves = (counter * self.ratio)//1
        print("Before Random Remove: {0}".format(actions))
        while moves > 0:
            index = random.randint(0,len(actions) - 1)
            die1 = random.randint(0,len(actions[index]) - 1)
            die2 = random.randint(0,len(actions[index][die1]) - 1)
            actions[index][die1].pop(die2)
            moves -= 1
        print("After Random Remove: {0}".format(actions))
        sys.exit(1)
        return actions
            
    
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