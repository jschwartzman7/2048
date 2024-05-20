import GameBoard2048
from GameBoard2048 import GameBoard
import SearchAgents
import EvaluationFunctions
import Simulations

#TestCases.testFunctions(TestCases.randomTestBoards)
#TestCases.testEvaluationFunction(EvaluationFunctions.evaluate)

#weights that reached 2048: [0.04, 0.13, 0.34, 0.36], [-0.21, 0.13, 0.34, 0.485]?, [-0.12666666666666665, 0.29666666666666663, 0.17333333333333337, -0.14]?
# [0.2, 0.4, 0.6, 0.2] ?
#Bot2048(randomSearch()).play()

evalFunction = EvaluationFunctions.EvaluationFunction([0.04110188, 0.31855271])


agent = SearchAgents.peacefulSearch(evalFunction.evaluateBoard, 3)

print("Averagte max tile:", Simulations.agentAvgScore(agent, 20))
