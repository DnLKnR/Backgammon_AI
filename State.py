'''This class holds a state of the backgammon board as well
as operations that can be performed on the state'''


class State:
    def __init__(self, redBoard, whiteBoard):
        self.redBoard   = redBoard
        self.whiteBoard = whiteBoard
        #The last action performed on the state
        self.action     = None
'''
Each index contains all possible actions for that dice roll.
Roll a 5 and a 3, then actions will be at ...[2][4]

rolls =    [[[1,1 or 1,1],[dup]       ,[dup]       ,[dup]       ,[dup]       ,[dup]       ],
            [[1,2 or 2,1],[2,2 or 2,2],[dup]       ,[dup]       ,[dup]       ,[dup]       ],
            [[1,3 or 3,1],[2,3 or 3,2],[3,3 or 3,3],[dup]       ,[dup]       ,[dup]       ],
            [[1,4 or 4,1],[2,4 or 4,2],[3,4 or 4,3],[4,4 or 4,4],[dup]       ,[dup]       ],
            [[1,5 or 5,1],[2,5 or 5,2],[3,5 or 5,3],[4,5 or 5,4],[5,5 or 5,5],[dup]       ],
            [[1,6 or 6,1],[2,6 or 6,2],[3,6 or 6,3],[4,6 or 6,4],[5,6 or 6,5],[6,6 or 6,6]]]

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
    
    def actions(self, player, diceroll):
        '''Returns a list of all possible actions from this state'''
        if diceroll == None:
            for die2 in range(1,7):
                for die1 in range(1, die2 + 1):
                    '''This weird looping order will allow for use to 
                       follow the desired setup for our matrix.
                       Ex. (die1,die2) == (1,1) then (2,1) then (2,2) then (3,1)....etc'''
                    
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
        else:
            # Higher index first
            die1,die2 = sorted(diceroll, reverse=True)
            
                
            
            pass
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