import time
from constants import rand, np
from gameBoard import randomStartingBoard, generatePiece
from searchAgents import getLegalMoves, moveInDirection

def simulateGame(agent):
    gameBoard = randomStartingBoard()
    legalMoves = getLegalMoves(gameBoard)
    time0 = time.time()
    while len(legalMoves) > 0:
        gameBoard = agent.getMove(gameBoard, legalMoves)(gameBoard)
        print("moved")
        gameBoard = generatePiece(gameBoard)
        legalMoves = getLegalMoves(gameBoard)
    print("max tile", max(gameBoard.flatten()))
    return max(gameBoard.flatten())

def scoreAgent(agent, numRounds):
    maxTiles = []
    #sumTiles = []
    for n in range(numRounds):
        print(n)
        maxTile = simulateGame(agent)
        maxTiles.append(maxTile)
    return np.median(maxTiles)
   
def userPlayGame():
    gameBoard = randomStartingBoard()
    print("board")
    print(gameBoard)
    while len(getLegalMoves(gameBoard)) > 0:
        text =input("Your move: ")
        print("Moving ", text)
        directionFunc = moveInDirection(text)
        if directionFunc != None:
            gameBoard = moveInDirection(text)(gameBoard)
            print(gameBoard)
            gameBoard = generatePiece(gameBoard)
            print("New piece added")
            print(gameBoard)
        else:
            print("Invalid move.  Re-enter your move")
    print("Game Over")
    print("Highest tile: ", max(gameBoard))
    print("Total score: ", sum(gameBoard))


if __name__ == "__main__":
    pass