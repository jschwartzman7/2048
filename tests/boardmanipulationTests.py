import numpy as np
from game.gameboard import log2Board
from game.gameboard import moveUp, moveDown, moveLeft, moveRight

boards = [
    np.array([[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]),

    np.array([[0, 1, 2, 3],
              [4, 5, 6, 7],
              [8, 9, 10, 11],
              [12, 13, 14, 15]]),

    np.array([[2, 4, 8, 16],
              [32, 64, 128, 256],
              [512, 1024, 2048, 4096],
              [0, 0, 0, 0]]),

    np.array([[0, 0, 0, 0],
              [0, 8, 8, 0],
              [0, 8, 8, 0],
              [0, 0, 0, 0]])]

def testLog2():
    for board in boards:
        print("Testing")
        print(board)
        print("log2 board")
        print(log2Board(board))

def testMoveUp():
    for board in boards:
        print("Testing")
        print(board)
        print("Moved Up")
        print(moveUp(board))

def testMoveDown():
    for board in boards:
        print("Testing")
        print(board)
        print("Moved Down")
        print(moveDown(board))

def testMoveLeft():
    for board in boards:
        print("Testing")
        print(board)
        print("Moved Left")
        print(moveLeft(board))

def testMoveRight():
    for board in boards:
        print("Testing")
        print(board)
        print("Moved Right")
        print(moveRight(board))

def testMoves():
    testMoveUp()
    testMoveDown()
    testMoveLeft()
    testMoveRight()
        
def testAll():
    testLog2()
    testMoves()
    

