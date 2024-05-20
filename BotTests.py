import random
import math
from GameBoard2048 import GameBoard
from SearchAgents import Search
'''
Test cases for move functions (left, right, up, down)
Test cases for search strategies
'''
maxExponent = 5
gameBoard = GameBoard()
agent = Search()
'''
[0, 0, 0, 0,
 0, 0, 0, 0,
 0, 0, 0, 0,
 0, 0, 0, 0]
'''

def randomBoard(maxTileExponent):
    board = []
    for i in range(16):
        exponent = random.randint(0, maxTileExponent)
        tileValue = int(math.pow(2, exponent)) if exponent > 0 else 0
        board.append(tileValue)
    return board

def testMoveUp(numBoards):
    print("Moving Up Test")
    print()
    for i in range(numBoards):
        print("Test board #", i+1)
        gameBoard.board = randomBoard(maxExponent)
        gameBoard.printBoard()
        print("Moving up:")
        agent.moveUp(gameBoard.board)
        gameBoard.printBoard()
        print()

def testMoveDown(numBoards):
    print("Moving Down Test")
    print()
    for i in range(numBoards):
        print("Test board #", i+1)
        gameBoard.board = randomBoard(maxExponent)
        gameBoard.printBoard()
        print("Moving down:")
        agent.moveDown(gameBoard.board)
        gameBoard.printBoard()
        print()

def testMoveLeft(numBoards):
    print("Moving Left Test")
    print()
    for i in range(numBoards):
        print("Test board #", i+1)
        gameBoard.board = randomBoard(maxExponent)
        gameBoard.printBoard()
        print("Moving left:")
        agent.moveLeft(gameBoard.board)
        gameBoard.printBoard()
        print()

def testMoveRight(numBoards):
    print("Moving Right Test")
    print()
    for i in range(numBoards):
        print("Test board #", i+1)
        gameBoard.board = randomBoard(maxExponent)
        gameBoard.printBoard()
        print("Moving right:")
        agent.moveRight(gameBoard.board)
        gameBoard.printBoard()
        print()

testMoveRight(1)
testMoveLeft(1)
testMoveUp(1)
testMoveDown(1)
