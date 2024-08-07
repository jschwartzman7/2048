from constants import maxExponent, primeBoard, rand, np
from searchAgents import moves, stringToMove

def hashInt(board:np.ndarray) -> int:
    lBoard = np.copy(board)
    lBoard[lBoard == 0] = 1
    return np.prod(np.power(primeBoard, np.log2(lBoard)))

def randomStartingBoard() -> np.ndarray:
    board = np.zeros(16, dtype=int)
    board[rand.choice(16, size=2, replace=False)] = rand.choice([2,4], size=2, p=[0.9,0.1])
    return board.reshape(4,4)

def randomPositions(tileset:np.ndarray) -> np.ndarray:
    board = np.zeros(16)
    indices = rand.choice(16, size=len(tileset), replace=False)
    for i, idx in enumerate(indices):
        board[idx] = tileset[i]
    return board.reshape(4,4)

def randomTestBoardUniform(maxTileExponent:int=maxExponent, numFilled=None) -> np.ndarray:
    possibleExponents = np.arange(1, maxTileExponent+1)
    board = np.zeros(16, dtype=int)
    if numFilled == None:
        numFilled = rand.choice(17)
    tileIndices = rand.choice(16, size=numFilled, replace=False)
    board[tileIndices] = np.power(2, rand.choice(possibleExponents, size=numFilled))
    return moves[rand.choice(4)](board.reshape(4,4))
    
def randomTestBoardWeighted(maxTileExponent:int=maxExponent, numFilled:int=None) -> np.ndarray:
    possibleExponents = np.arange(1, maxTileExponent+1)
    board = np.zeros(16, dtype=int)
    if numFilled == None:
        numFilled = rand.choice(17)
    tileIndices = rand.choice(16, size=numFilled, replace=False)
    board[tileIndices] = np.power(2, rand.choice(possibleExponents, size=numFilled, p = possibleExponents[::-1]/np.sum(possibleExponents)))
    return board.reshape(4,4)

def generatePiece(board:np.ndarray) -> np.ndarray:
    #emptyCords = np.nonzero(board==0)
    emptyCords = np.argwhere(board == 0)
    if emptyCords.size > 0:
        newIdx = rand.choice(emptyCords)
        board[newIdx[0],newIdx[1]] = rand.choice([2,4], p=[0.9,0.1])
        #board[emptyCords[0][newIdx],emptyCords[1][newIdx]] = rand.choice([2,4], p=[0.9,0.1])
    return board


'''
    
def printBoard(board):
    
    0  | 1  | 2  | 3
    ----------------
    4  | 5  | 6  | 7
    ----------------
    8  | 9  | 10 | 11
    ----------------
    12 | 13 | 14 | 15
    
    maxSize = len(str(max(board)))
    blankZerosBoard = [val if val > 0 else "" for val in board]
    for idx, tileValue in enumerate(blankZerosBoard):
        print(end=" ")
        if (idx+1) % 4 == 0:
            print(tileValue)
            print(((maxSize+2)*4+3)*'-')
        else:
            print(tileValue, end=(maxSize-len(str(tileValue))+1)*" ")
            print("|", end="")'''
