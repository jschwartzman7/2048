import random
import math
import GameBoard2048 as gb
import SearchAgents as sa
import EvaluationFunctions as ef
import matplotlib.pyplot as plt
import TestValues as t

def testEvalutaionFunctionMoves(evaluationFunction, numBoards=5):
    print("Evalution function test")
    print()
    for i in range(numBoards):
        print("Board ", i+1)
        board = gb.randomBoard(t.maxExponent)
        gb.printBoard(board)
        print("Board value: ", evaluationFunction(board))
        print()
        change = random.randint(0, 4)
        match change:
            case 0:
                gb.generatePiece(board)
                print("Generated piece:")
            case 1:
                sa.moveDown(board)
                print("Moved down")
            case 2:
                sa.moveRight(board)
                print("Moved right")
            case 3:
                sa.moveLeft(board)
                print("Moved left")
            case 4:
                sa.moveUp(board)
                print("Moved up")
        gb.printBoard(board)
        print("Board value: ", evaluationFunction(board))
        print()

def testBoardFeatures(numBoards=5):
    print("Feature Testing")
    for i in range(numBoards):
        print("Test board #", i+1)
        board = gb.randomBoard()
        gb.printBoard(board)
        center = ef.center(board)
        print("Log max: ", math.log2(max(board)))
        print("num empty: ", len(gb.emptyIndices(board)))
        print("SD: ", ef.standardDeviation(board, center))
        print("distCenterCorner", ef.distanceCenterCorner(center))
        print()

def testTestBoardsFeatures():
    print("Feature Testing")
    for board in t.testBoards:
        gb.printBoard(board)
        center = ef.center(board)
        print("Center: ", center)
        print("SD: ", ef.standardDeviation(board, center))
        print("distCenterCorner", ef.distanceCenterCorner(center))
        print()

def distributionStatistics(numBoards=10):
    sds = []
    dCenterCorners = []
    maxTileLogs = []
    numEmptys = []
    for i in range(numBoards):
        board = gb.randomBoard()
        center = ef.center(board)
        sds.append(ef.standardDeviation(board, center))
        dCenterCorners.append(ef.distanceCenterCorner(center))
        maxTileLogs.append(math.log2(max(board)))
        numEmptys.append(len([i for i in range(16) if board[i] == 0]))

    figure, axis = plt.subplots(2, 2) 
  
    axis[0, 0].hist(sds)
    axis[0, 0].set_title("Standard Deviations") 
    
    axis[1, 0].hist(dCenterCorners)
    axis[1, 0].set_title("CenterCorners")

    axis[0, 1].hist(maxTileLogs)
    axis[0, 1].set_title("log max Tile") 
    
    axis[1, 1].hist(numEmptys)
    axis[1, 1].set_title("numEmpty") 
    
    plt.show()

testBoardFeatures(10)