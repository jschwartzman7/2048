from utils import np, rand
import boardevaluation.evaluationfunctions as ef


class BoardEvaluator:

    DEFAULT_EVALUATION_FUNCTION = ef.numEmpty

    def __init__(self):
        pass

    def evaluate(self, board:np.ndarray) -> float:
        return self.DEFAULT_EVALUATION_FUNCTION(board)

class SingleFunctionEvaluator(BoardEvaluator):

    def __init__(self, evaluationFuncion:callable):
        self.evaluationFunction = evaluationFuncion

    def evaluate(self, board:np.ndarray) -> float:
        return self.evaluationFunction(board)

class MultipleFunctionEvaluator(BoardEvaluator):
    
    def __init__(self, evaluationFunctions:list=[ef.snakeStrength, ef.cornerStrength, ef.surrounded, ef.tileCompactness]):
        self.evaluationFunctions:list[callable] = evaluationFunctions
        self.Size = len(evaluationFunctions)
        self.functionCoefficients = [1]*self.Size

    def __str__(self):
        return str(self.evaluationFunctions) + str(self.functionCoefficients)

    def setCoefficients(self, parameters:list):
        assert len(parameters) == len(self.evaluationFunctions)
        self.functionCoefficients = parameters

    def setEvaluationFunctions(self, functions:list[callable]):
        self.evaluationFunctions = functions

    def evaluate(self, board:np.ndarray) -> float:
        boardValues = [evaluationFunction(board) for evaluationFunction in self.evaluationFunctions]
        boardValue = 0
        for i in range(len(boardValues)):
            boardValue += boardValues[i]*self.functionCoefficients[i]
        return boardValue