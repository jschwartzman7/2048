from selenium.webdriver.common.keys import Keys
import copy
import math
import random

class Search:

    def __init__(self, evaluationFunction=None):
        self.evaluationFunction = evaluationFunction


    def canMoveDown(self, board):
        for idx in range(0, 12):
            if board[idx] != 0 and (board[idx+4] == 0 or board[idx+4] == board[idx]):
                return True
        return False

    def canMoveUp(self, board):
        for idx in range(4, 16):
            if board[idx] != 0 and (board[idx-4] == 0 or board[idx-4] == board[idx]):
                return True
        return False

    def canMoveRight(self, board):
        for idx in range(16):
            if (idx+1)%4 == 0:
                continue
            if board[idx] != 0 and (board[idx+1] == 0 or board[idx+1] == board[idx]):
                return True
        return False

    def canMoveLeft(self, board):
        for idx in range(16):
                if idx%4 == 0:
                    continue
                if board[idx] != 0 and (board[idx-1] == 0 or board[idx-1] == board[idx]):
                    return True
        return False

    def moveArrayLeft(self, arr): # Ex. [0, 4, 4, 8] -> [8, 8, 0, 0]
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

    def moveArrayRight(self, arr): # Ex. [0, 4, 4, 8] -> [0, 0, 8, 8]
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

    def moveDown(self, board):
        for column in range(4):
            board[column::4] = self.moveArrayRight(board[column::4])
        return board


    def moveUp(self, board):
        for column in range(4):
            board[column::4] = self.moveArrayLeft(board[column::4])
        return board

    def moveRight(self, board):
        for row in range(4):
            board[4*row : 4*row + 4] = self.moveArrayRight(board[4*row : 4*row + 4])
        return board
       
    def moveLeft(self, board):
        for row in range(4):
            board[4*row : 4*row + 4] = self.moveArrayLeft(board[4*row : 4*row + 4])
        return board

    def getLegalMoves(self, board):
        legalMoves = []
        if self.canMoveUp(board): legalMoves.append(self.moveUp)
        if self.canMoveDown(board): legalMoves.append(self.moveDown)
        if self.canMoveLeft(board): legalMoves.append(self.moveLeft)
        if self.canMoveRight(board): legalMoves.append(self.moveRight)
        return legalMoves
            
    def getMove(self):
        pass


class randomSearch(Search):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'Random Search'

    def getMove(self, board):
        legalMoves = self.getLegalMoves(board)
        if len(legalMoves) > 0:
            return legalMoves[random.randint(0, len(legalMoves)-1)]
        
class reflexSearch(Search):

    def __init__(self, evaluationFunction=None):
        super().__init__(evaluationFunction)

    def __str__(self):
        return 'Reflex Search'

    def getMove(self, board):
        legalMoves = self.getLegalMoves(board)
        if len(legalMoves) > 0:
            movedBoards = [moveFunction(board.copy()) for moveFunction in legalMoves]
            movedBoardValues = [self.evaluationFunction(board) for board in movedBoards]
            return legalMoves[movedBoardValues.index(max(movedBoardValues))]

class expectimaxSearch(Search):

    def __init__(self, evaluationFunction=None, maxDepth=4):
        super().__init__(evaluationFunction)
        self.memo = dict()
        self.maxDepth = maxDepth

    def __str__(self):
        return 'Expectimax Search'

    def getMove(self, board):
        self.memo.clear()
        #bot.printBoard(board)
        '''Expectimax with "Player" and "Chance" turns
            Player can go Up, Down, Left, Right
            Chance has 90% chance of spawning a 2 in a random unoccupied location and 10% chance of spawing a 4
        '''
        legalMoves = self.getLegalMoves(board)
        if len(legalMoves) > 0:
            moveValues = [self.expectimax(moveDirection[0](board.copy()), False, 1, sum(moveDirection[0](board.copy()))) for moveDirection in legalMoves]
            '''for i in range(len(legalMoves)):
                print(moveValues[i])
            print()'''
            #moveValues = [self.expectimax(legalMoves[0][0](board.copy()), False, 1)]
            maxIndex = moveValues.index(max(moveValues))
            return legalMoves[maxIndex]

    def expectimax(self, board, maxPlayer, depth, mergeValues):
        hashedBoard = tuple(board)

        if not maxPlayer:
            stateValue = 0
            newBoard = copy.deepcopy(board)
            emptyTiles = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
            for tile in emptyTiles:
                newBoard[tile[0]][tile[1]] = 2
                stateValue += 1.8 * self.expectimax(copy.deepcopy(newBoard), True, depth, mergeValues)
                newBoard[tile[0]][tile[1]] = 4
                stateValue += 0.2 * self.expectimax(copy.deepcopy(newBoard), True, depth, mergeValues)
                newBoard[tile[0]][tile[1]] = 0
            #self.memo[hashedBoard] = stateValue / (2*len(emptyTiles))
            self.memo[hashedBoard] = stateValue / (2*len(emptyTiles))
            #scoreNew = (score) / (2*numEmpty)
            #return scoreNew
            return self.memo[hashedBoard]
        
        if hashedBoard in self.memo.keys():
            #Bot2048.printBoard(board)
            return self.memo[hashedBoard]

        legalMoves = self.getLegalMoves(board)
        if depth > self.maxDepth or len(legalMoves) == 0:
            self.memo[hashedBoard] = self.evaluationFunction(board, mergeValues, self.weights)
            return self.memo[hashedBoard]
        
        #return max([self.expectimax(moveDirection[0](copy.deepcopy(board))[0], False, depth + 1, merges + (1/(4**depth))*sum(moveDirection[0](copy.deepcopy(board))[1].values())) for moveDirection in legalMoves])
        movedBoards = [moveDirection[0](copy.deepcopy(board)) for moveDirection in legalMoves]
        self.memo[self.hash(board)] = max([self.expectimax(movedBoard[0], False, depth + 1, mergeValues + sum(movedBoard[1].values())) for movedBoard in movedBoards])
        
        #self.memo[self.hash(board)] = max([self.expectimax(moveDirection[0](copy.deepcopy(board))[0], False, depth + 1, mergeValues + sum(moveDirection[0](copy.deepcopy(board))[1].values())) for moveDirection in legalMoves])
        return self.memo[self.hash(board)]
    
    
class peacefulSearch(Search):

    def __init__(self, evaluationFunction=None, maxDepth=4):
        super().__init__(evaluationFunction)
        self.memo = dict()
        self.maxDepth = maxDepth

    def __str__(self):
        return 'Peaceful Search'

    def getMove(self, board):
        ''' maxMax search, where no piece is generated between turns
            Treating game to be deterministic; takes max over deeper board values, not average
        '''
        legalMoves = self.getLegalMoves(board)
        if len(legalMoves) > 0:
            movedBoardValues = [self.search(moveFunction(board.copy()), 1) for moveFunction in legalMoves]
            return legalMoves[movedBoardValues.index(max(movedBoardValues))]

    def search(self, board, curDepth):
        if curDepth > self.maxDepth:
            return self.evaluationFunction(board)

        hashedBoard = tuple(board)
        if hashedBoard in self.memo.keys():
            return self.memo[hashedBoard]
        
        legalMoves = self.getLegalMoves(board)
        if len(legalMoves) == 0:
            return self.evaluationFunction(board) # should return 0
       

        movedBoardValues = [self.search(moveFunction(board.copy()), curDepth+1) for moveFunction in legalMoves]
        self.memo[hashedBoard] = max(movedBoardValues)
        return self.memo[hashedBoard]
    
    





