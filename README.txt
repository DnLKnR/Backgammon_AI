Names: Daniel Koniar, John Mollberg
x500:  konia013, mollb011
ID:    4343456, 4806556

To run the tests, execute the Test.py file through the Python3.4 interpreter. These 
files should be fully functional.

To execute a playable game against CuttingOff Search, run the following:

    python3.4 Driver.py
    
To execute a playable game against ForwardPruning:

    python3.4 Driver.py -P FP
    
To execute with more personalized settings, you can use the following
command line arguments:

    usage: Driver.py [-h] [-a INT] [-b INT] [-R FLOAT] [-d INT] [-P NAME]
                     [--face-off] [--FF] [--CC]
    
    This program executes puzzles
    
    optional arguments:
      -h, --help  show this help message and exit
      -a INT      Specify an alpha value for Alpha-Beta Pruning
      -b INT      Specify an beta value for Alpha-Beta Pruning
      -R FLOAT    Specify an Remove ratio for Random Forward Pruning
      -d INT      Specify a cutt-off depth for the AI algorithm
      -P NAME     Specify a pruning algorithm (CuttingOff, ForwardPruning)
      --face-off  Specify to have both AI algorithms play against eachother
      --FF        Specify to have Forward Pruing play against itself
      --CC        Specify to have Cuttoff Search play against itself



To execute the basic test, run the following:
	
	python3.4 Test.py

To execute the basic tests to an output file called output.txt, run the
following:
	
	python3.4 Test.py --log output.txt
	
Note: output.txt can be swapped out for any file ending in either *.txt or
*.log.

To execute with more personalized settings, you can use the following 
command line arguments:

    usage: Test.py [-h] [--runs INT] [--log FILE] [-rt] [-mu] [-vs] [-ff] [-cc]
                   [-a INT] [-b INT] [-R FLOAT] [-d INT]
    
    This program provides tools to evaluate the imperfect real-time pruning
    algorithms implemented
    
    optional arguments:
      -h, --help  show this help message and exit
      --runs INT  Number of games to run
      --log FILE  Specify a log file (default will print to terminal)
      -rt         Execute Run-Time analysis (default is Cuttoff Search vs
                  ForwardPruning)
      -mu         Execute Memory Usage analysis (default is Cuttoff Search vs
                  ForwardPruning)
      -vs         Execute Forward Pruning Versus Cuttoff Search Analysis
                  (Wins/Loss)
      -ff         Execute Forward Pruning Versus Itself Analysis (Wins/Loss)
      -cc         Execute Cuttoff Search Versus Itself Versus Analysis (Wins/Loss)
      -a INT      Specify an alpha value for Alpha-Beta Pruning
      -b INT      Specify a beta value for Alpha-Beta Pruning
      -R FLOAT    Specify a Remove ratio for Random Forward Pruning
      -d INT      Specify a cut-off depth for the AI algorithm
	  
	  
Note: If -vs, -rt, -mu are used in any combination, only those tests specified
will run instead of all of them.  Also, Memory Usage was measured in move count
since a single state exists across the whole game.  Move evaluation was the default
choice for Memory Usage.

If --log FILE, where FILE is a file name of *.txt or *.log, is used,
the output will be redirected to that file.  The FILE will be overwritten
with the new information.

The metrics that can be adjusted for this program are the alpha, beta, depth, number
of runs, and ratio for Random  Forward Pruning.

The necessary files for this project are:
	__init__.py
	CuttingOff.py
	ForwardPruning.py
	State.py
	Driver.py
	Visualizer.py
	Test.py
	
The general approach to cutting off search was to implement it as close to the book's
implementation as possible.  Ofcourse, altercations had to be made to accommodate a
stochastic game.  My approach to Forward Pruning was to reuse CuttingOff Search, but
with a special modification.  That modification was to randomly choose a certain ratio 
of moves to completely skip.  This sped up CuttingOff Search at the cost of loosing
some precision.  However, you can argue how much precision would be lost when dealing
with imperfect real-time pruning.