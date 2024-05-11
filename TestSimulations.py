import Bot2048
import SearchAgents
from SearchAgents import expectimaxSearch
import copy
import random
import EvaluationFunctions

pieces = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
blankBoard = {0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
            13: 0,
            14: 0,
            15: 0}
blankBoard = [[' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ']]

randomTestBoards = []
for i in range(10):
    testBoard = copy.deepcopy(blankBoard)
    for row in range(4):
        for col in range(4):
            piece = random.choice(pieces)
            testBoard[row][col] = piece
    randomTestBoards.append(testBoard)

def testFunctions(testBoards):
    for board in testBoards:
        print("New board: ")
        Bot2048.printBoard(board)
        '''print("Can move down? ", Search.canMoveDown(board))
        print("Can move up? ", Search.canMoveUp(board))
        print("Can move right? ", Search.canMoveRight(board))
        print("Can move left? ", Search.canMoveLeft(board))'''
        legalMoves = SearchAgents.getLegalMoves(board)
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
        print("Evalutation function: ", evaluationFunction(board, sum([sum(moveDirection[0](copy.deepcopy(board))[1].values()) for moveDirection in SearchAgents.getLegalMoves(board)]), [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))
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


def randomBoard():
    board = {i : 0 for i in range(16)}
    tile1Idx, tile2Idx = random.sample(range(16), 2)
    board[tile1Idx] = 2 if random.random() < .9 else 4
    board[tile2Idx] = 2 if random.random() < .9 else 4

def simulateGame(strategy):
    currentBoard = randomBoard()
    while len(SearchAgents.getLegalMoves(currentBoard)) > 0:
        currentBoard = strategy.move(currentBoard)[0](currentBoard)[0]
        currentBoard = generatePiece(currentBoard)
    return topPiece(currentBoard)

def generatePiece(board):
    emptyCords = {i for i in range(16) if board[i] == 0}
    board[emptyCords.pop()] = 2 if random.random() < .9 else 4


def topPiece(board):
    return max(board.values())
    






 





 