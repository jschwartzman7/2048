#import Simulations.gameBoard as gb
from simulations import simulateGame, simulateLateGame, userPlayGame
from gameBoard import randomStartingBoard, randomTestBoardWeighted, hashInt
import searchAgents as sa
import evaluationFunctions as ef
from constants import snakePaths, testBoards, rand, np
from Testing.moveTests import testMove
from Testing.evaluationTests import testEvalutaionFunctions


def main():
    agents = sa.MinimaxAlphaBeta()
    simulateLateGame(agents)
    
   
    
if __name__ == "__main__":
    main()