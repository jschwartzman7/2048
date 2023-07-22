import random
import TestCases
import Search
import EvaluationFunctions
from EvaluationFunctions import evaluate
'''
Methods to train feature weights:
    Random Search
        Select n random tuples of hyperparameters/weights from the domain
        For each tuple:
            Determine an accuracy score based on game simulations
        Select tuple with highest accuracy score

    Grid Search
        Select n tuples of hyperparameters/weights from spaced intervals from the domain
        For each tuple:
            Determine an accuracy score based on game simulations
        Select tuple with highest accuracy score

    Evolutionary Search
        Start with n tuples of random or chosen hyperparameters
        Until desired outcome:
            Run simulations and record an accuracy score for each tuple
            Keep highest scoring tuples and change lowest scoring tuples by evolutionary processes like inheritance, mutation, natural selection from higheset scoring tuples
        Select tuple with highest accuracy score

    Random Evolutionary Search:
        Select n random tuples of hyperparameters/weights from the domain
        Until desired outcome:
            For each tuple:
                Determine an accuracy score based on game simulations
            Keep highest scoring tuples and change lowest scoring tuples by evolutionary processes like inheritance, mutation, natural selection from higheset scoring tuples
        Select tuple with highest accuracy score
'''

def evolutionSearch():
    weightsLength = 4
    numCandidates = 16
    numSurviving = 8
    numRounds = 15
    numTestsPerWeightVector = 8
    topScoringWeight = []
    topScore = 0

    randomWeightsVectors = [[100*random.random()-50 for i in range(weightsLength)] for j in range(numCandidates)]
    for i in range(numRounds):
        # evaluate all candidates
        print("Pass ", i+1)
        scoresMap = dict()
        for weightVector in randomWeightsVectors:
            strategy = Search.reflexSearch(evaluate, weightVector)
            trialScores = []
            for j in range(numTestsPerWeightVector):
                maxTile = TestCases.simulateGame(strategy)
                trialScores.append(maxTile)
            scoresMap[(sum(trialScores)/numTestsPerWeightVector)] = weightVector
        # select best candidates
        trialScores = list(scoresMap.keys())
        trialScores.sort()
        if trialScores[-1] > topScore:
            topScore = trialScores[-1]
            topScoringWeight = scoresMap[topScore]
        trialScores = trialScores[numSurviving:]
        print("Top average scores: ", trialScores[-4:])
        survivingWeights = [scoresMap[score] for score in trialScores]
        # reproduce new candidates
        averageSurvivingWeights = []
        for k in range(weightsLength):
            sum2 = 0
            for w in range(len(survivingWeights)):
                sum2 += survivingWeights[w][k]
            averageSurvivingWeights.append(sum2/len(survivingWeights))
        for m in range(int(numCandidates/4)):
            newWeightVector = averageSurvivingWeights
            for entry in newWeightVector:
                entry += 4/(i+1)*random.random()-2/(i+1)
            randomWeightsVectors.append(newWeightVector)
        for n in range(int(numCandidates/4)):
            randomWeightsVectors.append([100*random.random()-50 for i in range(weightsLength)])
        print()
    print("Best weight: ", topScoringWeight, topScore)

def gridSearch(numIntervals):
    #features: numEmpty, mergeValues, distanceToCenter, sd
    strategy = Search.reflexSearch(EvaluationFunctions.evaluate, [1, 1, 1, 1])
    avgMaxTiles = dict()
    for h in [x/numIntervals for x in range(0, numIntervals)]:
        print(h)
        for i in [x/numIntervals for x in range(0, numIntervals)]:
            for j in [x/numIntervals for x in range(0, numIntervals)]:
                for k in [x/numIntervals for x in range(0, numIntervals)]:
                    weightVector = [h, i, j, k ]
                    strategy.weights = weightVector
                    avgMaxTile = TestCases.runSimulations([strategy], 7)
                    avgMaxTiles[avgMaxTile] = weightVector
                    #if curMaxTile > maxTile:
                        #maxTile = curMaxTile
    maxTilesList = list(avgMaxTiles.keys())
    bestWeights = avgMaxTiles[max(maxTilesList)]
    print(max(maxTilesList), bestWeights)

def randomSearch(numIntervals):
    #features: numEmpty, mergeValues, distanceToCenter, sd
    strategy = Search.reflexSearch(EvaluationFunctions.evaluate, [1, 1, 1, 1])
    avgMaxTiles = dict()
    for h in [random.random() for x in range(0, numIntervals)]:
        print(h)
        for i in [random.random() for x in range(0, numIntervals)]:
            for j in [random.random() for x in range(0, numIntervals)]:
                for k in [random.random() for x in range(-numIntervals, 0)]:
                    weightVector = [h, i, j, k]
                    strategy.weights = weightVector
                    avgMaxTile = TestCases.runSimulations([strategy], 10)
                    avgMaxTiles[avgMaxTile] = weightVector
    maxTilesList = list(avgMaxTiles.keys())
    bestWeights = avgMaxTiles[max(maxTilesList)]
    print(max(maxTilesList), bestWeights)

def constantSearch(numIntervals):
    strategy = Search.reflexSearch(EvaluationFunctions.evaluate,[.5, .5, .5, .5])
    for round in range(2*len(strategy.weights)):
        averageScores = dict()
        for i in [x/numIntervals for x in range(0, numIntervals)]:
            strategy.weights[round%len(strategy.weights)] = i
            averageScore = TestCases.runSimulations([strategy], 10)
            averageScores[averageScore] = i
        averageScoresList = list(averageScores.keys())
        newWeight = averageScores[max(averageScoresList)]
        print("max average score: ", max(averageScoresList))
        strategy.weights[round%len(strategy.weights)] = newWeight
        print("weights used: ", strategy.weights)
        print()

constantSearch(10)