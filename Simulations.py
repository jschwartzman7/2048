from GameBoard2048 import GameBoard
import SearchAgents
from SearchAgents import Search
import random


gameBoard = GameBoard()
basicAgent = Search()



def randomStartingBoard():
    board = [0]*16
    tile1Idx, tile2Idx = random.sample(range(16), 2)
    board[tile1Idx], board[tile2Idx] = 2 if random.random() < .9 else 4, 2 if random.random() < .9 else 4
    return board

def simulateGame(agent):
    gameBoard.board = randomStartingBoard()
    while len(agent.getLegalMoves(gameBoard.board)) > 0:
        #bot.printBoard()
        agent.getMove(gameBoard.board)(gameBoard.board)
        #bot.printBoard()
        gameBoard.generatePiece()
    return gameBoard.getMaxTile()

def agentAvgScore(agent, numRounds):
    sumMaxTiles = 0
    for n in range(numRounds):
        sumMaxTiles += simulateGame(agent)
    return sumMaxTiles / numRounds


def userPlayGame():
    gameBoard.board = randomStartingBoard()
    gameBoard.printBoard()
    userMoved = False
    while len(basicAgent.getLegalMoves(gameBoard.board)) > 0:
        while not userMoved:
            match input("Your move: "):
                case "up":
                    if basicAgent.canMoveUp(gameBoard.board):
                        print("Moving up")
                        basicAgent.moveUp(gameBoard.board)
                        gameBoard.printBoard()
                        userMoved = True
                    else:
                        print("Cannot move up.  Make a different move")

                case "down":
                    if basicAgent.canMoveDown(gameBoard.board):
                        print("Moving down")
                        basicAgent.moveDown(gameBoard.board)
                        gameBoard.printBoard()
                        userMoved = True
                    else:
                        print("Cannot move down.  Make a different move")
                    
                case "left":
                    if basicAgent.canMoveLeft(gameBoard.board):
                        print("Moving left")
                        basicAgent.moveLeft(gameBoard.board)
                        gameBoard.printBoard()
                        userMoved = True
                    else:
                        print("Cannot move left.  Make a different move")
                    
                case "right":
                    if basicAgent.canMoveRight(gameBoard.board):
                        print("Moving right")
                        basicAgent.moveRight(gameBoard.board)
                        gameBoard.printBoard()
                        userMoved = True
                    else:
                        print("Cannot move right.  Make a different move")
                    
                case _:
                    print("Invalid move.  Make a different move")
        emptyCords = gameBoard.getEmptyIndices()
        if len(emptyCords) > 0:
            print("New piece...")
            random.shuffle(emptyCords)
            gameBoard.board[emptyCords[0]] = 2 if random.random() < .9 else 4
            gameBoard.printBoard()
        userMoved = False
    print("Game Over. Highest tile: ", gameBoard.getMaxTile())





 





 