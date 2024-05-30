import random
import GameBoard2048 as gb
import numpy as np

def canMoveDown(board):
    for idx in range(0, 12):
        if board[idx] != 0 and (board[idx+4] == 0 or board[idx+4] == board[idx]):
            return True
    return False

def canMoveUp(board):
    for idx in range(4, 16):
        if board[idx] != 0 and (board[idx-4] == 0 or board[idx-4] == board[idx]):
            return True
    return False

def canMoveRight(board):
    for idx in range(16):
        if (idx+1)%4 == 0:
            continue
        if board[idx] != 0 and (board[idx+1] == 0 or board[idx+1] == board[idx]):
            return True
    return False

def canMoveLeft(board):
    for idx in range(16):
            if idx%4 == 0:
                continue
            if board[idx] != 0 and (board[idx-1] == 0 or board[idx-1] == board[idx]):
                return True
    return False

def moveArrayLeft(arr): # Ex. [0, 4, 4, 8] -> [8, 8, 0, 0]
    mergedIndices = set()
    for i in range(1, len(arr)):
        for j in range(i, 0, -1):
            match arr[j-1], arr[j]:
                case x, 0:
                    pass
                case 0, x:
                    arr[j-1], arr[j] = arr[j], arr[j-1]
                case x, y if x == y and j-1 not in mergedIndices and j not in mergedIndices:
                    arr[j-1], arr[j] = 2*arr[j-1], 0
                    mergedIndices.add(j-1)
                case _:
                    pass
    return arr

def moveArrayRight(arr): # Ex. [0, 4, 4, 8] -> [0, 0, 8, 8]
    mergedIndices = set()
    for i in range(len(arr)-2, -1, -1):
        for j in range(i, len(arr)-1):
            match arr[j], arr[j+1]:
                case 0, x:
                    pass
                case x, 0:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                case x, y if x == y and j not in mergedIndices and j+1 not in mergedIndices:
                    arr[j], arr[j+1] = 0, 2*arr[j+1]
                    mergedIndices.add(j+1)
                case _:
                    pass
    return arr

def moveDown(board):
    for column in range(4):
        board[column::4] = moveArrayRight(board[column::4])
    return board

def moveUp(board):
    for column in range(4):
        board[column::4] = moveArrayLeft(board[column::4])
    return board

def moveRight(board):
    for row in range(4):
        board[4*row : 4*row + 4] = moveArrayRight(board[4*row : 4*row + 4])
    return board
    
def moveLeft(board):
    for row in range(4):
        board[4*row : 4*row + 4] = moveArrayLeft(board[4*row : 4*row + 4])
    return board

moveToString = {moveDown: "down", moveRight: "right", moveLeft: "left", moveUp: "up"}

def getLegalMoves(board):
    legalMoves = []
    if canMoveDown(board): legalMoves.append(moveDown)
    if canMoveRight(board): legalMoves.append(moveRight)
    if canMoveLeft(board): legalMoves.append(moveLeft)
    if canMoveUp(board): legalMoves.append(moveUp)
    return legalMoves
        
class Search:
    
    def getMove(self):
        return
    
    def testMove(self):
        return

class RandomSearch(Search):

    def __str__(self):
        return 'Random Search'

    def getMove(self, board):
        legalMoves = getLegalMoves(board)
        if len(legalMoves) > 0:
            return legalMoves[random.randint(0, len(legalMoves)-1)]
        
    def testMove(self, board):
        print("Initial Board:")
        gb.printBoard(board)
        legalMoves = getLegalMoves(board)
        if len(legalMoves) > 0:
            print("Returned move: ", moveToString[legalMoves[random.randint(0, len(legalMoves)-1)]])
        
class BasicSearch(Search):

    def __str__(self):
        return 'Basic Search'

    def getMove(self, board):
        legalMoves = getLegalMoves(board)
        if len(legalMoves) > 0:
            return legalMoves[0]
        
    def testMove(self, board):
        print("Initial Board:")
        gb.printBoard(board)
        legalMoves = getLegalMoves(board)
        if len(legalMoves) > 0:
            print("Returned move: ", moveToString[legalMoves[0]])
        
class ReflexSearch(Search):

    def __init__(self, evaluationFunction=None):
        self.evaluationFunction = evaluationFunction

    def __str__(self):
        return 'Reflex Search'

    def getMove(self, board):
        legalMoves = getLegalMoves(board)
        if len(legalMoves) > 0:
            movedBoards = [moveFunction(board.copy()) for moveFunction in legalMoves]
            movedBoardValues = [self.evaluationFunction(board) for board in movedBoards]
            return legalMoves[movedBoardValues.index(max(movedBoardValues))]
        
    def testMove(self, board):
        print("Initial Board:")
        gb.printBoard(board)
        legalMoves = getLegalMoves(board)
        if len(legalMoves) > 0:
            movedBoards = []
            for move in legalMoves:
                print("Just moved ", moveToString[move])
                movedBoards.append(move(board.copy()))
                gb.printBoard(movedBoards[-1])
                print("Board Value = ", self.evaluationFunction(movedBoards[-1]))
                print()
            movedBoardValues = [self.evaluationFunction(board) for board in movedBoards]
            print("Returned move: ", moveToString[legalMoves[movedBoardValues.index(max(movedBoardValues))]])

class ExpectimaxSearch(Search):

    def __init__(self, evaluationFunction=None, maxDepth=3, newTileFrac = 1):
        self.evaluationFunction = evaluationFunction
        self.maxDepth = maxDepth
        self.newTileFrac = newTileFrac
        self.memo = dict()

    def __str__(self):
        return 'Expectimax Search'

    def getMove(self, board, legalMoves):
        '''Expectimax with "Player" and "Chance" turns
            Player can go Up, Down, Left, Right
            Chance has 90% chance of spawning a 2 in a random unoccupied location and 10% chance of spawing a 4
            legalMoves passed in is non-empty
        '''
        moveValues = [self.expectimax(moveDirection(board.copy()), False, 1) for moveDirection in legalMoves]
        return legalMoves[moveValues.index(max(moveValues))]
    
    def expectimax(self, board, maxPlayer, curDepth):
        legalMoves = getLegalMoves(board)
        if len(legalMoves) == 0:
            return float("-inf")
        hashedBoard = tuple(board)
        if curDepth > self.maxDepth:
            self.memo[hashedBoard] = self.evaluationFunction(board)
            return self.memo[hashedBoard]
        if hashedBoard in self.memo.keys():
            return self.memo[hashedBoard]
        if not maxPlayer:
            emptyTiles = gb.emptyIndices(board)
            if int(self.newTileFrac*len(emptyTiles)) > 0:
                newTileIndices = random.sample(emptyTiles, int(self.newTileFrac*len(emptyTiles)))
                boardValue = 0
                for tileIdx in newTileIndices:
                    newBoard2 = board.copy()
                    newBoard4 = board.copy()
                    newBoard2[tileIdx] = 2
                    newBoard4[tileIdx] = 4
                    if tuple(newBoard2) in self.memo.keys():
                        boardValue += 0.9*self.memo[tuple(newBoard2)]
                    else:
                        boardValue += 0.9*self.expectimax(newBoard2.copy(), True, curDepth)
                    if tuple(newBoard4) in self.memo.keys():
                        boardValue += 0.1*self.memo[tuple(newBoard4)]
                    else:
                        boardValue += 0.1 * self.expectimax(newBoard4.copy(), True, curDepth)
                self.memo[hashedBoard] = boardValue / len(newTileIndices)
                return self.memo[hashedBoard]
        movedBoardValues = [self.expectimax(moveFunction(board.copy()), False, curDepth+1) for moveFunction in legalMoves]
        self.memo[hashedBoard] = max(movedBoardValues)
        return self.memo[hashedBoard]

   
    
class PeacefulSearch(Search):

    def __init__(self, evaluationFunction=None, maxDepth=3):
        self.evaluationFunction = evaluationFunction
        self.maxDepth = maxDepth
        self.memo = dict()

    def __str__(self):
        return 'Peaceful Search'

    def getMove(self, board):
        legalMoves = getLegalMoves(board)
        if len(legalMoves) > 0:
            movedBoardValues = [self.search(moveFunction(board.copy()), 1) for moveFunction in legalMoves]
            return legalMoves[movedBoardValues.index(max(movedBoardValues))]

    def search(self, board, curDepth):
        legalMoves = getLegalMoves(board)
        if len(legalMoves) == 0:
            return 0
        
        hashedBoard = tuple(board)
        if curDepth > self.maxDepth:
            self.memo[hashedBoard] = self.evaluationFunction(board)
            return self.memo[hashedBoard]

        if hashedBoard in self.memo.keys():
            return self.memo[hashedBoard]
        
        movedBoardValues = [self.search(moveFunction(board.copy()), curDepth+1) for moveFunction in legalMoves]
        self.memo[hashedBoard] = sum(movedBoardValues)/len(legalMoves)
        return self.memo[hashedBoard]
    