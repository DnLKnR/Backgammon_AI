'''Note: These will have to be modified for
node counting instead.  We can have cutting
off search do node counting instead of depth'''

class CuttingOff:
    def __init__(self, initial, player, max_depth):
        self.initial = initial
        self.player  = player
        self.max_depth = max_depth
        self.action = None
        #self.node_limit = node_limit
        #self.node_count = 0
        #self.diceroll   = [0,0]
        
    def Search(self, state, diceroll):
        #Reset the node count
        self.node_count = 0
        #Begin the minimax search
        v = self.Max_Value(state, -193, 193, 0, diceroll)
        #Need a way to return the action that results in v
        return v
            
    def Max_Value(self, state, alpha, beta, depth, diceroll):
        if self.Cuttoff_Test(state, depth + 1):
            return self.Utility(state)
        v = -193
        
        
        if diceroll == None:
            for actions in self.Actions(state, diceroll):
                count = 0
                total_v = 0
                #print("All actions: " + str(actions))
                for die1 in range(len(actions)):
                    for die2 in range(len(actions[die1])):
                        temp = self.Min_Value(self.Result(state, actions[die1][die2]), alpha, beta, depth + 1)
                        total_v += (1/18) * temp
                #Increment the node count by 1 since this action is being evaluated
                #self.node_count += 1
                v = max(v, total_v)
                #v,action = max([v], self.Min_Value(self.Result(state, action), alpha, beta, depth + 1), key=lambda x: x[0])
                if v >= beta:
                    return v
                alpha = max(alpha, v)
        else:
            die1,die2 = diceroll
            for actions in self.Actions(state, diceroll)[max(die1,die2) - 1][min(die1,die2) - 1]:
                print("Action return from roll: " + str(actions))
                total_v = self.Min_Value(self.Result(state, actions), alpha, beta, depth + 1)
                #total_v += temp
                #Increment the node count by 1 since this action is being evaluated
                #self.node_count += 1
                v = max(v, total_v)
                #v,action = max([v], self.Min_Value(self.Result(state, action), alpha, beta, depth + 1), key=lambda x: x[0])
                if v >= beta:
                    self.action = actions
                    return v
                alpha = max(alpha, v)
            
        return v
    
    def Min_Value(self, state, alpha, beta, depth):
        if self.Cuttoff_Test(state, depth + 1):
            return self.Utility(state)
        v = 193
        for actions in self.Actions(state, None):
            count = 0
            total_v = 0
            for die1 in range(len(actions)):
                for die2 in range(len(actions[die1])):
                    temp = self.Max_Value(self.Result(state, actions[die1][die2]), alpha, beta, depth + 1, None)
                    total_v += (1/18) * temp
            #Increment the node count by 1 since this action is being evaluated
            v = min(v, total_v)
            #self.node_count += 1
            #v,a = min([v], self.Max_Value(self.Result(state, action), alpha, beta, depth + 1, None), key=lambda x: x[0])
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
    
    def Utility(self, state):
        '''this function assigns a value to a state, based on the
        player, which can be passed to this object at the start
        and checked via self.player'''
        player_index = int(self.player == "w")
        return state.score([state.redBoard,state.whiteBoard], player_index)
    
    def Actions(self, state, diceroll):
        '''this function returns a list of all possible
        actions that can be applied to a state'''
        return state.actions(self.player, diceroll)
    
    def Result(self, state, action):
        '''This function returns a state with the action
        applied to it'''
        return state.result(action, self.player)


class Node:
    def __init__(self, state, value, actions, parent):
        self.state   = state
        self.value   = value
        self.actions = actions
        self.parent  = parent
        


''' If we are node counting, we might have to convert this search to BFS...
    it's not the best, but it seems to be the only way...'''
class MiniMaxBFS:
    def __init__(self, node_limit):
        self.node_limit = node_limit
    
    def Search(self, state, diceroll, player):
        self.node_count = 0
        Min_Queue = []
        Max_Queue = []
        value = 0
        next_actions = state.actions(player, diceroll)
        for index,action in enumerate(next_actions):
            new_state = state.result(action, player)
            actions   = new_state.actions(player, diceroll)
            value     = value + new_state.score(player)
            Min_Queue.append(Node(new_state, actions, value, index))
            self.node_count += 1
            
        ply = 0
        
        while self.node_count < self.node_limit:
            while len(Min_Queue) > 0 and self.node_count < self.node_limit:
                node = Min_Queue.pop(0)
                for action in node.actions:
                    new_state = node.state.result(action, player)
                    actions   = new_state.actions(player, None)
                    value     = node.value - new_state.score(player)
                    Min_Queue.append(Node(new_state, actions, value, node.parent))
                    self.node_count += 1
                '''Push new actions into Min_Queue'''
                '''Min_Queue.push(Node(new_state, value, actions))'''
                pass
            
            ply += 1
            
            while len(Max_Queue) > 0 and self.node_count < self.node_limit:
                node = Max_Queue.pop(0)
                for action in node.actions:
                    new_state = node.state.result(action, player)
                    actions   = new_state.actions(player, None)
                    value     = node.value + new_state.score(player)
                    Min_Queue.append(Node(new_state, actions, value, node.parent))
                    self.node_count += 1
                '''Push new actions into Min_Queue'''
                '''Min_Queue.push(Node(new_state, value, actions))'''
                
                pass
            
        action_index = self.computeBestState(Max_Queue + Min_Queue, next_actions)
        
        
                
        #sorted(Max_Queue, key=lambda x: x.value)
    def computeBestState(self, queue, actions):
        sorted(queue, key=lambda x: x.parent)
        next_values = []
        count = 0
        length = len(queue)
        for i in range(len(actions)):
            value = 0
            for j in range(count,length):
                if queue[j].parent != i:
                    next_values.append(value/(j - count))
                else:
                    count += 1
                    value += queue[j].value
        maxv = -100000000
        action_index = 0
        for i in range(len(actions)):
            if maxv < value[i]:
                maxv = value[i]
                action_index = i
        
        return action_index