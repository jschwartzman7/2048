import random
import math
import TestValues as t

def to2D(idx):
    '''
    (0,0) | (1,0) | (2,0) | (3,0)
    -----------------------------
    (0,1) | (1,1) | (2,1) | (3,1)
    -----------------------------
    (0,2) | (1,2) | (2,2) | (3,2)
    -----------------------------
    (0,3) | (1,3) | (2,3) | (3,3)
    '''
    return idx%4, idx//4

def randomBoard(maxTileExponent=t.maxExponent, numFilled=None):
    if numFilled != None:
        tileIndices = random.sample(range(16), numFilled)
        tileExponents = random.choices(range(1, maxTileExponent+1), weights=[1/i for i in range(1, maxTileExponent+1)], k=len(tileIndices))
        return [int(math.pow(2, tileExponents.pop(0))) if i in tileIndices else 0 for i in range(16)]
    return random.choices([int(math.pow(2, i)) if i > 0 else 0 for i in range(maxTileExponent+1)], weights=[1/i if i > 0 else 1 for i in range(maxTileExponent+1)], k=16)

def randomBoardUniform():
    f = lambda e: int(math.pow(2, e)) if e > 0 else 0
    return [f(random.randint(0, t.maxExponent+1)) for i in range(16)]


def generatePiece(board):
    emptyCords = emptyIndices(board)
    if len(emptyCords) > 0:
        board[random.choice(emptyCords)] = 2 if random.random() < .9 else 4
        return True
    return False

def emptyIndices(board):
    return [i for i in range(16) if board[i] == 0]

def printBoard(board):
    '''
    0  | 1  | 2  | 3
    ----------------
    4  | 5  | 6  | 7
    ----------------
    8  | 9  | 10 | 11
    ----------------
    12 | 13 | 14 | 15
    '''
    maxSize = len(str(max(board)))
    blankZerosBoard = [val if val > 0 else "" for val in board]
    for idx, tileValue in enumerate(blankZerosBoard):
        print(end=" ")
        if (idx+1) % 4 == 0:
            print(tileValue)
            print(((maxSize+2)*4+3)*'-')
        else:
            print(tileValue, end=(maxSize-len(str(tileValue))+1)*" ")
            print("|", end="")
