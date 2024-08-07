
def testMove(moveDirection, tilesFilled, maxExponent):
    board = gb.randomBoardNumpy(maxTileExponent=maxExponent, numFilled=tilesFilled)
    print(board)
    match moveDirection:
        case "down":
            print("Moving Down")
            board = sa.moveDown(board)
        case "right":
            print("Moving Right")
            board = sa.moveRight(board)
        case "left":
            print("Moving Left")
            board = sa.moveLeft(board)
        case "up":
            print("Moving Up")
            board = sa.moveUp(board)
    print(board)

def testMoveUp(numBoards=5, tilesFilled=8, maxExponent=t.maxExponent):
    print("Move Up Test")
    for i in range(numBoards):
        print("Test Board #", i+1)
        testMove("up", tilesFilled, maxExponent)
        
def testMoveDown(numBoards=5, tilesFilled=8, maxExponent=t.maxExponent):
    print("Move Down Test")
    for i in range(numBoards):
        print("Test Board #", i+1)
        testMove("down", tilesFilled, maxExponent)
        
def testMoveLeft(numBoards=5, tilesFilled=8, maxExponent=t.maxExponent):
    print("Move Left Test")
    for i in range(numBoards):
        print("Test Board #", i+1)
        testMove("left", tilesFilled, maxExponent)
        
def testMoveRight(numBoards=5, tilesFilled=8, maxExponent=t.maxExponent):
    print("Move Right Test")
    for i in range(numBoards):
        print("Test Board #", i+1)
        testMove("right", tilesFilled, maxExponent)
 
