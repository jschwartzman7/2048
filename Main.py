import Bot2048
from Bot2048 import Bot2048
import Search
from Search import expectimaxSearch
from Search import reflexSearch
from Search import randomSearch
from Search import basicSearch
import TestCases
import EvaluationFunctions
import time

#TestCases.testFunctions(TestCases.randomTestBoards)
#TestCases.testEvaluationFunction(EvaluationFunctions.evaluate)

#weights that reached 2048: [0.04, 0.13, 0.34, 0.36], [-0.21, 0.13, 0.34, 0.485]?, [-0.12666666666666665, 0.29666666666666663, 0.17333333333333337, -0.14]?
# [0.2, 0.4, 0.6, 0.2] ?
#Bot2048(randomSearch()).play()

Bot2048(expectimaxSearch(EvaluationFunctions.evaluate, [0.2, 0.4, 0.6, 0.2])).play()

random = randomSearch()
basic = basicSearch()
reflex = reflexSearch(EvaluationFunctions.evaluate, [1, 1, 1, 1])
expectimax = expectimaxSearch(EvaluationFunctions.evaluate, [1, 1, 1, 1])


strategies = [reflex]#, reflex, expectimax]
TestCases.runSimulations(strategies, 1)
'''
#Bot2048TestCases.testEvaluationFunction()
#TestCases.testFunctions(TestCases.randomTestBoards)
#search2 = Search.randomSearch()
#search3 = Search.basicSearch()
'''

