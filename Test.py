import argparse, sys, time, random
from CuttingOff import CuttingOff
from ForwardPruning import RandomForwardPruning
from State import State


## CLASS FOR STORING COMMAND LINE ARGUMENTS ##
class Inputs:
    pass

## CREATE ARGUMENT PARSING OBJECT ##
parser = argparse.ArgumentParser(description="This program provides tools to evaluate the imperfect real-time pruning algorithms implemented")
parser.add_argument("--runs",   metavar="INT", dest="runs",   nargs=1, default=[10],type=int,  help="Number of games to run")
parser.add_argument("--log",    metavar="FILE", dest="file",  nargs=1, default=[""],type=str,  help="Specify a log file (default will print to terminal)")
parser.add_argument("-rt",         dest="rt",     action='store_true', default=False, help="Execute Run-Time analysis (default is Cuttoff Search vs ForwardPruning)")
parser.add_argument("-mu",         dest="mu",     action='store_true', default=False, help="Execute Memory Usage analysis (default is Cuttoff Search vs ForwardPruning)")
parser.add_argument("-vs",         dest="vs",     action='store_true', default=False, help="Execute Forward Pruning Versus Cuttoff Search Analysis (Wins/Loss)")
parser.add_argument("-ff",         dest="ff",     action='store_true', default=False, help="Execute Forward Pruning Versus Itself Analysis (Wins/Loss)")
parser.add_argument("-cc",         dest="cc",     action='store_true', default=False, help="Execute Cuttoff Search Versus Itself Versus  Analysis (Wins/Loss)")
parser.add_argument("-a",metavar="INT", dest="alpha",  nargs=1, default=[-100000], type=int,help="Specify an alpha value for Alpha-Beta Pruning")
parser.add_argument("-b",metavar="INT", dest="beta",   nargs=1, default=[100000],   type=int,help="Specify a beta value for Alpha-Beta Pruning")
parser.add_argument("-R",metavar="FLOAT", dest="ratio",   nargs=1, default=[0.5],   type=int,help="Specify a Remove ratio for Random Forward Pruning")
parser.add_argument("-d",metavar="INT", dest="depth",  nargs=1, default=[3],   type=int,help="Specify a cut-off depth for the AI algorithm")

class Mem_Usage:
    def __init__(self,alpha,beta,depth,ratio,runs,FF,CC):
        self.runs = runs
        self.Alpha = alpha
        self.Beta  = beta
        self.Depth = depth
        self.Ratio = ratio
        self.names = []
        if CC:
            self.AI1 = CuttingOff(self.Alpha, self.Beta, self.Depth)
            self.AI2 = CuttingOff(self.Alpha, self.Beta, self.Depth)
            self.names = ["CuttingOff", "CuttingOff"]
        elif FF:
            self.AI1 = RandomForwardPruning(self.Alpha, self.Beta, self.Depth, self.Ratio)
            self.AI2 = RandomForwardPruning(self.Alpha, self.Beta, self.Depth, self.Ratio)
            self.names = ["ForwardPruning","ForwardPruning"]
        else:
            self.AI1 = CuttingOff(self.Alpha, self.Beta, self.Depth)
            self.AI2 = RandomForwardPruning(self.Alpha, self.Beta, self.Depth, self.Ratio)
            self.names = ["CuttingOff","ForwardPruning"]
        self.__construct__()
            
    def __construct__(self):
        w =  [0,0,0,0,0,0,5,0,3,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,2] 
        r =  [0,2,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,5,0,0,0,0,0]
        self.state = State(r,w)
        
    def get_analysis(self):
        '''This function generates the analysis for the memory usage in terms
        of nodes.  This function returns in the form of a string.'''
        MemInfo_of = [[],[]]
        BFS,BI    = 0, 1
        ## EXECUTE BREADTH FIRST SEARCH AND BIDIRECTIONAL MEMORY-USAGE ANALYSIS ##
        for h in self.heights:
            ## SETUP AND STORE INSTANCE FOR MEMORY USAGE FOR HEIGHT h ##
            answer_bfs = breadth_first_search(Towers_Of_Hanoi(length=self.towers,height=h,explore=self.explore),
                                              return_mem_usage=True)
            ## GET AND STORE MEMORY USAGE METRICS ##
            BFS_mem = answer_bfs[-1]
            MemInfo_of[BFS].append(BFS_mem)
            
            answer_bi = bidirectional_search(Towers_Of_Hanoi(length=self.towers,height=h,explore=self.explore),
                                             Towers_Of_Hanoi(length=self.towers,height=h,swap=True,explore=self.explore),
                                             return_mem_usage=True)
            BI_mem  = answer_bi[-1]
            MemInfo_of[BI].append(BI_mem)
            
        
        ## FORMAT ANALYSIS FOR MEMORY USAGE ##
        analysis = "Memory Usage Test Results\n\n"
        for i,h in enumerate(self.heights):
            analysis += "\tFor Height = " + str(h) + ":\n"
            analysis += "\t\tBreadth-First-Search sizes:\n"
            analysis += "\t\t  Graph:\t\t"        + str(MemInfo_of[BFS][i][0]) + "\n"
            if self.explore:
                analysis += "\t\t  Explored:\t\t" + str(MemInfo_of[BFS][i][1]) + "\n"
            analysis += "\t\t  Frontier Max:\t"   + str(MemInfo_of[BFS][i][2]) + "\n"
            analysis += "\t\tBidirectional sizes:\n"
            analysis += "\t\t  Graph:\t\t"        + str(MemInfo_of[BI][i][0]) + "\n"
            if self.explore:
                analysis += "\t\t  Explored:\t\t" + str(MemInfo_of[BI][i][1]) + "\n"
            analysis += "\t\t  Frontier Max:\t"   + str(MemInfo_of[BI][i][2]) + "\n\n"
        
        ## RETURN THE MEMORY USAGE ANALYSIS AS A STRING ##
        return analysis
    
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
            action          = self.AI1.Search(self.state, self.player, dice)
            if action != None:
                self.state.result(action, self.enemy)
                print("Computer has performed the following moves: {0}".format(action))
            else:
                print("The Computer has no valid moves, passing turn...")
            #Print the board for the player to see!
            writeBoard(self.state.redBoard, self.state.whiteBoard)
            #input("Press Enter to continue...")
            if self.state.isGameOver():
                not_game_over = False
                break
            #AI Action
            print("White Roll: {0}".format(', '.join([str(x) for x in dice])))
            dice            = [random.randint(1,6), random.randint(1,6)]
            action          = self.AI2.Search(self.state, self.enemy, dice)
            if action != None:
                self.state.result(action, self.enemy)
                print("Computer has performed the following moves: {0}".format(action))
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
    
class Versus:
    def __init__(self,alpha,beta,depth,ratio,runs,FF,CC):
        self.runs = runs
        self.Alpha = alpha
        self.Beta  = beta
        self.Depth = depth
        self.Ratio = ratio
        self.names = []
        if CC:
            self.AI1 = CuttingOff(self.Alpha, self.Beta, self.Depth)
            self.AI2 = CuttingOff(self.Alpha, self.Beta, self.Depth)
            self.names = ["CuttingOff", "CuttingOff"]
        elif FF:
            self.AI1 = RandomForwardPruning(self.Alpha, self.Beta, self.Depth, self.Ratio)
            self.AI2 = RandomForwardPruning(self.Alpha, self.Beta, self.Depth, self.Ratio)
            self.names = ["ForwardPruning","ForwardPruning"]
        else:
            self.AI1 = CuttingOff(self.Alpha, self.Beta, self.Depth)
            self.AI2 = RandomForwardPruning(self.Alpha, self.Beta, self.Depth, self.Ratio)
            self.names = ["CuttingOff","ForwardPruning"]
    
        self.__construct__()
            
    def __construct__(self):
        w =  [0,0,0,0,0,0,5,0,3,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,2] 
        r =  [0,2,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,5,0,0,0,0,0]
        self.state = State(r,w)
        
    def get_analysis(self):
        r = 0
        w = 0
        runs = self.runs
        while runs > 0:
            winner = self.faceoff()
            if winner == "r":
                r += 1
            elif winner == "w":
                w += 1
            runs -= 1
            
        analysis =  ' vs. '.join(self.names)+ " Win/Loss Analysis\n\n"
        analysis += "\tWins over " + str(self.runs) + " runs:\n"
        analysis += "\t\tCuffoff Search:\t" + str(r) + "\n"
        analysis += "\t\tForward Pruning:\t" + str(w)  + "\n\n"
        return analysis
    
    def faceoff(self):
        self.player = 0
        self.enemy  = 1
        not_game_over = True
        while not_game_over:
            if self.state.isGameOver():
                not_game_over = False
                break
            #AI1 Action
            dice            = [random.randint(1,6), random.randint(1,6)]
            action          = self.AI1.Search(self.state, self.player, dice)
            if action != None:
                self.state.result(action, self.enemy)
            #Check if the game is over
            if self.state.isGameOver():
                not_game_over = False
                break
            #AI2 Action
            dice            = [random.randint(1,6), random.randint(1,6)]
            action          = self.AI2.Search(self.state, self.enemy, dice)
            if action != None:
                self.state.result(action, self.enemy)
        
        if self.getWinner() == "w":
            return "w"
        elif self.getWinner() == "r":
            return "r"
        else:
            return "n"
    
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
    
class Run_Time:
    def __init__(self,alpha,beta,depth,ratio,runs,FF,CC):
        self.runs = runs
        self.Alpha = alpha
        self.Beta  = beta
        self.Depth = depth
        self.Ratio = ratio
        self.names = []
        if CC:
            self.AI1 = CuttingOff(self.Alpha, self.Beta, self.Depth)
            self.AI2 = CuttingOff(self.Alpha, self.Beta, self.Depth)
            self.names = ["CuttingOff", "CuttingOff"]
        elif FF:
            self.AI1 = RandomForwardPruning(self.Alpha, self.Beta, self.Depth, self.Ratio)
            self.AI2 = RandomForwardPruning(self.Alpha, self.Beta, self.Depth, self.Ratio)
            self.names = ["ForwardPruning","ForwardPruning"]
        else:
            self.AI1 = CuttingOff(self.Alpha, self.Beta, self.Depth)
            self.AI2 = RandomForwardPruning(self.Alpha, self.Beta, self.Depth, self.Ratio)
            self.names = ["CuttingOff","ForwardPruning"]
        self.__construct__()
            
    def __construct__(self):
        w =  [0,0,0,0,0,0,5,0,3,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,2] 
        r =  [0,2,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,5,0,0,0,0,0]
        self.state = State(r,w)
        
    def get_analysis(self):
        r = 0
        w = 0
        runs = self.runs
        while runs > 0:
            winner = self.faceoff()
            if winner == "r":
                r += 1
            elif winner == "w":
                w += 1
            runs -= 1
            
        analysis =  ' vs. '.join(self.names)+ " Win/Loss Analysis\n\n"
        analysis += "\tWins over " + str(self.runs) + " runs:\n"
        analysis += "\t\t" + self.names[0] + ":\t" + str(r) + "\n"
        analysis += "\t\t" + self.names[1] + ":\t" + str(w)  + "\n\n"
        return analysis
    
    def faceoff(self):
        self.player = 0
        self.enemy  = 1
        moves_r,moves_w,times_r,times_w = 0,0,0,0
        not_game_over = True
        while not_game_over:
            if self.state.isGameOver():
                not_game_over = False
                break
            #AI1 Action
            dice            = [random.randint(1,6), random.randint(1,6)]
            start = time.time()
            action1          = self.AI1.Search(self.state, self.player, dice)
            end   = time.time()
            moves_r += 1
            times_r  += (end - start)
            if action != None:
                self.state.result(action1, self.enemy)
            #Check if the game is over
            if self.state.isGameOver():
                not_game_over = False
                break
            #AI2 Action
            dice            = [random.randint(1,6), random.randint(1,6)]
            start = time.time()
            action2          = self.AI2.Search(self.state, self.enemy, dice)
            end   = time.time()
            moves_w += 1
            times_w  += (end - start)
            if action2 != None:
                self.state.result(action2, self.enemy)
        
        return (moves_r,moves_w,times_r,times_w)
    
    def get_analysis(self):
        r = 0
        w = 0
        moves = [0,0]
        times = [0,0]
        runs = self.runs
        while runs > 0:
            moves_r,moves_w,total_r,total_w = self.faceoff()
            moves[0] += moves_r
            moves[1] += moves_w
            times[0] += total_r
            times[1] += total_w
            runs -= 1
        
        ## COMPUTE TOTAL AVG RUNTIME AND AVG MOVE TIME FOR EACH ##
        avg_tot_time = [times[0]/self.runs,times[1]/self.runs]
        avg_mov_time = [times[0]/moves[0],times[1]/moves[1]]
        
        ## CREATE OUTPUT RUN-TIME ANALYSIS ##
        analysis =  ' vs. '.join(self.names)+ " Run-Time Analysis\n\n"
        analysis += "\tAverage Total Time over " + str(self.runs) + " runs:\n"
        analysis += "\t\t" + self.names[0] + ":\t" + str(avg_tot_time[0]) + "\n"
        analysis += "\t\t" + self.names[1] + ":\t" + str(avg_tot_time[1])  + "\n\n"
        analysis += "\tAverage Time per Move:\n"
        analysis += "\t\t" + self.names[0] + ":\t" + str(avg_mov_time[0]) + "\n"
        analysis += "\t\t" + self.names[1] + ":\t" + str(avg_mov_time[1])  + "\n\n"
        
        return analysis

if __name__ == '__main__':
    ## PARSE COMMAND LINE ARGUMENTS AND STORE VALUES IN inputs OBJECT ##
    inputs = Inputs()
    parser.parse_args(sys.argv[1:], namespace=inputs)
    ## GET COMMAND LINE ARGUMENTS ##
    FF      = inputs.ff
    CC      = inputs.cc
    COUNT   = inputs.runs[0]
    LOGFILE = inputs.file[0]
    RUN_SP  = inputs.vs
    RUN_RT  = inputs.rt
    RUN_MU  = inputs.mu
    ALPHA   = inputs.alpha[0]
    BETA    = inputs.beta[0]
    DEPTH   = inputs.depth[0]
    RATIO   = inputs.ratio[0]
    ## CHECK VALIDITY OF COMMAND LINE ARGS ##
    invalid = 0
    if COUNT < 1 and (RUN_ALL or RUN_RT):
        print("Invalid Execution Count: Number of executions must be greater than 1 to actually run")
        invalid += 1
    extension = LOGFILE.split(".")[-1]
    if LOGFILE != "" and extension not in ["txt","log"]:
        print("Invalid Log Extension: Log files should either be of *.txt or *.log")
        invalid += 1
    if invalid:
        print("\n...Program Exiting")
        sys.exit(1)
    
    ## FORMAT OUTPUT FOR ANALYSIS HEADER ##
    table  = "Backgammon Adversarial Search Analysis\n"
    seper  = "-" * len(table) + "\n"
    table += seper
    
    #IF NO TEST SPECIFIED OR RUNTIME SPECIFIED, EXECUTE RUNTIME
    if RUN_RT or not (RUN_MU or RUN_RT or RUN_SP):
        table += seper
        run_time = Run_Time(ALPHA, BETA, DEPTH, RATIO, COUNT, FF, CC)
        ## ADD RUN TIME REPORT BY CALLING get_analysis FUNCTION ##
        table += run_time.get_analysis()
    
    #IF NO TEST SPECIFIED OR MEMORY USAGE SPECIFIED, EXECUTE MEMORY USAGE
    if RUN_MU or not (RUN_MU or RUN_RT or RUN_SP):
        #table += seper
        mem_usage = Mem_Usage(ALPHA, BETA, DEPTH, RATIO, COUNT, FF, CC)
        ## ADD MEMORY USAGE REPORT BY CALLING get_analysis FUNCTION ##
        #table += mem_usage.get_analysis()
    
    #IF NO TEST SPECIFIED OR SOLUTION PATH SPECIFIED, EXECUTE SOLUTION PATH
    if RUN_VS or not (RUN_MU or RUN_RT or RUN_SP):
        table += seper
        #Default test just returns the solution path lengths
        versus = Versus(ALPHA, BETA, DEPTH, RATIO, COUNT, FF, CC)
        table += versus.get_analysis()
    
    #Print to terminal if a log file was not specified
    if LOGFILE == "":
        print(table)
    else:
        log = open(LOGFILE, 'w')
        log.write(table)
        log.close()
        print("Results output to " + LOGFILE)