'''This class holds a state of the backgammon board as well
as operations that can be performed on the state'''


class State:
    def __init__(self, redBoard, whiteBoard):
        self.redBoard   = redBoard
        self.whiteBoard = whiteBoard
        self.boards = [redBoard, whiteBoard]
        #The last action performed on the state
        self.action     = None

    
    '''
    Each index contains all possible actions for that dice roll.
    Roll a 5 and a 3, then actions will be at ...[2][4]

    rolls =    [
                [[1,1 or 1,1]],
                [[1,2 or 2,1],[2,2 or 2,2]],
                [[1,3 or 3,1],[2,3 or 3,2],[3,3 or 3,3]],
                [[1,4 or 4,1],[2,4 or 4,2],[3,4 or 4,3],[4,4 or 4,4]],
                [[1,5 or 5,1],[2,5 or 5,2],[3,5 or 5,3],[4,5 or 5,4],[5,5 or 5,5]],
                [[1,6 or 6,1],[2,6 or 6,2],[3,6 or 6,3],[4,6 or 6,4],[5,6 or 6,5],[6,6 or 6,6]]
               ]

    '''

    def get(self, player):
        return self.boards[player]
    
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
            if len(move) != 2:
                print(action)
                continue
            i,j          = move
            board[i]     -= 1
            board[j]     += 1
        copy_state.action = action
        
        return copy_state
    
    def actions(self, player, diceroll):
        '''Returns a list of all possible actions from this state'''

        boards = [self.redBoard,self.whiteBoard]
        #Store all actions
        all_actions  = initializeActionsArray()
        #If a dice roll isn't given
        if diceroll == None:
            for die1 in range(1,7):
                for first_action in self.moves(die1, boards, player):
                #first_actions = self.moves(die1, boards, player_index)
                    for die2 in range(1,7):
                    #for first_action in first_actions:
                        ''' Apply first action to the board(s) '''
                        #print("Before Action:\t{0}".format(boards[player_index]))
                        undo_actions = self.do(first_action, boards, player)
                        #print("After Action:\t{0}".format(boards[player_index]))
                        ''' Get the second actions '''
                        second_actions = self.moves(die2, boards, player)
                        if(len(second_actions) == 0):
                            all_actions[max(die1,die2) - 1][min(die1,die2) - 1].append([first_action,(0,0)])
                        ''' Store the action set '''
                        for second_action in second_actions:
                            all_actions[max(die1,die2) - 1][min(die1,die2) - 1].append([first_action,second_action])
                        ''' Undo first_action to the board(s) '''
                        self.undo(undo_actions, boards)
                        #print("After Undo:\t{0}".format(boards[player_index]))

        #if a dice roll is provided
        else:
            die1,die2     = diceroll
            first_actions = self.moves(die1, boards, player)
            for first_action in first_actions:
                ''' Apply first action to the board(s) '''
                #print("Before Action:\t{0}".format(boards[player_index]))
                undo_actions = self.do(first_action, boards, player)
                #print("After Action:\t{0}".format(boards[player_index]))
                ''' Get the second actions '''
                second_actions = self.moves(die2, boards, player)
                ''' Store the action set '''
                for second_action in second_actions:
                    all_actions[max(die1,die2) - 1][min(die1,die2) - 1].append([first_action,second_action])
                ''' Undo first_action to the board(s) '''
                self.undo(undo_actions, boards)
                #print("After Undo:\t{0}".format(boards[player_index]))
        return all_actions
    
    
    def moves(self, die, boards, player_index):
        '''Given a single die roll, generate possible actions'''
        enemy_index  = int(not player_index)
        moves_list   = []
         #bar not empty
        if (boards[player_index][0] >= 1):
            #if move allowed
            if player_index == 0:
                if (boards[enemy_index][25 - die] <= 1):
                    moves_list.append((0, 25 - die))
                
            elif player_index == 1:
                if (boards[enemy_index][die] <= 1):
                    moves_list.append((0, die))
        else:
            for i in range (1, 25):
                #if white can move from index i with die2
                if player_index == 0:
                    if (boards[player_index][i] > 0 and i + die < 24 and boards[enemy_index][i + die] < 2):
                        j = i + die
                        if j > 24:
                            continue
                        moves_list.append((i, j))
                if player_index == 1:
                    if (boards[player_index][i] > 0 and i - die > 0 and boards[enemy_index][i - die] < 2):
                        j = i - die
                        if j < 1:
                            continue
                        moves_list.append((i, j))
        return moves_list
    
    def do(self, move, boards, player_index):
        '''This function executes an action and returns a list of action necessary to undo it'''
        enemy_index  = int(not player_index)
        undos = []
        i,j  = move
        #make sure we don't go back last index
        #if (player_index == 0):
        #    index = i + j
        #    if index < 1 or index > 24:
        #        return undos
        #else:
        #    index = i - j
        #    if index < 1 or index > 24:
        #        return undos
                
        boards[player_index][j]  += 1
        boards[player_index][i]      -= 1
        undos.append((j,i,player_index))
        #If enemy player has a piece there, put them on bar
        if boards[enemy_index][j] == 1:
            #Remove from the old piece index
            boards[enemy_index][j] -= 1
            #Add to the new piece index, (the bar)
            boards[enemy_index][0] += 1
            #Provide undo tuple, (new index, old index, board index)
            undos.append((0,j,enemy_index))
        #return the special formatted actions
        return undos
    
    def undo(self, moves, boards):
        for move in moves:
            new,old,board  = move
            #Remove from the new piece index
            boards[board][new]  -= 1
            #Place back onto the old piece index
            boards[board][old]  += 1
    
    def score(self, boards, player_index):
        '''Computes/returns the score for the specified player's board (r or w)'''
        
        barConst = 5
        doorConst = 1
        
        enemy_index = int(not player_index)
        scores = [0,0]
    
        '''Increase score if enemy has pieces on bar'''
        scores[0] += boards[1][0] * barConst
        scores[1] += boards[0][0] * barConst
        
        for index in range(1, 25):
            '''
            scores[0] += index * boards[0][index]
            scores[1] += (25 - index) * boards[1][index]
            '''
            
            '''Increase score if pieces are doored (stacked)'''
            if boards[0][index] > 1:
                scores[0] += doorConst
                
            if boards[1][index] > 1:
                scores[1] += doorConst
                
                
        
        value =  scores[enemy_index] - scores[player_index]
        
        return value
    
    def isGameOver(self):
        '''returns true if the state is terminal (game over), else false'''
        redWon = True
        for i in range(24):
            if self.redBoard[i] > 0:
                redWon = False
                break
        if redWon:
            print("Red wins!")
            return True
            
        whiteWon = True
        for i in range(24):
            if self.whiteBoard[i] > 0:
                whiteWon = False
                break
        if whiteWon:
            print("White wins!")
            return True

def initializeActionsArray():
    array = [[[] for i in range(1, j + 1)] for j in range(1, 7)]
    return array
    
