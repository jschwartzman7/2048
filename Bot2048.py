import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as Options
from bs4 import BeautifulSoup
import time
import math
import copy

class Search:
    
    def canMoveDown(self, board):
        for col in range(4):
            for row in range(1, 4):
                if board[row][col] == ' ' and board[row-1][col] != ' ':
                    return True
                elif board[row][col] == board[row-1][col] and board[row][col] != ' ':
                    return True
        return False
    
    def canMoveUp(self, board):
        for col in range(4):
            for row in range(1, 4):
                if board[row][col] != ' ' and board[row-1][col] == ' ':
                    return True
                elif board[row][col] == board[row-1][col] and board[row][col] != ' ':
                    return True
        return False
    
    def canMoveRight(self, board):
        for col in range(1, 4):
            for row in range(4):
                if board[row][col] == ' ' and board[row][col-1] != ' ':
                    return True
                elif board[row][col] == board[row][col-1] and board[row][col] != ' ':
                    return True
        return False
    
    def canMoveLeft(self, board):
        for col in range(1, 4):
            for row in range(4):
                if board[row][col] != ' ' and board[row][col-1] == ' ':
                    return True
                elif board[row][col] == board[row][col-1] and board[row][col] != ' ':
                    return True
        return False
    
    def moveDown(self, board):
        mergedLocations = set()
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
                        board[checkRow][col] = str(int(board[checkRow][col])*2)
                        board[row][col] = ' '
                        mergedLocations.add((checkRow, col))
                    elif board[checkRow][col] == ' ':
                        board[checkRow][col] = board[row][col]
                        board[row][col] = ' '
                    elif checkRow > row + 1:
                        board[checkRow-1][col] = board[row][col]
                        board[row][col] = ' '
        return board
    
    def moveUp(self, board):
        mergedLocations = set()
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
                        board[checkRow][col] = str(int(board[checkRow][col])*2)
                        board[row][col] = ' '
                        mergedLocations.add((checkRow, col))
                    elif board[checkRow][col] == ' ':
                        board[checkRow][col] = board[row][col]
                        board[row][col] = ' '
                    elif checkRow < row - 1:
                        board[checkRow+1][col] = board[row][col]
                        board[row][col] = ' '
        return board
    
    def moveRight(self, board):
        mergedLocations = set()
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
                        board[row][checkCol] = str(int(board[row][checkCol])*2)
                        board[row][col] = ' '
                        mergedLocations.add((row, checkCol))
                    elif board[row][checkCol] == ' ':
                        board[row][checkCol] = board[row][col]
                        board[row][col] = ' '
                    elif checkCol > col + 1:
                        board[row][checkCol-1] = board[row][col]
                        board[row][col] = ' '
        return board
    
    def moveLeft(self, board):
        mergedLocations = set()
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
                        board[row][checkCol] = str(int(board[row][checkCol])*2)
                        board[row][col] = ' '
                        mergedLocations.add((row, checkCol))
                    elif board[row][checkCol] == ' ':
                        board[row][checkCol] = board[row][col]
                        board[row][col] = ' '
                    elif checkCol < col - 1:
                        board[row][checkCol+1] = board[row][col]
                        board[row][col] = ' '
        return board
    

    def countEmptyTiles(self, board):
        emptyTiles = 0
        for i in range(4):
            for j in range(4):
                if board[i][j] == ' ':
                    emptyTiles += 1
        return emptyTiles
    
    def numMerges(self, board, direction):
        return self.countEmptyTiles(direction(copy.deepcopy(board))) - self.countEmptyTiles(board)
    
    def getLegalMoves(self, board):
        legalMoves = []
        if self.canMoveDown(board): legalMoves.append((self.moveDown, Keys.DOWN))
        if self.canMoveUp(board): legalMoves.append((self.moveUp, Keys.UP))
        if self.canMoveRight(board): legalMoves.append((self.moveRight, Keys.RIGHT))
        if self.canMoveLeft(board): legalMoves.append((self.moveLeft, Keys.LEFT))
        return legalMoves
 
class basicSearch(Search):
    def move(self, board):
        if self.canMoveDown(board):
            return Keys.DOWN
        elif self.canMoveRight(board):
            return Keys.RIGHT
        elif self.canMoveLeft(board):
            return Keys.LEFT
        else:
            return Keys.UP

class expectimaxSearch(Search):

    memo = dict()
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    tileWeights = {
        (0, 0) : 0,
        (0, 1) : 0,
        (0, 2) : 0,
        (0, 3) : 0,
        (1, 0) : 0,
        (1, 1) : 0,
        (1, 2) : .5,
        (1, 3) : .5,
        (2, 0) : .5,
        (2, 1) : .5,
        (2, 2) : 1,
        (2, 3) : 1,
        (3, 0) : .5,
        (3, 1) : 3,
        (3, 2) : 10,
        (3, 3) : 20,

    }
 
    def hash(self, board):
        index = 0
        hashCode = 0
        for i in range(4):
            for j in range(4):
                if board[i][j] != ' ':
                    hashCode += int(board[i][j]) * self.primes[index]
                    index += 1
        return hashCode


    def move(self, board):
        self.memo.clear()
        #bot.printBoard(board)
        '''Expectimax with "Player" and "Chance" turns
            Player can go Up, Down, Left, Right
            Chance has 90% chance of spawning a 2 in a random unoccupied location and 10% chance of spawing a 4
            Evaluation function: based on sum of current tiles, possibilities of merging tiles, location of certain tiles
        '''
        legalMoves = self.getLegalMoves(board)
        #print(len(legalMoves))
        #print()
        moveValues = [self.expectimax(moveDirection[0](copy.deepcopy(board)), False, 1, self.numMerges(board, moveDirection[0])) for moveDirection in legalMoves]
        '''for i in range(len(legalMoves)):
            print(moveValues[i])
        print()'''
        #moveValues = [self.expectimax(legalMoves[0][0](board.copy()), False, 1)]
        maxIndices = [i for i in range(len(moveValues)) if moveValues[i] == max(moveValues)]
        return legalMoves[maxIndices[0]][1]
    
    maxMerges = 0
    minMerges = 100

    def expectimax(self, board, maxPlayer, depth, merges):

        if self.hash(board) in self.memo.keys():
            return self.memo[self.hash(board)]
        if depth == 25:
            if merges > expectimaxSearch.maxMerges:
                expectimaxSearch.maxMerges = merges
            if merges < expectimaxSearch.minMerges:
                expectimaxSearch.minMerges = merges
        
        legalMoves = self.getLegalMoves(board)

        if depth >= 10 or len(legalMoves) == 0:
            self.memo[self.hash(board)] = self.evaluate(board, merges)
            return self.memo[self.hash(board)]
        elif maxPlayer:
            #print("Max player about to move " , legalMoves[0])
            self.memo[self.hash(board)] = max([self.expectimax(moveDirection[0](copy.deepcopy(board)), False, depth + 1, merges + self.numMerges(board, moveDirection[0])) for moveDirection in legalMoves])
            return self.memo[self.hash(board)]
            #return max([self.expectimax(legalMoves[0][0](board.copy()), False, depth + 1)])
        else:
            #newBoards2, newBoards4 = self.generatePieces(board.copy())
            values2 = []
            values4 = []
            for i in range(4):
                for j in range(4):
                    if board[i][j] == ' ':
                        newBoard = copy.deepcopy(board)
                        newBoard[i][j] = '2'
                        values2.append(self.expectimax(copy.deepcopy(newBoard), True, depth + 1, merges))
                        newBoard[i][j] = '4'
                        values4.append(self.expectimax(copy.deepcopy(newBoard), True, depth + 1, merges))
                        #newBoard[i][j] = ' '
            #values2 = [self.expectimax(newBoard.copy(), True, depth + 1) for newBoard in newBoards2]
            #values4 = [self.expectimax(newBoard.copy(), True, depth + 1) for newBoard in newBoards4]
            #return (sum(values2)*.9 + sum(values4)*.1) / (len(newBoards2) + len(newBoards4) + 1)
            #print(values2, values4)
            self.memo[self.hash(board)] = (sum(values2)*1.8 + sum(values4)*.2) / (2*len(values2))
            return self.memo[self.hash(board)]
        
    def evaluate(self, board, merges):
        numEmpty = self.countEmptyTiles(board)
        boardValue = 0
        for i in range(4):
            for j in range(4):
                if board[i][j] != ' ':
                    boardValue += int(board[i][j])*self.tileWeights[(i, j)]
        return numEmpty + merges + boardValue
    


class Bot2048:
    
    options = Options()
    options.page_load_strategy = 'eager'

    def __init__(self, strategy):
        self.strategy = strategy
        self.driver = webdriver.Chrome(options=Bot2048.options)
        self.actions = ActionChains(self.driver)
        self.board = [
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ']
        ]
        

        
    def printBoard(self, board):
        maxSize = 1
        for i in range(4):
            for j in range(4):
                size = len(str(board[i][j]))
                if size > maxSize:
                    maxSize = size
        for row in range(4):
            for col in range(4):
                if col < 3:
                    print(board[row][col], end=(maxSize-len(str(board[row][col])))*' ')
                    print('|', end='')
                else:
                    print(board[row][col])
            if row < 3:
                print((maxSize*4+3)*'-')
        print()
        print()
        print()

    def fillBoard(self):
        HTML = self.driver.page_source
        parsedHTML = BeautifulSoup(HTML, 'html.parser')
        tileContainer = parsedHTML.find(class_="tile-container")
        tiles = tileContainer.find_all(class_="tile")
        for tile in tiles:
            value = tile.contents[0].string
            position = tile['class'][2][-3:]
            self.board[int(position[2])-1][int(position[0])-1] = value
    
    def resetBoard(self):
        for i in range(4):
            for j in range(4):
                self.board[i][j] = ' '    

    def play(self):
        self.driver.get('https://play2048.co')
        time.sleep(.25)
        self.fillBoard()
        while len(self.strategy.getLegalMoves(self.board)) > 0:
        #while BeautifulSoup(self.driver.page_source, 'html.parser').find_all(class_='game-over') == []:
            self.actions.send_keys(self.strategy.move(self.board)).perform()
            self.actions.reset_actions()
            #time.sleep(.1)
            self.resetBoard()
            self.fillBoard()
            #self.printBoard(self.board)

Bot2048(expectimaxSearch()).play()
            






    





'''while True:
    pass
search = Search()
bot.printBoard()
search.moveLeft(bot.board)
bot.printBoard()'''


