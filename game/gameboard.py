from utils import maxExponent, primeBoard, rand, np

def log2Board(board:np.ndarray) -> np.ndarray:
    return np.log2(board, where=board>0)

#def hashInt(board:np.ndarray) -> int:
    return np.prod(np.power(primeBoard, log2Board(board)))

def hashInt(board:np.ndarray) -> int:
    return hash(tuple(board.flatten()))

def canMoveUp(board:np.ndarray) -> bool:
    return not np.array_equal(board, moveUp(board))

def canMoveDown(board:np.ndarray) -> bool:
    return not np.array_equal(board, moveDown(board))

def canMoveRight(board:np.ndarray) -> bool:
    return not np.array_equal(board, moveRight(board))

def canMoveLeft(board:np.ndarray) -> bool:
    return not np.array_equal(board, moveLeft(board))

def moveUp(board:np.ndarray) -> np.ndarray:
    return np.apply_along_axis(shiftedArray, 0, board)

def moveDown(board:np.ndarray) -> np.ndarray:
    return np.flipud(np.apply_along_axis(shiftedArray, 0, np.flipud(board)))

def moveRight(board:np.ndarray) -> np.ndarray:
    return np.fliplr(np.apply_along_axis(shiftedArray, 1, np.fliplr(board)))

def moveLeft(board:np.ndarray) -> np.ndarray:
    return np.apply_along_axis(shiftedArray, 1, board)

def shiftedArray(array:np.ndarray) -> np.ndarray:
    ''' Returns a 1D array representing the input array after one swipe move'''
    # allocate an array that will be returned shifted
    shiftedArray = array[array!=0]
    if shiftedArray.size == 0:
        return array
    mergedIndices = set()
    idx = 1
    while idx < len(shiftedArray):
        if np.all(shiftedArray[idx:] == 0):
            break
        if idx == 0:
            idx += 1
        elif shiftedArray[idx-1] == 0:
            shiftedArray[idx], shiftedArray[idx-1] = 0, shiftedArray[idx]
            idx -= 1
        elif shiftedArray[idx] == shiftedArray[idx-1] and idx-1 not in mergedIndices:
            shiftedArray[idx], shiftedArray[idx-1] = 0, 2*shiftedArray[idx-1]
            mergedIndices.add(idx-1)
            idx += 1
        else:
            idx += 1
    return np.pad(shiftedArray, (0, 4-len(shiftedArray)))

# Down, Right, Left, Up order of moves
moveFunctions = [moveDown, moveRight, moveLeft, moveUp]

stringToMove = {
    'up': {'move': moveUp, 'can': canMoveUp},
    'down': {'move': moveDown, 'can': canMoveDown},
    'right': {'move': moveRight, 'can': canMoveRight},
    'left': {'move': moveLeft, 'can': canMoveLeft}
}

def canMoveInStrDirection(directionInput:str, board:np.ndarray) -> bool:
    if directionInput in stringToMove:
        return stringToMove[directionInput]['can'](board)
    print('Invalid direction input')
    return None

def getMoveDirectionStr(directionInput:str):
    if directionInput in stringToMove:
        return stringToMove[directionInput]['move']
    print('Invalid direction input')
    return None

def getLegalMoves(board:np.ndarray) -> list:
    #return [stringToMove[direction]['move'] for direction in ['up', 'down', 'right', 'left'] if stringToMove[direction]['can'](board)]
    legalMoves = []
    if canMoveDown(board): 
        legalMoves.append(moveDown)
    if canMoveRight(board): 
        legalMoves.append(moveRight)
    if canMoveLeft(board): 
        legalMoves.append(moveLeft)
    if canMoveUp(board): 
        legalMoves.append(moveUp)
    return legalMoves

def filterTileIndices(emptyIndices:np.ndarray) -> tuple:
    ''' tuple of empty tile indices n x 2
        Return MINIMUM number of indices such that each empty row and column is accounted for
    '''

    missingXCounts = {x: [np.count_nonzero(emptyIndices[:,0]==x), 1] for x in emptyIndices[:,0]}
    missingYCounts = {y: [np.count_nonzero(emptyIndices[:,1]==y), 1] for y in emptyIndices[:,1]}
    uniqueEmptyIndices = [v for v in emptyIndices if missingXCounts[v[0]][0] == 1 and missingYCounts[v[1]][0] == 1]
    selectedIndices = [[v[0] for v in uniqueEmptyIndices],[v[1] for v in uniqueEmptyIndices]]
    for v in uniqueEmptyIndices:
        missingXCounts[v[0]][1] = float('inf')
        missingYCounts[v[1]][1] = float('inf')
    while (not all([v[1] == float('inf') for v in missingXCounts.values()])) or (not all([v[1] == float('inf') for v in missingYCounts.values()])):
        if min([count*missing for count, missing in missingXCounts.values()]) < min([count*missing for count, missing in missingYCounts.values()]):
            newXIdx = sorted(missingXCounts.keys(), key=lambda x:missingXCounts[x][0]*missingXCounts[x][1])[0]
            missingXCounts[newXIdx] = [1, float('inf')]
            newYIdx = sorted(np.unique(emptyIndices[emptyIndices[:,0]==newXIdx][:,1]), key=lambda y:missingYCounts[y][0]*missingYCounts[y][1])[0]
            missingYCounts[newYIdx] = [1, float('inf')]
        else:
            newYIdx = sorted(missingYCounts.keys(), key=lambda y:missingYCounts[y][0]*missingYCounts[y][1])[0]
            missingYCounts[newYIdx] = [1, float('inf')]
            newXIdx = sorted(np.unique(emptyIndices[emptyIndices[:,1]==newYIdx][:,0]), key=lambda x:missingXCounts[x][0]*missingXCounts[x][1])[0]
            missingXCounts[newXIdx] = [1, float('inf')]
        selectedIndices[0].append(newXIdx)
        selectedIndices[1].append(newYIdx)
    assert len(selectedIndices[0]) == len(selectedIndices[1])
    return selectedIndices

def randomStartingBoard() -> np.ndarray:
    board = np.zeros(16, dtype=int)
    board[rand.choice(16, size=2, replace=False)] = rand.choice([2,4], size=2, p=[0.9,0.1])
    return board.reshape(4,4)

# watch out for integer overflow
def randomTestBoardWeighted(maxTileExponent:int=maxExponent, numFilled:int=None) -> np.ndarray:
    possibleExponents = np.arange(1, maxTileExponent+1)
    board = np.zeros(16)
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

def randomPositionedBoard(tileset:np.ndarray) -> np.ndarray:
    board = np.zeros(16)
    indices = rand.choice(16, size=len(tileset), replace=False)
    for i, idx in enumerate(indices):
        board[idx] = tileset[i]
    return board.reshape(4,4)
