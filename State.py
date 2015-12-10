'''This class holds a state of the backgammon board as well
as operations that can be performed on the state'''


class State:
    def __init__(self, redBoard, whiteBoard):
        self.redBoard   = redBoard
        self.whiteBoard = whiteBoard
        self.boards = [self.redBoard, self.whiteBoard]
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
        undo_actions = self.result(action, player)
        value        = self.score(player)
        self.undo(undo_actions)
        return value
    
    def result(self, action, player):
        '''Returns a list of actions necessary to undo the action performed'''
        undos = []
        enemy  = int(not player)
        for move in action:
            i,j  = move
            if j != -1:
                self.boards[player][j]  += 1
            
            self.boards[player][i]  -= 1
            undos.append((j,i,player))
            #If enemy player has a piece there, put them on bar
            if self.boards[enemy][j] == 1 and j != -1:
                #Remove from the old piece index
                self.boards[enemy][j] -= 1
                #Add to the new piece index, (the bar)
                self.boards[enemy][0] += 1
                #Provide undo tuple, (new index, old index, board index)
                undos.append((0,j,enemy))
        
        #return the special formatted actions
        return undos
    
    def actions(self, player, diceroll):
        '''Returns a list of all possible actions from this state'''
        #If a dice roll isn't given
        if diceroll == None:
            #Store all actions
            all_actions  = self.initializeActionsArray()
            for die1 in range(1,7):
                for first_action in self.moves(die1, player):
                #first_actions = self.moves(die1, boards, player_index)
                    #print("Before Action:\t{0}".format(boards[player_index]))
                    ''' Apply first action to the board(s) '''
                    undo_actions = self.do(first_action, player)
                    #print("After Action:\t{0}".format(boards[player_index]))
                    for die2 in range(1,7):
                        ''' Get the second actions '''
                        second_actions = self.moves(die2, player)
                        if(len(second_actions) == 0):
                            all_actions[max(die1,die2) - 1][min(die1,die2) - 1].append([first_action,(0,0)])
                        ''' Store the action set '''
                        for second_action in second_actions:
                            all_actions[max(die1,die2) - 1][min(die1,die2) - 1].append([first_action,second_action])
                            
                    ''' Undo first_action to the board(s) '''
                    self.undo(undo_actions)
                    #print("After Undo:\t{0}".format(boards[player_index]))
            return all_actions
        #if a dice roll is provided
        else:
            actions       = []
            die1,die2     = diceroll
            ''' loop through first actions '''
            for first_action in self.moves(die1, player):
                ''' Apply first action to the board(s) '''
                #print("Before Action:\t{0}".format(boards[player_index]))
                undo_actions = self.do(first_action, player)
                #print("After Action:\t{0}".format(boards[player_index]))
                ''' Get second actions and store the action set '''
                for second_action in self.moves(die2, player):
                    actions.append([first_action,second_action])
                ''' Undo first_action to the board(s) '''
                self.undo(undo_actions)
                #print("After Undo:\t{0}".format(boards[player_index]))
            return actions
    
    
    def moves(self, die, player):
        '''Given a single die roll, generate possible actions'''
        enemy  = int(not player)
        moves_list   = []
         #bar not empty
        if (self.boards[player][0] >= 1):
            j = die
            if player == 1:
                j = 25 - die
            #if move allowed
            if (self.boards[enemy][j] <= 1):
                moves_list.append((0, j))
        
        elif self.isBearingOff(player):
            if player == 0:
                player_name = "Red"
            else:
                player_name = "White"
            print("{0} Player can now Bear off...".format(player_name))
            
            
            if player == 0:
                i = 25 - die
                #if red has a piece at that location, they can remove it
                if self.boards[player][i] > 0:
                    moves_list.append((i, -1))
            
            elif player == 1:
                i = die
                if self.boards[player][i] > 0:
                    moves_list.append((i, -1))
            
            else:
                print("Error: Invalid player index")    
            
        
        else:
            for i in range (1, 25):
                #if white can move from index i with die2
                if player == 0:
                    if (self.boards[player][i] > 0 and i + die < 24 and self.boards[enemy][i + die] < 2):
                        j = i + die
                        if j > 24:
                            continue
                        moves_list.append((i, j))
                if player == 1:
                    if (self.boards[player][i] > 0 and i - die > 0 and self.boards[enemy][i - die] < 2):
                        j = i - die
                        if j < 1:
                            continue
                        moves_list.append((i, j))
        return moves_list
    
    def do(self, move, player):
        '''This function executes a single move and returns a list of moves necessary to undo it'''
        enemy  = int(not player)
        undos = []
        i,j  = move
        #Check if move is not bearing off
        if j != -1:
            self.boards[player][j]  += 1
        self.boards[player][i]  -= 1
        undos.append((j,i,player))
        #If enemy player has a piece there, put them on bar
        if self.boards[enemy][j] == 1 and j != -1:
            #Remove from the old piece index
            self.boards[enemy][j] -= 1
            #Add to the new piece index, (the bar)
            self.boards[enemy][0] += 1
            #Provide undo tuple, (new index, old index, board index)
            undos.append((0,j,enemy))
        #return the special formatted actions
        return undos
    
    def undo(self, moves):
        for move in moves:
            i,j,player  = move
            #Check if the move was bearing off
            if i != -1:
                #Remove from the new piece index
                self.boards[player][i]  -= 1
                
            #Place back onto the old piece index
            self.boards[player][j]  += 1
    
    def score(self, player):
        '''Computes/returns the score for the specified player's board (r or w)'''
        
        barConst = 100
        doorConst = 50
        bearConst = 10
        moveForwardConst = 1
        
        enemy = int(not player)
        scores = [0,0]
    
        '''Increase score if enemy has pieces on bar'''
        scores[0] += self.boards[1][0] * barConst
        scores[1] += self.boards[0][0] * barConst
        
        for index in range(1, 25):
            
            self.boards[0] += index * self.boards[0]
            self.boards[1] += index * self.boards[1]
            
            '''Increase score if pieces are doored (stacked)'''
            if self.boards[0][index] > 1:
                scores[0] += doorConst
                
            if self.boards[1][index] > 1:
                scores[1] += doorConst
                
        if self.isBearingOff(0):
            scores[0] += bearConst
        if self.isBearingOff(1):
            scores[1] += bearConst  
        
        value =  scores[player] - scores[enemy]
        
        return value
    
    def isBearingOff(self, player):
        if player == 0:
            for position in self.boards[player][0:18]:
                if position != 0:
                    return False
            
        elif player == 1:
            if self.boards[player][0] != 0:
                return False
            for position in self.boards[player][7:24]:
                if position != 0:
                    return False
        
        return True
    
    def isGameOver(self):
        '''returns true if the state is terminal (game over), else false'''
        redWon = True
        for i in range(24):
            if self.boards[0][i] > 0:
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

    def initializeActionsArray(self):
        array = [[[] for i in range(1, j + 1)] for j in range(1, 7)]
        return array
    
