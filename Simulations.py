import GameBoard2048 as gb
import SearchAgents as sa
import EvaluationFunctions as ef
import random
import matplotlib.pyplot as plt
import random
import numpy as np


def randomStartingBoard():
    board = [0]*16
    tile1Idx, tile2Idx = random.sample(range(16), 2)
    board[tile1Idx], board[tile2Idx] = 2 if random.random() < .9 else 4, 2 if random.random() < .9 else 4
    return board

def randomStartingBoardNumpy():
   return np.where(np.isin(np.arange(16), np.random.choice(np.arange(16), size=2, replace=False)), np.random.choice([2,4], size=16, p=[0.9,0.1]), 0).reshape(4,4) 

def simulateGame(agent):
    gameBoard = randomStartingBoard()
    legalMoves = sa.getLegalMoves(gameBoard)
    while len(legalMoves) > 0:
        agent.getMove(gameBoard, legalMoves)(gameBoard)
        gb.generatePiece(gameBoard)
        legalMoves = sa.getLegalMoves(gameBoard)
    return max(gameBoard), sum(gameBoard)

def scoreAgent(agent, numRounds, scoreCalculation=0):
    maxTiles = []
    #sumTiles = []
    for n in range(numRounds):
        maxTile = simulateGame(agent)[0]
        maxTiles.append(maxTile)
        #sumTiles.append(sumTile)
    return np.median(maxTiles)
    '''match scoreCalculation:
        case 1: # median
            return np.median(maxTiles), np.median(sumTiles)
        case 2: # mode
            return max(maxTiles, key=maxTiles.count), max(sumTiles, key=sumTiles.count)
        case _: # mean
            return sum(maxTiles)/numRounds, sum(sumTiles)/numRounds'''
        
def userPlayGame():
    gameBoard = randomStartingBoard()
    gb.printBoard(gameBoard)
    userMoved = False
    while len(sa.getLegalMoves(gameBoard)) > 0:
        while not userMoved:
            match input("Your move: "):
                case "up":
                    if sa.canMoveUp(gameBoard):
                        print("Moving up")
                        sa.moveUp(gameBoard)
                        gb.printBoard(gameBoard)
                        userMoved = True
                    else:
                        print("Cannot move up.  Make a different move")

                case "down":
                    if sa.canMoveDown(gameBoard):
                        print("Moving down")
                        sa.moveDown(gameBoard)
                        gb.printBoard(gameBoard)
                        userMoved = True
                    else:
                        print("Cannot move down.  Make a different move")
                    
                case "left":
                    if sa.canMoveLeft(gameBoard):
                        print("Moving left")
                        sa.moveLeft(gameBoard)
                        gb.printBoard(gameBoard)
                        userMoved = True
                    else:
                        print("Cannot move left.  Make a different move")
                    
                case "right":
                    if sa.canMoveRight(gameBoard):
                        print("Moving right")
                        sa.moveRight(gameBoard)
                        gb.printBoard(gameBoard)
                        userMoved = True
                    else:
                        print("Cannot move right.  Make a different move")
                case _:
                    print("Invalid move.  Re-enter your move")
        gb.generatePiece(gameBoard)
        print("New piece added")
        gb.printBoard(gameBoard)
        userMoved = False
    print("Game Over")
    print("Highest tile: ", max(gameBoard))
    print("Total score: ", sum(gameBoard))

print(randomStartingBoardNumpy())
