import Bot2048
import Search
from Search import expectimaxSearch
import copy
import random
import EvaluationFunctions

pieces = [' ', 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
blankBoard = [[' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ']]
'''board = [
        [' ', ' ', ' ', ' '],
        [2, ' ', ' ', ' '],
        [' ', ' ', 4, ' '],
        [' ', ' ', ' ', ' ']]'''
randomTestBoards = []
for i in range(10):
    testBoard = copy.deepcopy(blankBoard)
    for row in range(4):
        for col in range(4):
            piece = random.choice(pieces)
            testBoard[row][col] = piece
    randomTestBoards.append(testBoard)

usedPieces = [' ', ' ', ' ', ' ', ' ', ' ', 2, 2, 4, 8, 8, 32, 64, 64, 128, 256]
randomEqualBoards = []
for i in range(20):
    index = 0
    random.shuffle(usedPieces)
    testBoard = copy.deepcopy(blankBoard)
    for row in range(4):
        for col in range(4):
            testBoard[row][col] = usedPieces[index]
            index += 1
    randomEqualBoards.append(testBoard)
testBoards =[
        [[' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ']],

        [[' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', 128]],

        [[' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', 32],
        [' ', ' ', 64, 128]],

       [[64, ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', 32],
        [' ', ' ', 128, ' ']],

       [[128, ' ', ' ', 128],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [128, ' ', ' ', 128]],

       [[' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [64, 1024, ' ', ' '],
        [512, 256, ' ', ' ']],

       [[256, 64, ' ', ' '],
        [128, ' ', ' ', ' '],
        [' ', ' ', ' ', 512],
        [' ', ' ', 512, 2048]],

]
def randomStartingBoard():
    board = copy.deepcopy(blankBoard)
    piece1Cords = random.randint(0, 3), random.randint(0, 3)
    piece2Cords = random.randint(0, 3), random.randint(0, 3)
    while piece2Cords == piece1Cords:
        piece2Cords = [random.randint(0, 3), random.randint(0, 3)]
    piece1Num = random.random()
    piece2Num = random.random()
    board[piece1Cords[0]][piece1Cords[1]] = 2 if piece1Num < .9 else 4
    board[piece2Cords[0]][piece2Cords[1]] = 2 if piece2Num < .9 else 4
    return board



def testFunctions(testBoards):
    for board in testBoards:
        print("New board: ")
        Bot2048.printBoard(board)
        '''print("Can move down? ", Search.canMoveDown(board))
        print("Can move up? ", Search.canMoveUp(board))
        print("Can move right? ", Search.canMoveRight(board))
        print("Can move left? ", Search.canMoveLeft(board))'''
        legalMoves = Search.getLegalMoves(board)
        print("Legal moves: ", end= " ")
        for move in legalMoves:
            print(move[2], end = " ")
        print()
        print("Board moves:")
        for move in legalMoves:
            print("Original board:")
            Bot2048.printBoard(board)
            print("Move: ", move[2])
            print()
            movedBoard = move[0](copy.deepcopy(board))
            Bot2048.printBoard(movedBoard[0])
            print()
            print("Num merges: ", len(movedBoard[1]))
            print("Merge values: ", sum(movedBoard[1].values()))
            print()
        '''newBoard = board.copy()
        test.bot.printBoard(test.bot.strategy.moveDown(newBoard))
        test.bot.printBoard(board)'''
        print()
        print()
        print()

def testEvaluationFunction(evaluationFunction):
    #scores = dict()
    #for board in randomEqualBoards:
        #scores[evaluationFunction(board, sum([sum(moveDirection[0](copy.deepcopy(board))[1].values()) for moveDirection in Search.getLegalMoves(board)]))] = board
    #scoresList = [key for key in scores.keys()]
    #scoresList.sort()
    #scoresList.reverse()
    for board in randomTestBoards:
        print("Evalutation function: ", evaluationFunction(board, sum([sum(moveDirection[0](copy.deepcopy(board))[1].values()) for moveDirection in Search.getLegalMoves(board)]), [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))
        Bot2048.printBoard(board)
        print()

def runSimulations(strategies, roundsPerStrategy=10):
    
    for strategy in strategies:
        sumMaxTiles = 0
        maxTileTotal= 0
        #print(str(strategy))
        for i in range(roundsPerStrategy):
            maxTile = simulateGame(strategy)
            #print(maxTile)
            maxTileTotal = maxTile if maxTile > maxTileTotal else maxTileTotal
            sumMaxTiles += maxTile
        return sumMaxTiles/roundsPerStrategy
        print()
        print("Max max tile: ", maxTileTotal)
        print("Average max tile: ", sumMaxTiles/roundsPerStrategy)
        print()


def simulateGame(strategy):
    currentBoard = randomStartingBoard()
    while len(Search.getLegalMoves(currentBoard)) > 0:
        currentBoard = strategy.move(currentBoard)[0](currentBoard)[0]
        currentBoard = generatePiece(currentBoard)
    return getTopPiece(currentBoard)

def generatePiece(board):
    emptyCords = set()
    for i in range(4):
        for j in range(4):
            if board[i][j] == ' ':
                emptyCords.add((i, j))
    tile = emptyCords.pop()
    if random.randint(1, 10) == 1:
        board[tile[0]][tile[1]] = 4
    else:
        board[tile[0]][tile[1]] = 2
    return board

def getTopPiece(board):
    topPiece = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != ' ':
                if board[i][j] > topPiece:
                    topPiece = board[i][j]
    return topPiece




 





 