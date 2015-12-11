import argparse, sys, time, random
from CuttingOff import CuttingOff
from ForwardPruning import RandomForwardPruning
from State import State
from Visualizer import writeBoard


## CLASS FOR STORING COMMAND LINE ARGUMENTS ##
class Inputs:
    pass

## CREATE ARGUMENT PARSING OBJECT ##
parser = argparse.ArgumentParser(description="This program provides tools to evaluate the imperfect real-time pruning algorithms implemented")
parser.add_argument("--runs",   metavar="INT", dest="runs",   nargs=1, default=[3],type=int,  help="Number of games to run")
parser.add_argument("--log",    metavar="FILE", dest="file",  nargs=1, default=[""],type=str,  help="Specify a log file (default will print to terminal)")
parser.add_argument("-rt",         dest="rt",     action='store_true', default=False, help="Execute Run-Time analysis (default is Cuttoff Search vs ForwardPruning)")
parser.add_argument("-mu",         dest="mu",     action='store_true', default=False, help="Execute Memory Usage analysis (default is Cuttoff Search vs ForwardPruning)")
parser.add_argument("-vs",         dest="vs",     action='store_true', default=False, help="Execute Forward Pruning Versus Cuttoff Search Analysis (Wins/Loss)")
parser.add_argument("-ff",         dest="ff",     action='store_true', default=False, help="Execute Forward Pruning Versus Itself Analysis (Wins/Loss)")
parser.add_argument("-cc",         dest="cc",     action='store_true', default=False, help="Execute Cuttoff Search Versus Itself Versus  Analysis (Wins/Loss)")
parser.add_argument("-a",metavar="INT", dest="alpha",  nargs=1, default=[-100000], type=int,help="Specify an alpha value for Alpha-Beta Pruning")
parser.add_argument("-b",metavar="INT", dest="beta",   nargs=1, default=[100000],   type=int,help="Specify a beta value for Alpha-Beta Pruning")
parser.add_argument("-R",metavar="FLOAT", dest="ratio",   nargs=1, default=[0.67],   type=int,help="Specify a Remove ratio for Random Forward Pruning")
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
            
    def __construct__(self):
        w =  [0,0,0,0,0,0,5,0,3,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,2] 
        r =  [0,2,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,5,0,0,0,0,0]
        self.state = State(r,w)
        
    def get_analysis(self):
        '''This function generates the analysis for the memory usage in terms
        of moves evaluated.  This function returns in the form of a string.'''
        r = 0
        w = 0
        tot_move = [0,0]
        runs = self.runs
        while runs > 0:
            self.faceoff()
            print("Game {0} completed for Memory Usage Test".format(self.runs - (runs - 1)))
            tot_move[0] += self.AI1.count
            tot_move[1] += self.AI2.count
            runs -= 1
        
        avg_mov = [tot_move[0]/self.runs,tot_move[1]/self.runs]
        ## CREATE OUTPUT RUN-TIME ANALYSIS ##
        analysis =  ' vs. '.join(self.names)+ " Memory Usage Analysis\n\n"
        analysis += "\tTotal Moves over " + str(self.runs) + " runs:\n"
        analysis += "\t\t" + self.names[0] + ":\t" + str(tot_move[0]) + "\n"
        analysis += "\t\t" + self.names[1] + ":\t" + str(tot_move[1])  + "\n\n"
        analysis += "\tAverage Moves per Game:\n"
        analysis += "\t\t" + self.names[0] + ":\t" + str(avg_mov[0]) + "\n"
        analysis += "\t\t" + self.names[1] + ":\t" + str(avg_mov[1])  + "\n\n"
        ## FORMAT ANALYSIS FOR MEMORY USAGE ##
        analysis += "Memory Usage Test Results\n\n"
        
        ## RETURN THE MEMORY USAGE ANALYSIS AS A STRING ##
        return analysis
    
    def faceoff(self):
        self.__construct__()
        self.player = 0
        self.enemy  = 1
        not_game_over = True
        while not_game_over:
            if self.state.isGameOver():
                not_game_over = False
                break
            #AI Action
            dice            = [random.randint(1,6), random.randint(1,6)]
            action          = self.AI1.Search(self.state, self.player, dice)
            if action != None:
                self.state.result(action, self.enemy)
                
            if self.state.isGameOver():
                not_game_over = False
                break
            #AI Action
            dice            = [random.randint(1,6), random.randint(1,6)]
            action          = self.AI2.Search(self.state, self.enemy, dice)
            if action != None:
                self.state.result(action, self.enemy)
    

    
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
            print("Game {0} completed for Versus Test".format(self.runs - (runs - 1)))
            if winner == "r":
                r += 1
            elif winner == "w":
                w += 1
            runs -= 1
            
        analysis =  ' vs. '.join(self.names)+ " Win/Loss Analysis\n\n"
        analysis += "\tWins over " + str(self.runs) + " runs:\n"
        analysis += "\t\tCuffoff Search:\t\t" + str(r) + "\n"
        analysis += "\t\tForward Pruning:\t" + str(w)  + "\n\n"
        return analysis
    
    def faceoff(self):
        self.__construct__()
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
        return self.getWinner()
    
    def getWinner(self):
        '''returns the winner of the game'''
        redWon = True
        whiteWon = True
        for i in range(25):
            if self.state.boards[0][i] > 0:
                redWon = False
            if self.state.boards[1][i] > 0:
                whiteWon = False
            if not redWon and not whiteWon:
                return "n"
        if redWon:
            return "r"
            
        if whiteWon:
            return "w"
    
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
            
    def __construct__(self):
        w =  [0,0,0,0,0,0,5,0,3,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,2] 
        r =  [0,2,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,5,0,0,0,0,0]
        self.state = State(r,w)
    
    def faceoff(self):
        self.__construct__()
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
            if action1 != None:
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
            print("Game {0} completed for Run-Time Test".format(self.runs - (runs - 1)))
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
    RUN_VS  = inputs.vs
    RUN_RT  = inputs.rt
    RUN_MU  = inputs.mu
    ALPHA   = inputs.alpha[0]
    BETA    = inputs.beta[0]
    DEPTH   = inputs.depth[0]
    RATIO   = inputs.ratio[0]
    ## CHECK VALIDITY OF COMMAND LINE ARGS ##
    invalid = 0
    if COUNT < 1:
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
    if RUN_RT or not (RUN_MU or RUN_RT or RUN_VS):
        table += seper
        run_time = Run_Time(ALPHA, BETA, DEPTH, RATIO, COUNT, FF, CC)
        ## ADD RUN TIME REPORT BY CALLING get_analysis FUNCTION ##
        table += run_time.get_analysis()
    
    #IF NO TEST SPECIFIED OR MEMORY USAGE SPECIFIED, EXECUTE MEMORY USAGE
    if RUN_MU or not (RUN_MU or RUN_RT or RUN_VS):
        table += seper
        mem_usage = Mem_Usage(ALPHA, BETA, DEPTH, RATIO, COUNT, FF, CC)
        ## ADD MEMORY USAGE REPORT BY CALLING get_analysis FUNCTION ##
        table += mem_usage.get_analysis()
    
    #IF NO TEST SPECIFIED OR SOLUTION PATH SPECIFIED, EXECUTE SOLUTION PATH
    if RUN_VS or not (RUN_MU or RUN_RT or RUN_VS):
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