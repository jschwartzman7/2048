import pygad
import Simulations
from EvaluationFunctions import EvaluationFunction
import SearchAgents


def fitnessFunction(gaInstance, parameters, solutionIdx): # parameters = [x, y, z, ...] "weights"
    '''
    agent(evaluationFunction(parameters))
    Run n 2048 game simulations with agent
    return avg MaxTile
    '''
    evaluationFunction = EvaluationFunction(parameters)
    agent = SearchAgents.peacefulSearch(evaluationFunction.evaluateBoard)
    return Simulations.agentAvgScore(agent, 6)




def generation(gad):
    print("here")


gaInstance = pygad.GA(5, 2, fitnessFunction, num_genes=2, sol_per_pop=5, mutation_num_genes=1, on_generation=generation)

gaInstance.run()
solution, solution_fitness, solution_idx = gaInstance.best_solution()
print(f"Parameters of the best solution : {solution}")
print(f"Fitness value of the best solution = {solution_fitness}")
print(f"Index of the best solution : {solution_idx}")

#print(fitnessFunction(0, [1, 1], 0))