class Bot2048:
    
    def __init__(self, agent=None):
        self.agent = agent
        self.board = [0 for i in range(16)]

    def getMaxTile(self):
        return max(self.board)

    def printBoard(self):
        ''' board indices
        0  | 1  | 2  | 3
        ----------------
        4  | 5  | 6  | 7
        ----------------
        8  | 9  | 10 | 11
        ----------------
        12 | 13 | 14 | 15
        '''
        maxSize = len(str(self.getMaxTile()))
        blankZerosBoard = [val if val > 0 else " " for val in self.board]
        for idx, tileValue in enumerate(blankZerosBoard):
            print(end=" ")
            if (idx+1) % 4 == 0:
                print(tileValue)
                print(((maxSize+2)*4+3)*'-')
            else:
                print(tileValue, end=(maxSize-len(str(tileValue))+1)*" ")
                print("|", end="")
        print()


    def resetBoard(self):
        self.board = [0 for i in range(16)]
    


