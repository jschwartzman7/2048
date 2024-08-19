import Bot2048.evaluationFunctions as ef
from Bot2048.gameBoard import hashInt
from Bot2048.constants import rand, np
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

    def __str__(self):
        return 'Abstract Agent'
    
    def getMove(self, board, legalMoves):
        return
    

class Random(Agent):

    def __str__(self):
        return 'Random Agent'

    def getMove(self, board, legalMoves):
        return legalMoves[rand.integers(0, len(legalMoves))]
        
class Priority(Agent):

    def __str__(self):
        return 'Priority Agent'

    def getMove(self, board, legalMoves):
        return legalMoves[0]
        
class Reflex(Agent):
    
    def __init__(self, evaluationFunction=ef.cornerStrength):
        self.evaluationFunction = evaluationFunction

    def __str__(self):
        return 'Reflex Agent'

    def getMove(self, board, legalMoves):
        return legalMoves[np.argmax([self.evaluationFunction(moveFunction(board)) for moveFunction in legalMoves])]
    
class Search(Agent):

    def __init__(self, evaluationFunction, maxDepth):
        self.evaluationFunction = evaluationFunction
        self.maxDepth = maxDepth
        self.calculatedMoves = dict()
        self.hashedBoardEvaluations = dict()

    def __str__(self):
        return 'Base Search Agent'
    
    def getMove(self, board, legalMoves):
        print("base agent getting move")
        if len(legalMoves) == 1:
            return legalMoves[0]
        if hashedBoard:=hashInt(board) in self.calculatedMoves.keys():
            return self.calculatedMoves[hashInt(board)]
        moveValues = [self.search(moveDirection(board), False, 1) for moveDirection in legalMoves]
        self.calculatedMoves[hashedBoard] = legalMoves[moveValues.index(max(moveValues))]
        return self.calculatedMoves[hashedBoard]
    
    def search(self) -> float:
        pass

class Expectimax(Search):

    def __init__(self, evaluationFunction=ef.cornerSnakeStrength, maxDepth=2, newTileFrac=1, newTileMax=16):
        super().__init__(evaluationFunction, maxDepth)
        self.newTileFrac = newTileFrac
        self.newTileMax = newTileMax

    def __str__(self):
        return 'Expectimax Search Agent'
    
    def search(self, board, maxPlayer:bool, curDepth) -> float:
        if curDepth > self.maxDepth:
            
            if hashedBoard:=hashInt(board) in self.hashedBoardEvaluations.keys():
                #print("maxDepth in dict: ", time.time()-time0)
                return self.hashedBoardEvaluations[hashedBoard]
            else:
                self.hashedBoardEvaluations[hashedBoard] = self.evaluationFunction(board)
                #print("maxDepth evalued: ", time.time()-time0)
                return self.hashedBoardEvaluations[hashedBoard]
        if np.count_nonzero(board) < 16 and not maxPlayer:
            newTilesX, newTilesY = filterTileIndices(np.argwhere(board == 0))
            #numNewTiles = np.min([int(self.newTileFrac*np.count_nonzero(board==0)), self.newTileMax])
            boardExpectedValue = 0
            for i in range(len(newTilesX)):
                board[newTilesX[i], newTilesY[i]] = 2
                boardExpectedValue += 0.9*self.search(board, True, curDepth+1)
                board[newTilesX[i], newTilesY[i]] = 4
                boardExpectedValue += 0.1 * self.search(board, True, curDepth+1)
                board[newTilesX[i], newTilesY[i]] = 0
            #print("expectation calced: ", time.time()-time0)
            return boardExpectedValue / len(newTilesX)
        legalMoves = getLegalMoves(board)
        if len(legalMoves) == 0: 
            #print("no moves for maxPlayer: ", time.time()-time0)
            return 0
        movedBoardValues = [self.search(moveFunction(np.array(board)), False, curDepth+1) for moveFunction in legalMoves]
        #print("maxPlayer calced: ", time.time()-time0)
        return max(movedBoardValues)

class ExpectimaxAlpha(Search):

    def __init__(self, evaluationFunction=ef.cornerSnakeStrength, maxDepth=2, newTileFrac=1, newTileMax=16):
        super().__init__(evaluationFunction, maxDepth)
        self.newTileFrac = newTileFrac
        self.newTileMax = newTileMax

    def __str__(self):
        return 'Expectimax Alpha Pruning Search Agent'

    def search(self, board, maxPlayer:bool, curDepth, alpha:float=float('-inf')) -> float:
        if curDepth > self.maxDepth:
            hashedBoard = hashInt(board)
            if hashedBoard in self.hashedBoardEvaluations.keys():
                return self.hashedBoardEvaluations[hashedBoard]
            else:
                self.hashedBoardEvaluations[hashedBoard] = self.evaluationFunction(board)
                return self.hashedBoardEvaluations[hashedBoard]
        if np.count_nonzero(board) < 16 and not maxPlayer:
            newTilesX, newTilesY = filterTileIndices(np.argwhere(board == 0))
            #numNewTiles = np.min([int(self.newTileFrac*np.count_nonzero(board==0)), self.newTileMax])
            boardExpectedValue = 0
            for i in range(len(newTilesX)):
                board[newTilesX[i], newTilesY[i]] = 2
                boardExpectedValue += 0.9*self.search(board, True, curDepth+1, float('-inf'))
                board[newTilesX[i], newTilesY[i]] = 4
                boardExpectedValue += 0.1 * self.search(board, True, curDepth+1, float('-inf'))
                board[newTilesX[i], newTilesY[i]] = 0
                # If the upper bound of final boardValueSum is less than alpha (current best move), return
                if maxBvs:=(boardExpectedValue + ef.M*(len(newTilesX)-i-1))/len(newTilesX) < alpha:
                    return maxBvs
            return boardExpectedValue / len(newTilesX)
        legalMoves = getLegalMoves(board)
        if len(legalMoves) == 0: 
            return 0
        for move in legalMoves:
            v = self.search(move(board), False, curDepth+1, alpha)
            alpha = max(alpha, v)
        return alpha

class MinimaxAlphaBeta(Search):

    def __init__(self, evaluationFunction=ef.cornerSnakeStrength, maxDepth=2):
        super().__init__(evaluationFunction, maxDepth)
        
    def __str__(self):
        return 'Minimax Alpha Beta Pruning Search Agent'
    
    def search(self, board, maxPlayer:bool, curDepth, alpha:float=float('-inf'), beta:float=float('inf')) -> float:
       
       # print("Minimax at depth ", curDepth, "with alpha: ", alpha, ", beta: ", beta)
        if curDepth > self.maxDepth:
            hashedBoard = hashInt(board)
            if hashedBoard in self.hashedBoardEvaluations.keys():
                return self.hashedBoardEvaluations[hashedBoard]
            else:
                self.hashedBoardEvaluations[hashedBoard] = self.evaluationFunction(board)
                return self.hashedBoardEvaluations[hashedBoard]
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
                v = self.search(newBoard, True, curDepth+1, alpha, beta)
                beta = min(beta, v)
            return beta
        else:
            for move in legalMoves:
                if alpha > beta:
                    return alpha
                v = self.search(move(np.array(board)), False, curDepth+1, alpha, beta)
                alpha = max(alpha, v)
            return alpha
        
'''
Expecti/Mini Max (ab pruning)
    cost grows exponentially with tree depth
    cannot visit all chance nodes up to depth in time
    must filter tile indices to reduce branching factor



MCTS
    cost grows linearly with tree depth
    random rollouts take advantage of chance nodes
        no need to visit all chance nodes
'''

class GamestateNode():

    nodeCount = 0

    def __init__(self, board:np.ndarray, legalMoves, parent=None):
        self.board = board
        self.numVisits = 0
        self.scoreSum = 0
        self.parent = parent
        self.children = {move : None for move in legalMoves}
        self.id = GamestateNode.nodeCount
        GamestateNode.nodeCount += 1

    def calculateUCT(self, explorationConstant:float):
        '''returns the UCT value of the node, assumes parent is not None'''
        if self.numVisits == 0:
            return float('inf')
        return self.scoreSum/self.numVisits + explorationConstant*np.sqrt(np.log(self.parent.numVisits)/self.numVisits)

    def getDepth(self):
        if len(self.children) == 0 or all([child == None for child in self.children.values()]):
            return 0
        return 1 + max([child.getDepth() for child in self.children.values() if child != None])


class MCTSAgent(Agent):
    '''
    Monte Carlo Tree Search Agent

    Move stages:
        s0 = current state, root of tree
        traverse to a leaf node descendant s1 of s0 based on UCT bound
        expand s1 by adding its successor state(s) c() to tree
        perform rollouts from c(), keeping track of scores
        backpropagate scores from c() up to root s0
    '''

    def __init__(self, explorationConstant=np.sqrt(2), moveTimeLimit=2):
        self.explorationConstant = explorationConstant
        self.timeToMove = moveTimeLimit
        self.searchTreeRoots = []

    def rollout(self, state:GamestateNode):
        '''simulates a random game starting from 'state' and returns final score'''
        rolloutBoard = np.array(state.board)
        while len(legalMoves:=getLegalMoves(rolloutBoard)) > 0:
            rolloutBoard = legalMoves[rand.integers(0, len(legalMoves))](rolloutBoard)
            rolloutBoard[tuple(rand.choice(np.argwhere(rolloutBoard == 0)))] = rand.choice([2,4], p=[0.9,0.1])    
        return rolloutBoard.max()
    
    def backPropagate(self, state:GamestateNode, score:int):
        '''updates the scoreSum and numVisits fields of 'state' and all its ancestors'''
        
        curNode = state
        while curNode != None:
            curNode.numVisits += 1
            curNode.scoreSum += score
            curNode = curNode.parent

    def getChild(self, state:GamestateNode, moveFunction):
        '''generates a successor of state after moveFunction and a random new piece'''
        (movedBoard:=moveFunction(state.board))[tuple(rand.choice(np.argwhere(movedBoard == 0)))] = rand.choice([2,4], p=[0.9,0.1])    
        return GamestateNode(movedBoard, getLegalMoves(movedBoard), parent=state)

    def getNewChildNode(self, state:GamestateNode):
        curNode = state
        while all([child != None for child in curNode.children.values()]) and len(curNode.children) > 0:
            #curNode = sorted(curNode.children.values(), key=lambda child: child.calculateUCT(self.explorationConstant))[-1]
            curNode = max([child for child in curNode.children.values()], key=lambda child: child.calculateUCT(self.explorationConstant))
        if len(curNode.children) == 0:
            return curNode
        unexploredMoves = [move for move in curNode.children.keys() if curNode.children[move] == None]
        curNode.children[move] = self.getChild(curNode, move:=rand.choice(unexploredMoves))
        return curNode.children[move]
       
    def runMCTSonce(self, state:GamestateNode):
        '''runs one iteration of MCTS from "state"'''

        # add a node to tree representing unexplored state
        newChildNode = self.getNewChildNode(state)

        # perform a random simulation from the new node
        rolloutResult = self.rollout(newChildNode)

        # backpropagate the results up to the root's children
        self.backPropagate(newChildNode, rolloutResult)


    def getMove(self, board, legalMoves):
        rootNode = GamestateNode(board, legalMoves)
        numRollouts = 0
        t0 = time.time()
        while time.time()-t0 < self.timeToMove:
            self.runMCTSonce(rootNode)
            numRollouts += 1
        print("numRollouts: ", numRollouts)
        self.searchTreeRoots.append(rootNode)
        return max([move for move in rootNode.children.keys() if rootNode.children[move] != None], key=lambda move: rootNode.children[move].numVisits)

    def __str__(self):
        return 'Monte Carlo Tree Search Agent'
    
if __name__ == "__main__":
    pass




   
   