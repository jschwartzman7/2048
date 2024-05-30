import random
import math
import TestValues as t
import numpy as np

# Numpy: board is 1d ndarray of length 16

def to2D(idx):
    ''' (x, y)
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

def randomBoardNumpy(maxTileExponent=t.maxExponent, numFilled=None):
    exponents = np.arange(1, maxTileExponent+1)
    if numFilled == None:
        return np.power(2, np.random.choice(exponents, size=16, p=1/(exponents*np.sum(1/exponents)))).reshape(4, 4)
    tileIndices = np.random.choice(np.arange(16), size=numFilled, replace=False)
    return np.where(np.isin(np.arange(16), tileIndices), np.power(2, np.random.choice(exponents, size=16, p=1/(exponents*np.sum(1/exponents)))), 0).reshape(4, 4)
                            

def randomBoardUniform(maxTileExponent=t.maxExponent):
    f = lambda e: int(math.pow(2, e)) if e > 0 else 0
    return [f(random.randint(0, t.maxExponent+1)) for i in range(16)]

def randomBoardUniformNumpy(maxTileExponent=t.maxExponent):
    return np.power(2,x:=np.random.randint(0, t.maxExponent+1, size=16), where=x>0).reshape(4,4)

def generatePiece(board):
    emptyCords = emptyIndices(board)
    if len(emptyCords) > 0:
        board[random.choice(emptyCords)] = 2 if random.random() < .9 else 4
        return True
    return False

def emptyIndices(board):
    return [i for i in range(16) if board[i] == 0]
    

def emptyIndicesNumpy(board):
    return np.flatnonzero(board == 0)

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

