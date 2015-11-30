'''This class holds a state of the backgammon board as well
as operations that can be performed on the state'''


class State:
    def __init__(self, redBoard, whiteBoard):
        self.redBoard   = redBoard
        self.whiteBoard = whiteBoard
        #The last action performed on the state
        self.action     = None
'''
rolls =    [[1,1 or 1,1],[1,2 or 2,1],[1,3 or 3,1],[1,4 or 4,1],[1,5 or 5,1],[1,6 or 6,1],
            [dup]       ,[2,2 or 2,2],[2,3 or 3,2],[2,4 or 4,2],[2,5 or 5,2],[2,6 or 6,2],
            [dup]       ,[dup]       ,[3,3 or 3,3],[3,4 or 4,3],[3,5 or 5,3],[3,6 or 6,3],
            [dup]       ,[dup]       ,[dup]       ,[4,4 or 4,4],[4,5 or 5,4],[4,6 or 6,4],
            [dup]       ,[dup]       ,[dup]       ,[dup]       ,[5,5 or 5,5],[5,6 or 6,5],
            [dup]       ,[dup]       ,[dup]       ,[dup]       ,[dup]       ,[6,6 or 6,6]]
'''
    def get(self, player):
        if player.lower() == 'r':
            return self.redBoard
        elif player.lower() == 'w':
            return self.whiteBoard
        else:
            return None
    
    def copy(self):
        '''creates a copy of this object'''
        copy_redBoard = list(self.redBoard)
        copy_whiteBoard = list(self.whiteBoard)
        return State(copy_redBoard, copy_whiteBoard)
    
    def evaluate(self, action, player):
        return self.result(action).score(player)
    
    def result(self, action, player):
        '''Returns a copy of the state with the action performed'''
        copy_state = self.copy()
        board = copy_state.get(player)
        for move in action:
            i,j          = move
            board[i]     -= 1
            board[i + j] += 1
        
        return copy_state
    
    def actions(self, player):
        '''Returns a list of all possible actions from this state'''
        for die1 in range(1,7):
            for die2 in range(die1,7):
                pass
        '''
                if player has pieces in bar
                    only generate moves from bar
                actionList = []
                else
                    move1 = null
                    for each space in board
                        if piece can be moved with dice roll 1
                            move1 = move
                            
                            move2 = null
                            for each space in board
                                if piece can be moved with dice roll 2
                                    move2 = move
                                    
                                    actionList.append((move1, move2))
                            
                            
                            
                
        '''
        
        pass
    
    def score(self, player):
        '''Computes/returns the score for the specified player (r or w)'''
        pass
    
    def isGameOver(self):
        '''returns true if the state is terminal (game over), else false'''
        pass
    
    def rollDice(self):
        self.diceRolls[0] = Random.randint(1,6)
        self.diceRolls[1] = Random.randint(1,6)
        return