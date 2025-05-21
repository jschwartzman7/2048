import numpy as np
import matplotlib as plt
from sklearn.neighbors import KNeighborsClassifier
from agents.basicagents import Agent
from agents.searchagents import Search
import boardevaluation.evaluationfunctions as ef
from simulations import simulateGame
from skopt import gp_minimize
from skopt.space import Real
from skopt.plots import plot_convergence


'''
[Board vector]: moveLabel, ... is used to fit a kNN model
model.fit(BoardVectors, directionKeys[moveLabel])
model.predict(inputBoard.flatten())
'''
class KnnAgent(Agent):

    directionKeys = {
        'moveUp': 0,
        'moveDown': 1,
        'moveLeft': 2,
        'moveRight': 3,
    }

    def __init__(self, n_neighbors=3):
        self.nNeighbors = n_neighbors
        self.classifier = KNeighborsClassifier(n_neighbors=self.nNeighbors)
        self.trainModel("datacollection/moves.txt")

    def trainModel(self, trainingDataFileName):
        X, y = self.parseTrainingData(trainingDataFileName)
        self.classifier.fit(X, y)

    def parseTrainingData(self, trainingDataFileName):
        # Load training data from a file
        with open(trainingDataFileName, 'r') as file:
            lines = file.readlines()
            XTrain = []
            yTrain = []
            for line in lines:
                splitLine = line.split(' ')
                xVector = []
                for v in range(16):
                    xVector.append(float(splitLine[v]))
                XTrain.append(xVector)
                yTrain.append(line.split(" ")[-1])
        XTrain = np.array(XTrain)
        yTrain = np.array(yTrain)
        return XTrain, yTrain

    def predict(self, X):
        return self.classifier.predict(X)
    
    def __str__(self):
        return 'KNN Agent'

    def getMove(self, board:np.ndarray) -> callable:
        boardVector = board.flatten()
        return self.predict([boardVector])
    
'''
    Grid Search for hyperparameter tuning
    Run simulations with different coefficients for evaluation functions
    Select coefficients that score the highest
'''
class ParameterTuner:
    def __init__(self, agent:Search):
        self.evaluationFunctions = [ef.snakeStrength, ef.cornerStrength, ef.tileCompactness, ef.surrounded, ef.highestPiece]
        self.parameterRanges = [Real(-1,1) for function in self.evaluationFunctions]
        self.agent = agent
        self.numRounds = 3

    def objective(self, parameters):
        def evaluationFunction(board:np.ndarray) -> float:
            score = 0
            for i, function in enumerate(self.evaluationFunctions):
                score += function(board)*parameters[i]
            return ef.regularizeContinuous(score)
        self.agent.evaluationFunction = evaluationFunction
        score = np.log2(simulateGame(self.agent).sum())
        return -score

    def callbackFunction(self, res):
        print("Callback: ", res.x, res.fun)

    def optimize(self):
        func = self.objective
        dimensions = self.parameterRanges
        n_calls=20
        verbose=True
        callback=self.callbackFunction
        result = gp_minimize(func=func, dimensions=dimensions, n_calls=n_calls, verbose=verbose, callback=callback)
        print("RESULT: ", result)
        plot_convergence(result)
        plt.show()
    