from selenium.webdriver.common.keys import Keys
import Bot2048
import EvaluationFunctions
import copy
import math
import random

def canMoveDown(board):
    for col in range(4):
        for row in range(1, 4):
            if board[row][col] == ' ' and board[row-1][col] != ' ':
                return True
            elif board[row][col] == board[row-1][col] and board[row][col] != ' ':
                return True
    return False

def canMoveUp(board):
    for col in range(4):
        for row in range(1, 4):
            if board[row][col] != ' ' and board[row-1][col] == ' ':
                return True
            elif board[row][col] == board[row-1][col] and board[row][col] != ' ':
                return True
    return False

def canMoveRight(board):
    for col in range(1, 4):
        for row in range(4):
            if board[row][col] == ' ' and board[row][col-1] != ' ':
                return True
            elif board[row][col] == board[row][col-1] and board[row][col] != ' ':
                return True
    return False

def canMoveLeft(board):
    for col in range(1, 4):
        for row in range(4):
            if board[row][col] != ' ' and board[row][col-1] == ' ':
                return True
            elif board[row][col] == board[row][col-1] and board[row][col] != ' ':
                return True
    return False

def moveDown(board):
    mergedLocations = dict()
    for col in range(4):
        for row in [2, 1, 0]:
            if board[row][col] != ' ':
                checkRow = row + 1
                while board[checkRow][col] == ' ':
                    if checkRow+1 < 4:
                        checkRow = checkRow+1
                    else:
                        break
                if board[checkRow][col] == board[row][col] and ((checkRow, col)) not in mergedLocations:
                    board[checkRow][col] = (board[checkRow][col])*2
                    board[row][col] = ' '
                    mergedLocations[(checkRow, col)] = board[checkRow][col]
                elif board[checkRow][col] == ' ':
                    board[checkRow][col] = board[row][col]
                    board[row][col] = ' '
                elif checkRow > row + 1:
                    board[checkRow-1][col] = board[row][col]
                    board[row][col] = ' '
    return board, mergedLocations

def moveUp(board):
    mergedLocations = dict()
    for col in range(4):
        for row in [1, 2, 3]:
            if board[row][col] != ' ':
                checkRow = row - 1
                while board[checkRow][col] == ' ':
                    if checkRow-1 > -1:
                        checkRow = checkRow-1
                    else:
                        break
                if board[checkRow][col] == board[row][col] and ((checkRow, col)) not in mergedLocations:
                    board[checkRow][col] = (board[checkRow][col])*2
                    board[row][col] = ' '
                    mergedLocations[(checkRow, col)] = board[checkRow][col]
                elif board[checkRow][col] == ' ':
                    board[checkRow][col] = board[row][col]
                    board[row][col] = ' '
                elif checkRow < row - 1:
                    board[checkRow+1][col] = board[row][col]
                    board[row][col] = ' '
    return board, mergedLocations

def moveRight(board):
    mergedLocations = dict()
    for row in range(4):
        for col in [2, 1, 0]:
            if board[row][col] != ' ':
                checkCol = col + 1
                while board[row][checkCol] == ' ':
                    if checkCol+1 < 4:
                        checkCol = checkCol+1
                    else:
                        break
                if board[row][checkCol] == board[row][col] and ((row, checkCol)) not in mergedLocations:
                    board[row][checkCol] = (board[row][checkCol])*2
                    board[row][col] = ' '
                    mergedLocations[(row, checkCol)] = board[row][checkCol]
                elif board[row][checkCol] == ' ':
                    board[row][checkCol] = board[row][col]
                    board[row][col] = ' '
                elif checkCol > col + 1:
                    board[row][checkCol-1] = board[row][col]
                    board[row][col] = ' '
    return board, mergedLocations

def moveLeft(board):
    mergedLocations = dict()
    for row in range(4):
        for col in [1, 2, 3]:
            if board[row][col] != ' ':
                checkCol = col - 1
                while board[row][checkCol] == ' ':
                    if checkCol-1 > -1:
                        checkCol = checkCol-1
                    else:
                        break
                if board[row][checkCol] == board[row][col] and ((row, checkCol)) not in mergedLocations:
                    board[row][checkCol] = (board[row][checkCol])*2
                    board[row][col] = ' '
                    mergedLocations[(row, checkCol)] = board[row][checkCol]
                elif board[row][checkCol] == ' ':
                    board[row][checkCol] = board[row][col]
                    board[row][col] = ' '
                elif checkCol < col - 1:
                    board[row][checkCol+1] = board[row][col]
                    board[row][col] = ' '
    return board, mergedLocations

def getLegalMoves(board):
    legalMoves = []
    if canMoveDown(board): legalMoves.append((moveDown, Keys.DOWN, "down"))
    if canMoveRight(board): legalMoves.append((moveRight, Keys.RIGHT, "right"))
    if canMoveLeft(board): legalMoves.append((moveLeft, Keys.LEFT, "left"))
    if canMoveUp(board): legalMoves.append((moveUp, Keys.UP, "up"))
    return legalMoves
 
class basicSearch():

    def __str__(self):
        return 'Basic Search'

    def move(self, board):
        legalMoves = getLegalMoves(board)
        if len(legalMoves) > 0:
            return legalMoves[0]
        
class randomSearch():

    def __str__(self):
        return 'Random Search'

    def move(self, board):
        legalMoves = getLegalMoves(board)
        if len(legalMoves) > 0:
            index = random.randint(0, len(legalMoves)-1)
            return legalMoves[index]
        
class reflexSearch():

    def __init__(self, evaluationFunction, weights):
        self.evaluationFunction = evaluationFunction
        self.weights = weights

    def __str__(self):
        return 'Reflex Search'

    def move(self, board):
        legalMoves = getLegalMoves(board)
        movedBoards = [moveDirection[0](copy.deepcopy(board)) for moveDirection in legalMoves]
        moveValues = [self.evaluationFunction(movedBoard[0], sum(movedBoard[1].values()), self.weights) for movedBoard in movedBoards]
        return legalMoves[moveValues.index(max(moveValues))]

class expectimaxSearch():

    primes = [[2,   3,  5,  7], 
              [11, 13, 17, 19],
              [23, 29, 31, 37],
              [41, 43, 47, 53]]

    def __init__(self, evalutationFunction, weights):
    
        self.evaluationFunction = evalutationFunction
        self.memo = dict()
        self.weights = weights

    def __str__(self):
        return 'Expectimax Search'
    
    def hash(self, board):
        hashCode = 0
        filledTiles = [(i, j) for i in range(4) for j in range(4) if board[i][j] != ' ']
        for tile in filledTiles:
            hashCode += board[tile[0]][tile[1]] * self.primes[tile[0]][tile[1]]
        return hashCode

    def move(self, board):
        self.memo.clear()
        #bot.printBoard(board)
        '''Expectimax with "Player" and "Chance" turns
            Player can go Up, Down, Left, Right
            Chance has 90% chance of spawning a 2 in a random unoccupied location and 10% chance of spawing a 4
            Evaluation function: based on sum of current tiles, possibilities of merging tiles, location of certain tiles
        '''
        legalMoves = getLegalMoves(board)
        #print(len(legalMoves))
        #print()
        '''moveValues = []
        for moveDirection in legalMoves:
            newBoard = moveDirection[0](board)
            moveValues.append(self.expectimax(newBoard[0], False, 1, sum(newBoard[1].values())))'''
        moveValues = [self.expectimax(moveDirection[0](copy.deepcopy(board))[0], False, 1, sum(moveDirection[0](copy.deepcopy(board))[1].values())) for moveDirection in legalMoves]
        '''for i in range(len(legalMoves)):
            print(moveValues[i])
        print()'''
        #moveValues = [self.expectimax(legalMoves[0][0](board.copy()), False, 1)]
        maxIndex = moveValues.index(max(moveValues))
        return legalMoves[maxIndex]

    def expectimax(self, board, maxPlayer, depth, mergeValues):
        hashedBoard = self.hash(board)

        if not maxPlayer:
            stateValue = 0
            newBoard = copy.deepcopy(board)
            emptyTiles = [(i, j) for i in range(4) for j in range(4) if board[i][j] == ' ']
            for tile in emptyTiles:
                newBoard[tile[0]][tile[1]] = 2
                stateValue += 1.8 * self.expectimax(copy.deepcopy(newBoard), True, depth, mergeValues)
                newBoard[tile[0]][tile[1]] = 4
                stateValue += 0.2 * self.expectimax(copy.deepcopy(newBoard), True, depth, mergeValues)
                newBoard[tile[0]][tile[1]] = ' '
            #self.memo[hashedBoard] = stateValue / (2*len(emptyTiles))
            self.memo[hashedBoard] = stateValue / (2*len(emptyTiles))
            #scoreNew = (score) / (2*numEmpty)
            #return scoreNew
            return self.memo[hashedBoard]
        
        if hashedBoard in self.memo.keys():
            #Bot2048.printBoard(board)
            return self.memo[hashedBoard]

        legalMoves = getLegalMoves(board)
        if depth >= 4 or len(legalMoves) == 0:
            self.memo[hashedBoard] = self.evaluationFunction(board, mergeValues, self.weights)
            return self.memo[hashedBoard]
            self.memo[self.hash(board)] = self.evaluationFunction(board, mergeValues)
            return self.memo[self.hash(board)]
        
        #return max([self.expectimax(moveDirection[0](copy.deepcopy(board))[0], False, depth + 1, merges + (1/(4**depth))*sum(moveDirection[0](copy.deepcopy(board))[1].values())) for moveDirection in legalMoves])
        movedBoards = [moveDirection[0](copy.deepcopy(board)) for moveDirection in legalMoves]
        self.memo[self.hash(board)] = max([self.expectimax(movedBoard[0], False, depth + 1, mergeValues + sum(movedBoard[1].values())) for movedBoard in movedBoards])
        
        #self.memo[self.hash(board)] = max([self.expectimax(moveDirection[0](copy.deepcopy(board))[0], False, depth + 1, mergeValues + sum(moveDirection[0](copy.deepcopy(board))[1].values())) for moveDirection in legalMoves])
        return self.memo[self.hash(board)]
    
    


