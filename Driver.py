from CuttingOff     import CuttingOff
from State          import State
from Visualizer     import writeBoard
from ForwardPruning import RandomForwardPruning
from time           import time
import sys, timeit, argparse, sys, random

## CLASS FOR STORING COMMAND LINE ARGUMENTS ##
class Inputs:
    pass

## CREATE ARGUMENT PARSING OBJECT ##
parser = argparse.ArgumentParser(description="This program executes puzzles ")
parser.add_argument("-a",metavar="INT", dest="alpha",  nargs=1, default=[-100000], type=int,help="Specify an alpha value for Alpha-Beta Pruning")
parser.add_argument("-b",metavar="INT", dest="beta",   nargs=1, default=[100000],   type=int,help="Specify an beta value for Alpha-Beta Pruning")
parser.add_argument("-R",metavar="FLOAT", dest="ratio",   nargs=1, default=[0.5],   type=int,help="Specify an Remove ratio for Random Forward Pruning")
parser.add_argument("-d",metavar="INT", dest="depth",  nargs=1, default=[3],   type=int,help="Specify a cutt-off depth for the AI algorithm")
parser.add_argument("-P", metavar="NAME", dest="pruning",nargs=1, default=["CO"],  type=str, help="Specify a pruning algorithm (CuttingOff, ForwardPruning)")
parser.add_argument("--face-off", dest="faceoff", action='store_true', default=False, help="Specify to have both AI algorithms play against eachother")
parser.add_argument("--FF", dest="ff", action='store_true', default=False, help="Specify to have Forward Pruing play against itself")
parser.add_argument("--CC", dest="cc", action='store_true', default=False, help="Specify to have Cuttoff Search play against itself")

class Driver:
    def __init__(self, Alpha, Beta, Depth, Ratio, PruningType, FF, CC):
        self.Alpha = Alpha
        self.Beta  = Beta 
        self.Depth = Depth
        self.Ratio = Ratio
        if PruningType.lower() in ["co","cuttingoff"]:
            self.AI1 = CuttingOff(self.Alpha, self.Beta, self.Depth)
        elif PruningType.lower() in ["fc","forwardpruning"]:
            self.AI1 = RandomForwardPruning(self.Alpha, self.Beta, self.Depth, self.Ratio)
        else:
            print("Error: {0} is not a valid Pruning Type".format(PruningType))
            sys.exit(1)
        if CC:
            self.AI1 = CuttingOff(self.Alpha, self.Beta, self.Depth)
            self.AI2 = CuttingOff(self.Alpha, self.Beta, self.Depth)
        elif FF:
            self.AI1 = RandomForwardPruning(self.Alpha, self.Beta, self.Depth, self.Ratio)
            self.AI2 = RandomForwardPruning(self.Alpha, self.Beta, self.Depth, self.Ratio)
        else:
            self.AI1 = CuttingOff(self.Alpha, self.Beta, self.Depth)
            self.AI2 = RandomForwardPruning(self.Alpha, self.Beta, self.Depth, self.Ratio)
            
        self.__construct__()
            
    def __construct__(self):
        w =  [0,0,0,0,0,0,5,0,3,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,2] 
        r =  [0,2,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,5,0,0,0,0,0]
        self.state = State(r,w)
    
    def start(self):
        #Initial game sequence
        input("Press Enter to Begin...")
        not_set = True
        player  = ""
        while not_set:
            print("Select your color...(R or W)")
            player = input("Red or White? ")
            if player.lower() in ["r","red"]:
                self.player = 0
                self.enemy  = 1
                not_set = False
            elif player.lower() in ["w","white"]:
                self.player = 1
                self.enemy  = 0
                not_set = False
            else:
                print("{0} is not a valid choice".format(player))
        
        
        #Print the board for the player to see!
        writeBoard(self.state.redBoard, self.state.whiteBoard)
        tie = True
        dice = [0, 0]
        input("Press enter to roll the dice and see who goes first...")
        #Loop until somebody wins the dice roll
        while tie:
            dice = [random.randint(1,6),random.randint(1,6)]
            print("\n\nYour roll:  {0}\nTheir roll: {1}".format(dice[0],dice[1]))
            if dice[0] != dice[1]:
                tie = False
            else:
                input("It's a tie! Press Enter to reroll...")
        #if AI's die was higher, have them go first
        if dice[1] > dice[0]:
            print("They go first...")
            #AI Action
            print("Their Roll: {0}".format(', '.join([str(x) for x in dice])))
            dice            = [random.randint(1,6), random.randint(1,6)]
            action          = self.AI1.Search(self.state, self.enemy, dice)
            self.state.result(action, self.enemy)
            print("Computer has performed the following moves: {0}".format(action))
        else:
            print("You go first...")
        
        #Begin Game Loop with player starting
        game_not_over = True
        while game_not_over:
            if self.state.isGameOver():
                not_game_over = False
                break
            #Player Input Loop and values
            dice            = [random.randint(1,6),random.randint(1,6)]
            invalid = True
            moves = 2
            while moves > 0:
                possible_moves = []
                for die in dice:
                    possible_moves += self.state.moves(die, self.player)
                if self.state.isGameOver():
                    not_game_over = False
                    break
                #Print the board for the player to see!
                writeBoard(self.state.redBoard, self.state.whiteBoard)
                if len(possible_moves) == 0:
                    print("No valid moves exist...passing turn")
                    break
                print("Your Roll: {0}".format(', '.join([str(x) for x in dice])))
                str_i = input("Which piece would like to move? ")
                str_j = input("To where would you like to move it? ")
                die = 0
                try:
                    i = int(str_i)
                    j = int(str_j)
                    if self.player == 0 and j - i in dice:
                        die = j - i
                    elif self.player == 1 and i - j in dice:
                        die = i - j
                    else:
                        print("Invalid move...Please check your dice value")
                        continue
                except:
                    print("Invalid Input: Length is not of type integer")
                    continue
                if (i, j) not in possible_moves:
                    print("Invalid Move: Does not match valid possible moves")
                    print("Hint: Possible moves are: {0}".format(', '.join([str(x) for x in possible_moves])))
                else:
                    moves -= 1
                    self.state.do((i,j), self.player)
                    remove_index  = dice.index(die)
                    dice.pop(remove_index)
                    
            #Print the board for the player to see!
            writeBoard(self.state.redBoard, self.state.whiteBoard)
            #AI Action
            dice            = [random.randint(1,6),random.randint(1,6)]
            print("Their Roll: {0}".format(', '.join([str(x) for x in dice])))
            action          = self.AI1.Search(self.state, self.enemy, dice)
            if action != None:
                self.state.result(action, self.enemy)
                print("Computer has performed the following moves: {0}".format(action))
            else:
                print("The Computer has no valid moves, passing turn...")
            
        if self.getWinner() == "w":
            print("White Wins!!!")
        elif self.getWinner() == "r":
            print("Red Wins!!!")
        else:
            print("Nobody Wins!!!")
    
    
    def getWinner(self):
        winner = 1
        for i in range(24):
            if(self.state.redBoard[i] != 0):
                winner = 0
                break

        if (winner == 1):
            return "r"
            
        winner = 2
        for i in range(24):
            if(self.state.whiteBoard[i] != 0):
                winner = 0
                break

        if (winner == 2):
            return "w"

        return "n"
        
        
    def faceoff(self):
        self.player = 0
        self.enemy  = 1
        not_game_over = True
        while not_game_over:
            if self.state.isGameOver():
                not_game_over = False
                break
            dice            = [random.randint(1,6),random.randint(1,6)]
            #AI Action
            print("Red Roll: {0}".format(', '.join([str(x) for x in dice])))
            dice            = [random.randint(1,6), random.randint(1,6)]
            action1          = self.AI1.Search(self.state, self.player, dice)
            if action1 != None:
                self.state.result(action1, self.enemy)
                print("Computer has performed the following moves: {0}".format(action1))
            else:
                print("The Computer has no valid moves, passing turn...")
            #Print the board for the player to see!
            writeBoard(self.state.redBoard, self.state.whiteBoard)
            #input("Press Enter to continue...")
            if self.state.isGameOver():
                not_game_over = False
                break
            #AI Action
            print("White Roll: {0}".format(', '.join([str(x) for x in dice])))
            dice            = [random.randint(1,6), random.randint(1,6)]
            action2          = self.AI2.Search(self.state, self.enemy, dice)
            if action2 != None:
                self.state.result(action2, self.enemy)
                print("Computer has performed the following moves: {0}".format(action2))
            else:
                print("The Computer has no valid moves, passing turn...")
            #Print the board for the player to see!
            writeBoard(self.state.redBoard, self.state.whiteBoard)
            #input("Press Enter to continue...")
        
        if self.getWinner() == "w":
            print("White Wins!!!")
        elif self.getWinner() == "r":
            print("Red Wins!!!")
        else:
            print("Nobody Wins!!!")
    
    


if __name__ == '__main__':
    inputs = Inputs()
    parser.parse_args(sys.argv[1:], namespace=inputs)
    driver = Driver(inputs.alpha[0],inputs.beta[0],inputs.depth[0],inputs.ratio[0],inputs.pruning[0],inputs.ff,inputs.cc)
    try:
        if inputs.faceoff or inputs.ff or inputs.cc:
            driver.faceoff()
        else:
            driver.start()
    except KeyboardInterrupt:
        print("Command Ctrl-C: Now Exiting...")