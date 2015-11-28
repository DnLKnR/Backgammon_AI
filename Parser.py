import re

def parseInputString(s):
    inputList = s.split()

    if (inputList[0] == "q"):
        return inputList

    else:
        for each item in inputList:
            re.match("\d/\d")
