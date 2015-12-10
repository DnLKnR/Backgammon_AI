'''This one will be more difficult to implement.  At the simplest level,
we need to figure out some computable metric to decide if a route is going
nowhere so we can immediately prune it.  We will need to discuss how we want
to go about doing this.  This will be harder than implementing CuttingOff'''
    
class ForwardPruning:
    def __init__(self, alpha, beta, best_count):
        self.alpha      = alpha
        self.beta       = beta
        self.best_count = best_count
        
    def Search(self, state, player, diceroll):
        #Set attributes to store player index and enemy index for boards
        self.player = player
        self.enemy  = int(not player)
        #Reset action to None
        self.action = None
        #Begin the minimax search
        v = self.Max_Value(state, self.alpha, self.beta, diceroll)
        #Return the stored action from the search
        return self.action
            
    def Max_Value(self, state, alpha, beta, diceroll):
        if self.Terminal_Test(state):
            value = state.score(self.player)
            return value
        v     = -193
        v_max = -1000
        if diceroll == None:
            """actionss = state.actions(player, diceroll)
            self.printArray(actionss)"""
            value_actions = []
            for actions in state.actions(self.player, diceroll):
                total_value = 0
                #print("All actions: " + str(actions))
                for die1 in range(len(actions)):
                    for die2 in range(len(actions[die1])):
                        if len(actions[die1][die2]) == 0:
                            continue
                        value = state.evaluate(actions[die1][die2], self.player)
                        probability = 1/18
                        if die1 == die2:
                            probability = 1/36
                        value = probability * value
                        value_actions.append((value,actions[die1][die2]))
            value_actions = sorted(value_actions,key=lambda x: x[0], reverse=True)
            if len(value_actions) > self.best_count:
                value_actions = value_actions[:self.best_count + 1]
            for value, action in value_actions:
                undo_actions = state.result(action, self.player)
                value = self.Min_Value(state, alpha, beta)
                state.undo(undo_actions)
                v = max(v, total_value)
                if v >= beta:
                    return v
                alpha = max(alpha, v)
        else:
            value_actions = []
            die1,die2 = diceroll
            for actions in state.actions(self.player, diceroll):
                value = state.evaluate(actions, self.player)
                value_actions.append((value,actions))
            value_actions = sorted(value_actions,key=lambda x: x[0], reverse=True)
            if len(value_actions) > self.best_count:
                value_actions = value_actions[:self.best_count + 1]
            for value, action in value_actions:
                undo_actions = state.result(action, self.player)
                total_value = self.Min_Value(state, alpha, beta)
                state.undo(undo_actions)
                print("For Action = {0}, V is: {1}".format(action, total_value))
                v = max(v, total_value)
                if v >= beta:
                    self.action = action
                    return v
                elif v > v_max:
                    v_max = v
                    self.action = action
                    
                alpha = max(alpha, v)
            
        return v
    
    def Min_Value(self, state, alpha, beta):
        if self.Terminal_Test(state):
            #Always produce score based off AI side
            value = state.score(self.player)
            return value
        v     = 193
        value_actions = []
        for actions in state.actions(self.enemy, None):
            total_value = 0
            #print("All actions: " + str(actions))
            for die1 in range(len(actions)):
                for die2 in range(len(actions[die1])):
                    if len(actions[die1][die2]) == 0:
                        continue
                    value = state.evaluate(actions[die1][die2], self.enemy)
                    probability = 1/18
                    if die1 == die2:
                        probability = 1/36
                    value = probability * value
                    value_actions.append((value,actions[die1][die2]))
        value_actions = sorted(value_actions,key=lambda x: x[0])
        if len(value_actions) > self.best_count:
            value_actions = value_actions[:self.best_count + 1]
        #Produce the enemy's actions
        for value, action in value_actions:
            undo_actions = state.result(action, self.enemy)
            total_value  = self.Max_Value(state, alpha, beta, None)
            state.undo(undo_actions)
                    
            v = min(v, total_value)
            
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
    
    def Terminal_Test(self, state):
        '''returns true for all nodes greater than some fixed nodes limit
        OR if the state is terminal'''
        if state == None:
            print("In Cutoff_Test: State is of NoneType, returning True")
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