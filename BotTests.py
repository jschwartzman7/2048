import random
import math
import Bot2048
from SearchAgents import Search
'''
Test cases for move functions (left, right, up, down)
Test cases for search strategies
'''
blankBoard = [0 for i in range(16)]
maxExponent = 4
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
    testBot = Bot2048.Bot2048(Search())
    print("Moving Up Test")
    print()
    for i in range(numBoards):
        print("Test board #", i+1)
        testBot.board = randomBoard(maxExponent)
        testBot.printBoard()
        print("Moving up:")
        testBot.agent.moveUp(testBot.board)
        testBot.printBoard()
        print()

def testMoveDown(numBoards):
    testBot = Bot2048.Bot2048(Search())
    print("Moving Down Test")
    print()
    for i in range(numBoards):
        print("Test board #", i+1)
        testBot.board = randomBoard(maxExponent)
        testBot.printBoard()
        print("Moving down:")
        testBot.agent.moveDown(testBot.board)
        testBot.printBoard()
        print()

def testMoveLeft(numBoards):
    testBot = Bot2048.Bot2048(Search())
    print("Moving Left Test")
    print()
    for i in range(numBoards):
        print("Test board #", i+1)
        testBot.board = randomBoard(maxExponent)
        testBot.printBoard()
        print("Moving left:")
        testBot.agent.moveLeft(testBot.board)
        testBot.printBoard()
        print()

def testMoveRight(numBoards):
    testBot = Bot2048.Bot2048(Search())
    print("Moving Right Test")
    print()
    for i in range(numBoards):
        print("Test board #", i+1)
        testBot.board = randomBoard(maxExponent)
        testBot.printBoard()
        print("Moving right:")
        testBot.agent.moveRight(testBot.board)
        testBot.printBoard()
        print()

testMoveRight(5)
testMoveLeft(5)
testMoveUp(5)
testMoveDown(5)
