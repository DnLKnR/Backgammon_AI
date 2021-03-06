from CuttingOff     import CuttingOff
from Parser         import parseInputString
#from ForwardPruning import ForwardPruning

'''

Below is the starting position of the backgammon board.
The numbers shown represent the indices of the board arrays.
The 0th index of each array represents the "BAR" containing
their own pieces.  As such, red will move toward the end of
the array while white will move toward the beginning.

_____________________________________________________
|                       |   |                       |
|13  14  15  16  17  18 |   |19  20  21  22  23  24 |
| w               r     |   | r                   w |
| w               r     |   | r                   w |
| w               r     |   | r                     |
| w                     |   | r                     |
| w                     |   | r                     |
|                       |BAR|                       |
| r                     |   | w                     |
| r                     |   | w                     |
| r               w     |   | w                     |
| r               w     |   | w                   r |
| r               w     |   | w                   r |
|12  11  10   9   8   7 |   | 6   5   4   3   2   1 |
|_______________________|___|_______________________|



'''

from random import randint

class Game:
    def __init__(self):#   b 1 2 3 4 5 6 7 8 910 1 2 3 4 5 6 7 8 910 1 2 3 4
        self.redBoard =   [0,0,0,0,0,0,5,0,3,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,2]
        self.whiteBoard = [0,2,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,5,0,0,0,0,0]
        self.diceRolls = [0,0]
        return
        

    def rollDice(self):
        self.diceRolls[0] = randint(1,6)
        self.diceRolls[1] = randint(1,6)
        return

    def whiteMove(self, movesList):
        return

    def redMove(self, movesList):
        return

    def getWinner(self):
        winner = 1
        for i in range(24):
            if(self.redBoard[i] != 0):
                winner = 0
                break

        if (winner == 1):
            return "r"
            
        winner = 2
        for i in range(24):
            if(self.whiteBoard[i] != 0):
                winner = 0
                break

        if (winner == 2):
            return "w"

        return "n"
