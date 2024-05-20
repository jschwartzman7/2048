import random

class GameBoard:
    
    def __init__(self, initialBoard=[0]*16):
        self.board = initialBoard

    def getMaxTile(self):
        return max(self.board)
    
    def getSumTiles(self):
        return sum(self.board)

    def getEmptyIndices(self):
        return [i for i in range(16) if self.board[i] == 0]

    def generatePiece(self):
        emptyCords = self.getEmptyIndices()
        if len(emptyCords) > 0:
            self.board[random.sample(emptyCords, 1)[0]] = 2 if random.random() < .9 else 4

    def get2DCord(idx):
        ''' board indices
        (0,0) | (1,0) | (2,0) | (3,0)
        -----------------------------
        (0,1) | (1,1) | (2,1) | (3,1)
        -----------------------------
        (0,2) | (1,2) | (2,2) | (3,2)
        -----------------------------
        (0,3) | (1,3) | (2,3) | (3,3)
        '''
        return idx%4, idx//4

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
        blankZerosBoard = [val if val > 0 else "" for val in self.board]
        for idx, tileValue in enumerate(blankZerosBoard):
            print(end=" ")
            if (idx+1) % 4 == 0:
                print(tileValue)
                print(((maxSize+2)*4+3)*'-')
            else:
                print(tileValue, end=(maxSize-len(str(tileValue))+1)*" ")
                print("|", end="")
        print()
