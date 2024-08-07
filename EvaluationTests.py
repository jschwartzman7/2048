from gameBoard import randomTestBoardWeighted, generatePiece
import evaluationFunctions as ef
from constants import rand

def testEvalutaionFunctionMoves(evaluationFunction, numBoards=5):
    print("Evalution function test")
    print()
    for i in range(numBoards):
        print("Board ", i+1)
        board = gb.randomBoardNumpy(t.maxExponent, 8)
        print(board)
        print("Board value: ", evaluationFunction(board))
        print()
        change = random.randint(0, 4)
        match change:
            case 0:
                board = gb.generatePiece(board)
                print("Generated piece:")
            case 1:
                board = sa.moveDown(board)
                print("Moved down")
            case 2:
                board = sa.moveRight(board)
                print("Moved right")
            case 3:
                board = sa.moveLeft(board)
                print("Moved left")
            case 4:
                board = sa.moveUp(board)
                print("Moved up")
        print(board)
        print("Board value: ", evaluationFunction(board))
        print()

def testBoardFeature(evaluationFunction, numBoards=5):
    print("Feature Testing")
    for i in range(numBoards):
        print("Test board #", i+1)
        board = gb.randomBoardNumpy()
        print(board)
        print("Value ", evaluationFunction(board))
        print()

def testTestBoardsFeatures(evaluationFunction):
    print("Feature Testing")
    for board in t.testBoards:
        print(board)
        print("Value: ", evaluationFunction(board))
        print()

def testEvals(evals, numBoards):
    for i in range(numBoards):
        print("Board ", i+1)
        board = randomTestBoardWeighted()
        print(board)
        for eval, name in evals.items():
            value = eval(board)
            print(name, ": ", value)
        print()

testEvals({ef.snakeStrength: "snakeStrength", ef.cornerStrength: "cornerStrength"}, 10)