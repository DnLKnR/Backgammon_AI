from State import State
from CuttingOff import CuttingOff
from ForwardPruning import ForwardPruning
#Start board
#    0 1 2 3 4 5 6 7 8 910 1 2 3 4 5 6 7 8 920 1 2 3 4
#r = [0,2,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,3,0,5,0,0,0,0,0]
#w = [0,0,0,0,0,0,5,0,3,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,2]
#    0 1 2 3 4 5 6 7 8 910 1 2 3 4 5 6 7 8 920 1 2 3 4
r = [0,0,0,3,0,0,0,0,2,0,4,0,0,0,0,0,0,0,0,0,0,0,2,0,0]
w = [2,0,0,0,0,0,3,0,0,0,0,5,0,0,0,0,0,0,2,0,0,0,0,0,0]

s = State(r, w)

a = s.actions(1, None)

CO = CuttingOff(193, 2, 4)
FP = ForwardPruning(193, 2, 3)
print("Action from search: " + str(CO.Search(s,0,[1,3])))
print("Action from search: " + str(FP.Search(s,0,[1,3])))
'''
def printArray(array):
    for i,row in enumerate(array):
        for j,row2 in enumerate(row):
            print("------------- Dice Roll {0},{1} or {1},{0} -------------".format(i + 1,j + 1))
            for index,actionset in enumerate(row2):
                print("Option {0}:\t{1}".format(index + 1,actionset))

printArray(a)



print("current score " + str(s.score(r,[r,w], 0)))'''