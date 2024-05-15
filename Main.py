import Bot2048
from Bot2048 import Bot2048
import SearchAgents
import EvaluationFunctions

#TestCases.testFunctions(TestCases.randomTestBoards)
#TestCases.testEvaluationFunction(EvaluationFunctions.evaluate)

#weights that reached 2048: [0.04, 0.13, 0.34, 0.36], [-0.21, 0.13, 0.34, 0.485]?, [-0.12666666666666665, 0.29666666666666663, 0.17333333333333337, -0.14]?
# [0.2, 0.4, 0.6, 0.2] ?
#Bot2048(randomSearch()).play()


ok = Bot2048(SearchAgents.reflexSearch(EvaluationFunctions.evaluate2))
ok.board[0]=2048
ok.board[1]=2048
ok.board[2]=2048
ok.board[3]=2048
ok.printBoard()
ok.agent.moveRight(ok.board)
print()

ok.printBoard()
ok.agent.moveRight(ok.board)
print()
ok.printBoard()
ok.agent.moveLeft(ok.board)
print()
ok.printBoard()

