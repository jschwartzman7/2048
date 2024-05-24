from GameBoard2048 import randomBoard
from GameBoard2048 import printBoard
import SearchAgents as sa


def testMove(moveDirection):
    board = randomBoard()
    printBoard(board)
    match moveDirection:
        case "down":
            print("Moving Down")
            sa.moveDown(board)
        case "right":
            print("Moving Right")
            sa.moveRight(board)
        case "left":
            print("Moving Left")
            sa.moveLeft(board)
        case "up":
            print("Moving Up")
            sa.moveUp(board)
    printBoard(board)

def testMoveUp(numBoards=5):
    print("Move Up Test")
    for i in range(numBoards):
        print("Test Board #", i+1)
        testMove("up")
        
def testMoveDown(numBoards=5):
    print("Move Down Test")
    for i in range(numBoards):
        print("Test Board #", i+1)
        testMove("down")
        
def testMoveLeft(numBoards=5):
    print("Move Left Test")
    for i in range(numBoards):
        print("Test Board #", i+1)
        testMove("left")
        
def testMoveRight(numBoards=5):
    print("Move Right Test")
    for i in range(numBoards):
        print("Test Board #", i+1)
        testMove("right")
   
testMoveRight()