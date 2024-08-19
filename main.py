from Bot2048.simulations import simulateGame, simulateLateGame, userPlayGame, assessAgent, userPlayGame, displayAgentAssessment
from Bot2048.gameBoard import randomStartingBoard, randomTestBoardWeighted, hashInt
import Bot2048.searchAgents as sa
import Bot2048.evaluationFunctions as ef
from Testing.moveTests import testMove
from Testing.evaluationTests import testEvalutaionFunctions
import numpy as np


def main():
    #agents = [sa.MinimaxAlphaBeta(maxDepth=1)]
    #displayAgentAssessment(agents, 1)
    simulateGame(sa.MCTSAgent(moveTimeLimit=1))
    
if __name__ == "__main__":
    main()