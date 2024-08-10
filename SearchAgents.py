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

class Agent:
    
    def getMove(self, board, legalMoves):
        return
    
    def testMove(self, board, legalMoves):
        return
        

class Random(Agent):

    def __str__(self):
        return 'Random Search'

    def getMove(self, board, legalMoves):
        if len(legalMoves) > 0:
            return legalMoves[rand.integers(0, len(legalMoves))]
        
    def testMove(self, board, legalMoves):
        print("Initial Board:")
        print(board)
        if len(legalMoves) > 0:
            print("Returned move: ", legalMoves[rand.integers(0, len(legalMoves))].__name__)
        
class Priority(Agent):

    def __str__(self):
        return 'Basic Search'

    def getMove(self, board, legalMoves):
        if len(legalMoves) > 0:
            return legalMoves[0]
        
    def testMove(self, board, legalMoves):
        print("Initial Board:")
        print(board)
        if len(legalMoves) > 0:
            print("Returned move: ", legalMoves[0].__name__)
        
class Reflex(Agent):

    def __init__(self, evaluationFunction=ef.defaultEval):
        self.evaluationFunction = evaluationFunction

    def __str__(self):
        return 'Reflex Search'

    def getMove(self, board, legalMoves):
        legalMoves = getLegalMoves(board)
        if len(legalMoves) > 0:
            movedBoards = [moveFunction(np.array(board)) for moveFunction in legalMoves]
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

class Search(Agent):

    def __init__(self, evaluationFunction, maxDepth=1):
        self.evaluationFunction = evaluationFunction
        self.maxDepth = maxDepth
        self.movesDict = dict()
        self.hashesDict = dict()

    def __str__(self):
        return 'Search'
    
    def getMove(self, board, legalMoves):
        if len(legalMoves) == 1:
            return legalMoves[0]
        if hashedBoard:=gb.hashInt(board) in self.movesDict.keys():
            return self.movesDict[gb.hashInt(board)]
        moveValues = [self.search(moveDirection(np.array(board)), False, 1) for moveDirection in legalMoves]
        self.movesDict[hashedBoard] = legalMoves[moveValues.index(max(moveValues))]
        return self.movesDict[hashedBoard]
    
    def search(self) -> float:
        pass

class Expectimax(Search):

    def __init__(self, evaluationFunction=ef.cornerSnakeStrength, maxDepth=1, newTileFrac=1, newTileMax=8):
        super().__init__(evaluationFunction, maxDepth)
        self.newTileFrac = newTileFrac
        self.newTileMax = newTileMax

    def __str__(self):
        return 'Expectimax'
    
    def search(self, board, maxPlayer:bool, curDepth) -> float:
        print("yeea")
        if curDepth > self.maxDepth:
            
            if hashedBoard:=gb.hashInt(board) in self.hashesDict.keys():
                #print("maxDepth in dict: ", time.time()-time0)
                return self.hashesDict[hashedBoard]
            else:
                self.hashesDict[hashedBoard] = self.evaluationFunction(board)
                #print("maxDepth evalued: ", time.time()-time0)
                return self.hashesDict[hashedBoard]
        if np.count_nonzero(board) < 16 and not maxPlayer:
            newTilesX, newTilesY = filterTileIndices(np.argwhere(board == 0))
            #numNewTiles = np.min([int(self.newTileFrac*np.count_nonzero(board==0)), self.newTileMax])
            boardValueSum = 0
            for i in range(len(newTilesX)):
                newBoard2 = np.array(board)
                newBoard2[newTilesX[i], newTilesY[i]] = 2
                boardValueSum += 0.9*self.search(newBoard2, True, curDepth)
                newBoard4 = np.array(board)
                newBoard4[newTilesX[i], newTilesY[i]] = 4
                boardValueSum += 0.1 * self.search(newBoard4, True, curDepth)
            #print("expectation calced: ", time.time()-time0)
            return boardValueSum / len(newTilesX)
        legalMoves = getLegalMoves(board)
        if len(legalMoves) == 0: 
            #print("no moves for maxPlayer: ", time.time()-time0)
            return 0
        movedBoardValues = [self.search(moveFunction(np.array(board)), False, curDepth+1) for moveFunction in legalMoves]
        #print("maxPlayer calced: ", time.time()-time0)
        return max(movedBoardValues)

class ExpectimaxAlpha(Search):

    def __init__(self, evaluationFunction=ef.cornerSnakeStrength, maxDepth=1, newTileFrac=1, newTileMax=8):
        super().__init__(evaluationFunction, maxDepth)
        self.newTileFrac = newTileFrac
        self.newTileMax = newTileMax

    def __str__(self):
        return 'Expectimax Alpha pruning'

    def search(self, board, maxPlayer:bool, curDepth, alpha:float=float('-inf')) -> float:

        print("Expectimax at alpha ", alpha)
        if curDepth > self.maxDepth:
            hashedBoard = gb.hashInt(board)
            if hashedBoard in self.hashesDict.keys():
                return self.hashesDict[hashedBoard]
            else:
                self.hashesDict[hashedBoard] = self.evaluationFunction(board)
                return self.hashesDict[hashedBoard]
        if np.count_nonzero(board) < 16 and not maxPlayer:
            newTilesX, newTilesY = filterTileIndices(np.argwhere(board == 0))
            #numNewTiles = np.min([int(self.newTileFrac*np.count_nonzero(board==0)), self.newTileMax])
            boardValueSum = 0
            for i in range(len(newTilesX)):
                newBoard2 = np.array(board)
                newBoard2[newTilesX[i], newTilesY[i]] = 2
                boardValueSum += 0.9*self.search(newBoard2, True, curDepth, float('-inf'))
                newBoard4 = np.array(board)
                newBoard4[newTilesX[i], newTilesY[i]] = 4
                boardValueSum += 0.1 * self.search(newBoard4, True, curDepth, float('-inf'))
                if alpha > (boardValueSum + 12*(len(newTilesX)-i-1))/len(newTilesX):
                    return boardValueSum / (i+1)
            return boardValueSum / len(newTilesX)
        legalMoves = getLegalMoves(board)
        if len(legalMoves) == 0: 
            return -1000
        for move in legalMoves:
            v = self.search(move(board), False, curDepth+1, alpha)
            alpha = max(alpha, v)
        return alpha

class MinimaxAlphaBeta(Search):

    def __init__(self, evaluationFunction=ef.cornerSnakeStrength, maxDepth=1):
        super().__init__(evaluationFunction, maxDepth)
        
    def __str__(self):
        return 'Minimax Alpha Beta pruning'
    
    def search(self, board, maxPlayer:bool, curDepth, alpha:float=float('-inf'), beta:float=float('inf')) -> float:
       
        print("Minimax at depth ", curDepth, "with alpha: ", alpha, ", beta: ", beta)
        if curDepth > self.maxDepth:
            hashedBoard = gb.hashInt(board)
            if hashedBoard in self.hashesDict.keys():
                return self.hashesDict[hashedBoard]
            else:
                self.hashesDict[hashedBoard] = self.evaluationFunction(board)
                return self.hashesDict[hashedBoard]
        legalMoves = getLegalMoves(board)
        if len(legalMoves) == 0: 
            return 0
        if not maxPlayer:
            newTilesX, newTilesY = filterTileIndices(np.argwhere(board == 0))
            for i in range(len(newTilesX)):
                if beta < alpha:
                    return beta
                newBoard = np.array(board)
                newBoard[newTilesX[i], newTilesY[i]] = 2
                v = self.search(newBoard, True, curDepth, alpha, beta)
                beta = min(beta, v)
            return beta
        else:
            for move in legalMoves:
                if alpha > beta:
                    return alpha
                v = self.search(move(np.array(board)), False, curDepth+1, alpha, beta)
                alpha = max(alpha, v)
            return alpha



   
   