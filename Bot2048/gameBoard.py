from Bot2048.constants import maxExponent, primeBoard, rand, np

def hashInt(board:np.ndarray) -> int:
    return np.prod(np.power(primeBoard, np.log2(board, where=board>0)))

def randomStartingBoard() -> np.ndarray:
    board = np.zeros(16, dtype=np.uint16)
    board[rand.choice(16, size=2, replace=False)] = rand.choice([2,4], size=2, p=[0.9,0.1])
    return board.reshape(4,4)

def randomPositions(tileset:np.ndarray) -> np.ndarray:
    board = np.zeros(16, dtype=np.uint16)
    indices = rand.choice(16, size=len(tileset), replace=False)
    for i, idx in enumerate(indices):
        board[idx] = tileset[i]
    return board.reshape(4,4)

def randomTestBoardUniform(maxTileExponent:int=maxExponent, numFilled=None) -> np.ndarray:
    possibleExponents = np.arange(1, maxTileExponent+1)
    board = np.zeros(16, dtype=np.uint16)
    if numFilled == None:
        numFilled = rand.choice(17)
    tileIndices = rand.choice(16, size=numFilled, replace=False)
    board[tileIndices] = np.power(2, rand.choice(possibleExponents, size=numFilled))
    return board.reshape(4,4)
    
def randomTestBoardWeighted(maxTileExponent:int=maxExponent, numFilled:int=None) -> np.ndarray:
    possibleExponents = np.arange(1, maxTileExponent+1)
    board = np.zeros(16, dtype=np.uint16)
    if numFilled == None:
        numFilled = rand.choice(17)
    tileIndices = rand.choice(16, size=numFilled, replace=False)
    board[tileIndices] = np.power(2, rand.choice(possibleExponents, size=numFilled, p = possibleExponents[::-1]/np.sum(possibleExponents)))
    return board.reshape(4,4)

def generatePiece(board:np.ndarray) -> np.ndarray:
    if board[board==0].size == 0:
        return board
    board[tuple(rand.choice(np.argwhere(board == 0)))] = rand.choice([2,4], p=[0.9,0.1])
    return board

if __name__ == "__main__":
    pass