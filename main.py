#import Simulations.gameBoard as gb
from Bot2048.simulations import simulateGame, simulateLateGame, userPlayGame
from Bot2048.gameBoard import randomStartingBoard, randomTestBoardWeighted, hashInt
import Bot2048.searchAgents as sa
import Bot2048.evaluationFunctions as ef
from Testing.moveTests import testMove
from Testing.evaluationTests import testEvalutaionFunctions


def main():
    agents = sa.MinimaxAlphaBeta()
    simulateLateGame(agents)
    
   
    
if __name__ == "__main__":
    main()