#import Simulations.gameBoard as gb
from simulations import simulateGame, userPlayGame
from gameBoard import randomStartingBoard, randomTestBoardWeighted
import searchAgents as sa
import evaluationFunctions as ef
from constants import snakePaths, testBoards, rand, np


def main():
    #agent = sa.ExpectimaxAlphaSearch(evaluationFunction=ef.defaultEval, maxDepth=0, newTileMax=3)
    #agent = sa.ExpectimaxSearch(evaluationFunction=ef.control, maxDepth=3, newTileMax=4)
    #print(simulateGame(agent))
    #print(simulateGame(agent))
    
    userPlayGame()


if __name__ == "__main__":
    main()