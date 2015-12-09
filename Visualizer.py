'''

Below is the starting position of the backgammon board.
The numbers shown represent the indices of the board arrays.
The 0th index of each array represents the "BAR" containing
their own pieces.  As such, red will move toward the end of
the array while white will move toward the beginning.

_______________________________________________________
|                        |   |                        |
|13  14  15  16  17  18  |   |19  20  21  22  23  24  |
| w               r      |   | r                   w  |
| w               r      |   | r                   w  |
| w               r      |   | r                      |
| w                      |   | r                      |
| w                      |   | r                      |
|                        |BAR|                        |
| r                      |   | w                      |
| r                      |   | w                      |
| r               w      |   | w                      |
| r               w      |   | w                   r  |
| r               w      |   | w                   r  |
|12  11  10   9   8   7  |   | 6   5   4   3   2   1  |
|________________________|___|________________________|



'''

def writeBoard(redBoard, whiteBoard):
    outString = "_______________________________________________________\n" + \
    "|                        |   |                        |\n" + \
    "|13  14  15  16  17  18  |   |19  20  21  22  23  24  |\n"
    
    for j in range(5):
        outString += "|"
        for i in range(13, 19):
            if(redBoard[i] > 5 + j):
                outString += "rr  "
            elif(redBoard[i] > 0 + j):
                outString += " r  "
            elif(whiteBoard[i] > 5 + j):
                outString += "ww  "
            elif(whiteBoard[i] > 0 + j):
                outString += " w  "
            else:
                outString += "    "
                
        outString += "| "
        
        if(whiteBoard[0] > j):
            outString += "w"
        else:
            outString += " "
        
        outString += " |"
        
        for i in range(19, 25):
            if(redBoard[i] > 5 + j):
                outString += "rr  "
            elif(redBoard[i] > 0 + j):
                outString += " r  "
            elif(whiteBoard[i] > 5 + j):
                outString += "ww  "
            elif(whiteBoard[i] > 0 + j):
                outString += " w  "
            else:
                outString += "    "
                
        outString += "|\n"
        
    outString += "|                        |BAR|                        |\n" \
    
    for j in range(4, -1, -1):
        outString += "|"
        for i in range(12, 6, -1):
            if(redBoard[i] > 5 + j):
                outString += "rr  "
            elif(redBoard[i] > 0 + j):
                outString += " r  "
            elif(whiteBoard[i] > 5 + j):
                outString += "ww  "
            elif(whiteBoard[i] > 0 + j):
                outString += " w  "
            else:
                outString += "    "
                
        outString += "| "
        
        if(redBoard[0] > j):
            outString += "r"
        else:
            outString += " "
        
        outString += " |"
        
        for i in range(6, 0, -1):
            if(redBoard[i] > 5 + j):
                outString += "rr  "
            elif(redBoard[i] > 0 + j):
                outString += " r  "
            elif(whiteBoard[i] > 5 + j):
                outString += "ww  "
            elif(whiteBoard[i] > 0 + j):
                outString += " w  "
            else:
                outString += "    "
                
        outString += "|\n"
        
    
    outString += "|12  11  10   9   8   7  |   | 6   5   4   3   2   1  |\n" + \
    "|                        |   |                        |\n" + \
    "_______________________________________________________\n"
    
    print(outString)
    

#redBoard = [3,2,0,0,0,0,0,0,0,0,0,0,10,0,0,0,0,3,0,5,0,0,0,0,0]
#whiteBoard = [0,0,0,0,0,0,5,0,3,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,2]

#writeBoard(redBoard, whiteBoard)