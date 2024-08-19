import time
from Bot2048.constants import rand, np
from Bot2048.gameBoard import randomStartingBoard, generatePiece, randomTestBoardWeighted
from Bot2048.searchAgents import getLegalMoves, moveInDirection, Agent
import matplotlib.pyplot as plt


def simulateGame(agent):
    gameBoard = randomStartingBoard()
    legalMoves = getLegalMoves(gameBoard)
    while len(legalMoves) > 0:
        gameBoard = agent.getMove(gameBoard, legalMoves)(gameBoard)
        print(gameBoard)
        print()
        #print("moved")
        gameBoard = generatePiece(gameBoard)
        legalMoves = getLegalMoves(gameBoard)
    return gameBoard.max(), gameBoard.sum()

def simulateLateGame(agent):
    gameBoard = randomTestBoardWeighted(maxTileExponent=7, numFilled=rand.choice([8, 9, 10, 11]))
    legalMoves = getLegalMoves(gameBoard)
    maxNow = gameBoard.max()
    while len(legalMoves) > 0:
        gameBoard = agent.getMove(gameBoard, legalMoves)(gameBoard)
        gameBoard = generatePiece(gameBoard)
        legalMoves = getLegalMoves(gameBoard)
    #print("max first", maxNow)
    #print("max tile", max(gameBoard.flatten()))
    return gameBoard.max()

def assessAgent(agent:Agent, numRounds:int=10):
    print(agent)
    maxTiles = []
    tileSums = []
    roundTimes = []
    t0 = time.time()
    for i in range(numRounds):
        maxTile, tileSum = simulateGame(agent)
        roundTimes.append(time.time()-t0)
        t0 = time.time()
        maxTiles.append(maxTile)
        tileSums.append(tileSum)
    return maxTiles, tileSums, roundTimes

def displayAgentAssessment(agents:list[Agent], numRounds:int=10):
    axes = plt.subplots(3, len(agents))[1]
    for i, agent in enumerate(agents):
        maxTiles, tileSums, times = assessAgent(agent, numRounds)
        curPlot = axes[0][i]
        curPlot.set_title(agent)
        curPlot.hist(maxTiles)
        curPlot = axes[1][i]
        curPlot.hist(tileSums)
        curPlot.set_title("Tile sums")
        curPlot = axes[2][i]
        curPlot.hist(times)
    plt.show()
   
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
    userPlayGame()