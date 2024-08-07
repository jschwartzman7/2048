import evaluationFunctions as ef
import gameBoard as gb
from constants import rand, np
import time

'''
    0  | 1  | 2  | 3
    ----------------
    4  | 5  | 6  | 7
    ----------------
    8  | 9  | 10 | 11
    ----------------
    12 | 13 | 14 | 15
'''

def canMoveUp(board:np.ndarray) -> bool:
    return not np.array_equal(board, moveUp(board))

def canMoveDown(board:np.ndarray) -> bool:
    return not np.array_equal(board, moveDown(board))

def canMoveRight(board:np.ndarray) -> bool:
    return not np.array_equal(board, moveRight(board))

def canMoveLeft(board:np.ndarray) -> bool:
    return not np.array_equal(board, moveLeft(board))

def moveUp(board:np.ndarray) -> np.ndarray: # board = np.array().shape=(4, 4)
    return np.apply_along_axis(shiftedArray, 0, board)

def moveDown(board:np.ndarray) -> np.ndarray:
    return np.flipud(np.apply_along_axis(shiftedArray, 0, np.flipud(board)))

def moveRight(board:np.ndarray) -> np.ndarray:
    return np.fliplr(np.apply_along_axis(shiftedArray, 1, np.fliplr(board)))

def moveLeft(board:np.ndarray) -> np.ndarray:
    return np.apply_along_axis(shiftedArray, 1, board)

def shiftedArray(array:np.ndarray) -> np.ndarray:
    ''' Applies a single swipe move to the 1D array'''
    
    shiftedArray = array[array!=0]
    if len(shiftedArray) == 0:
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


moves = [moveUp, moveDown, moveRight, moveLeft]

stringToMove = {'down': {'move': moveDown, 'can': canMoveDown}, 'right': {'move': moveRight, 'can': canMoveRight}, 'left': {'move': moveLeft, 'can': canMoveLeft}, 'up': {'move': moveUp, 'can': canMoveUp}}

def canMoveInDirection(directionInput:str, board:np.ndarray) -> bool:
    if directionInput in stringToMove:
        return stringToMove[directionInput]['can'](board)
    return None

def moveInDirection(directionInput:str):
    if directionInput in stringToMove:
        return stringToMove[directionInput]['move']
    return None

def getLegalMoves(board):
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
    . [0,0]
    . [0,1]
    . [0,2]
    . [0,3]
    . [1,0]
    . [1,1]
    . [1,2]
    .]
    Return MINIMUM number of indices such that each empty row and column is accounted for
    '''

    emptyXCounts = {x: np.count_nonzero(emptyIndices[:,0]==x) for x in np.unique(emptyIndices[:,0])}
    emptyYCounts = {y: np.count_nonzero(emptyIndices[:,1]==y) for y in np.unique(emptyIndices[:,1])}
    uniqueEmptyIndices = [v for v in emptyIndices if emptyXCounts[v[0]] == 1 and emptyYCounts[v[1]] == 1]
    selectedIndices = [[v[0] for v in uniqueEmptyIndices],[v[1] for v in uniqueEmptyIndices]]
    print("initially selected: ", selectedIndices)
    missingRows = np.setdiff1d(emptyIndices[:,0], selectedIndices[0])
    missingColumns = np.setdiff1d(emptyIndices[:,1], selectedIndices[1])
    while missingRows.size > 0 or missingColumns.size > 0:
        if missingRows.size > 0:
            newXIdx = sorted(missingRows, key=lambda v:emptyXCounts[v])[0]
            emptyXCounts[newXIdx] -= 1
            possibleYs = np.unique(emptyIndices[emptyIndices[:,0]==newXIdx][:,1])
            goodYs = possibleYs[np.isin(possibleYs, missingColumns)]
            if np.any(goodYs):
                newYIdx = sorted(goodYs, key=lambda y: emptyYCounts[y])[0]
            else:
                newYIdx = sorted(possibleYs, key=lambda y: emptyYCounts[y])[0]
            emptyYCounts[newYIdx] -= 1
        else:
            newYIdx = sorted(missingColumns, key=lambda v:emptyYCounts[v])[0]
            emptyYCounts[newYIdx] -= 1
            possibleXs = np.unique(emptyIndices[emptyIndices[:,1]==newYIdx][:,0])
            goodXs = possibleXs[np.isin(possibleXs, missingRows)]
            if np.any(goodXs):
                newXIdx = sorted(goodXs, key=lambda x: emptyXCounts[x])[0]
            else:
                newXIdx = sorted(possibleXs, key=lambda x: emptyXCounts[x])[0]
            emptyXCounts[newXIdx] -= 1
        selectedIndices[0].append(newXIdx)
        selectedIndices[1].append(newYIdx)
        missingRows = np.setdiff1d(missingRows, selectedIndices[0])
        missingColumns = np.setdiff1d(missingColumns, selectedIndices[1])
    return selectedIndices


class Search:
    
    def getMove(self, board, legalMoves):
        return
    
    def testMove(self, board, legalMoves):
        return
        

class RandomSearch(Search):

    def __str__(self):
        return 'Random Search'

    def getMove(self, board, legalMoves):
        if len(legalMoves) > 0:
            return legalMoves[random.randint(0, len(legalMoves)-1)]
        
    def testMove(self, board, legalMoves):
        print("Initial Board:")
        print(board)
        legalMoves = self.getLegalMoves(board)
        if len(legalMoves) > 0:
            print("Returned move: ", moveToString[legalMoves[random.randint(0, len(legalMoves)-1)]])
        
class BasicSearch(Search):

    def __str__(self):
        return 'Basic Search'

    def getMove(self, board, legalMoves):
        legalMoves = self.getLegalMoves(board)
        if len(legalMoves) > 0:
            return legalMoves[0]
        
    def testMove(self, board, legalMoves):
        print("Initial Board:")
        print(board)
        legalMoves = self.getLegalMoves(board)
        if len(legalMoves) > 0:
            print("Returned move: ", moveToString[legalMoves[0]])
        
class ReflexSearch(Search):

    def __init__(self, evaluationFunction=ef.defaultEval):
        self.evaluationFunction = evaluationFunction

    def __str__(self):
        return 'Reflex Search'

    def getMove(self, board, legalMoves):
        legalMoves = getLegalMoves(board)
        if len(legalMoves) > 0:
            movedBoards = [moveFunction(board.copy()) for moveFunction in legalMoves]
            movedBoardValues = [self.evaluationFunction(board) for board in movedBoards]
            return legalMoves[movedBoardValues.index(max(movedBoardValues))]
        
    def testMove(self, board, legalMoves):
        print("Initial Board:")
        print(board)
        legalMoves = getLegalMoves(board)
        if len(legalMoves) > 0:
            movedBoards = []
            for move in legalMoves:
                print("Just moved ", moveToString[move])
                movedBoards.append(move(board.copy()))
                print(movedBoards[-1])
                print("Board Value = ", self.evaluationFunction(movedBoards[-1]))
                print()
            movedBoardValues = [self.evaluationFunction(board) for board in movedBoards]
            print("Returned move: ", moveToString[legalMoves[movedBoardValues.index(max(movedBoardValues))]])

class ExpectimaxSearch(Search):

    def __init__(self, evaluationFunction=ef.defaultEval, maxDepth=3, newTileFrac=1, newTileMax=15):
        self.evaluationFunction = evaluationFunction
        self.maxDepth = maxDepth
        self.newTileFrac = newTileFrac
        self.newTileMax = newTileMax
        self.movesDict = dict()
        self.hashesDict = dict()

    def __str__(self):
        return 'Expectimax Search'

    def getMove(self, board, legalMoves):
        '''Expectimax with "Player" and "Chance" turns
            Player can go Up, Down, Left, Right
            Chance has 90% chance of spawning a 2 in a random unoccupied location and 10% chance of spawing a 4
            legalMoves passed in is non-empty
        '''

        if len(legalMoves) == 1:
            return legalMoves[0]
        if hashedBoard:=gb.hashInt(board) in self.movesDict.keys():
            return self.movesDict[hashedBoard]
        moveValues = [self.expectimax(moveDirection(np.copy(board)), False, 1) for moveDirection in legalMoves]
        self.movesDict[hashedBoard] = legalMoves[moveValues.index(max(moveValues))]
        return self.movesDict[hashedBoard]
    



    def expectimax(self, board, maxPlayer:bool, curDepth) -> float:
        #print("Expectimax at depth ", curDepth)
        time0 = time.time()
        if curDepth > self.maxDepth:
            
            if hashedBoard:=gb.hashInt(board) in self.hashesDict.keys():
                #print("maxDepth in dict: ", time.time()-time0)
                return self.hashesDict[hashedBoard]
            else:
                self.hashesDict[hashedBoard] = self.evaluationFunction(board)
                #print("maxDepth evalued: ", time.time()-time0)
                return self.hashesDict[hashedBoard]
        if np.count_nonzero(board) < 16 and not maxPlayer:
            numNewTiles = np.min([int(self.newTileFrac*np.count_nonzero(board==0)), self.newTileMax])
            if numNewTiles > 0:
                newTileIndices = rand.choice(np.argwhere(board == 0), size=numNewTiles, replace=False)
                boardValueSum = 0
                for row,col in newTileIndices:
                    newBoard2 = np.array(board)
                    newBoard2[row,col] = 2
                    boardValueSum += 0.9*self.expectimax(newBoard2, True, curDepth)
                    newBoard4 = np.array(board)
                    newBoard4[row,col] = 4
                    boardValueSum += 0.1 * self.expectimax(newBoard4, True, curDepth)
                #print("expectation calced: ", time.time()-time0)
                return boardValueSum / newTileIndices.shape[0]
        legalMoves = getLegalMoves(board)
        if len(legalMoves) == 0: 
            #print("no moves for maxPlayer: ", time.time()-time0)
            return -1000
        movedBoardValues = [self.expectimax(moveFunction(np.array(board)), False, curDepth+1) for moveFunction in legalMoves]
        #print("maxPlayer calced: ", time.time()-time0)
        return max(movedBoardValues)

class ExpectimaxAlphaSearch(Search):

    def __init__(self, evaluationFunction=ef.defaultEval, maxDepth=3, newTileFrac=1, newTileMax=15):
        self.evaluationFunction = evaluationFunction
        self.maxDepth = maxDepth
        self.newTileFrac = newTileFrac
        self.newTileMax = newTileMax
        self.movesDict = dict()
        self.hashesDict = dict()
        self.rand = np.random.default_rng()

    def __str__(self):
        return 'Expectimax Alpha Search'

    def getMove(self, board, legalMoves):

        if len(legalMoves) == 1:
            return legalMoves[0]
        if gb.hashInt(board) in self.movesDict.keys():
            return self.movesDict[gb.hashInt(board)]
        moveValues = [self.expectimaxAlpha(moveDirection(np.copy(board)), False, 1, -100) for moveDirection in legalMoves]
        self.movesDict[gb.hashInt(board)] = legalMoves[moveValues.index(max(moveValues))]

        return self.movesDict[gb.hashInt(board)]
    
    def expectimaxAlpha(self, board, maxPlayer:bool, curDepth, alpha:float) -> float:

        #print("Expectimax at depth ", curDepth)
        if curDepth > self.maxDepth:
            hashedBoard = gb.hashInt(board)
            if hashedBoard in self.hashesDict.keys():
                return self.hashesDict[hashedBoard]
            else:
                self.hashesDict[hashedBoard] = self.evaluationFunction(board)
                return self.hashesDict[hashedBoard]
        if np.count_nonzero(board) < 16 and not maxPlayer:
            numNewTiles = np.min([int(self.newTileFrac*np.count_nonzero(board==0)), self.newTileMax])
            if numNewTiles > 0:
                newTileIndices = self.rand.choice(np.argwhere(board == 0), size=numNewTiles, replace=False)
                boardValueSum = 0
                for i in range(len(newTileIndices)):
                    row, col = newTileIndices[i]
                    newBoard2 = npCopy(board)
                    newBoard2[row,col] = 2
                    boardValueSum += 0.9*self.expectimaxAlpha(newBoard2, True, curDepth, float('-inf'))
                    newBoard4 = npCopy(board)
                    newBoard4[row,col] = 4
                    boardValueSum += 0.1 * self.expectimaxAlpha(newBoard4, True, curDepth, float('-inf'))
                    if alpha > (boardValueSum + 12*(len(newTileIndices)-i-1))/len(newTileIndices):
                            return boardValueSum / (i+1)
                return boardValueSum / newTileIndices.shape[0]
        legalMoves = getLegalMoves(board)
        if len(legalMoves) == 0: 
            return -1000
        for move in legalMoves:
            v = self.expectimaxAlpha(move(npCopy(board)), False, curDepth+1, alpha)
            alpha = max(alpha, v)
        return alpha


   