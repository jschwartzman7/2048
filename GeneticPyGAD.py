import pygad
import Simulations
from EvaluationFunctions import EvaluationFunction
import SearchAgents


def fitnessFunction(gaInstance, parameters, solutionIdx): # parameters = [wLogMaxTile, wNumEmpty, wStd, wDistCenterCorner]
    '''
    agent(evaluationFunction(parameters))
    Run n 2048 game simulations with agent
    return avg MaxTile
    '''
    evaluationFunction = EvaluationFunction(parameters)
    agent = SearchAgents.ExpectimaxSearch(evaluationFunction.evaluateBoard, newTileFrac=0.3)
    return Simulations.scoreAgent(agent, 5)




def generation(gad):
    print(gad.generations_completed)

def begin(gad):
    print("Running GA")
    print(gad.valid_parameters)

numGenerations = 10
numParentsMating = 3
numSolutionsPerGeneration = 5
solutionLength = 4
initialParameterMin = -3
initialParameterMax = 3
numSolutionsRetainedPerGeneration = 4
probabilityMutation = 0.35
probabilityCrossover = 0.25
mutationMinValue = -1.7
mutationMaxVal = 1.7


gaInstance = pygad.GA(num_generations=numGenerations,
                      num_parents_mating=numParentsMating,
                      fitness_func=fitnessFunction,
                      sol_per_pop=numSolutionsPerGeneration,
                      num_genes=solutionLength,
                      init_range_low=initialParameterMin,
                      init_range_high=initialParameterMax,
                      parent_selection_type="rank",
                      keep_elitism=numSolutionsRetainedPerGeneration,
                      crossover_type="scattered",
                      crossover_probability=probabilityCrossover,
                      mutation_probability=probabilityMutation,
                      random_mutation_min_val=mutationMinValue,
                      random_mutation_max_val=mutationMaxVal,
                      on_generation=generation,
                      on_start=begin,
                      suppress_warnings=True,
                      save_best_solutions=True,
                      save_solutions=True)

gaInstance.run()
solution, solution_fitness, solution_idx = gaInstance.best_solution()
print(f"Parameters of the best solution : {solution}")
print(f"Fitness value of the best solution = {solution_fitness}")
print(f"Index of the best solution : {solution_idx}")
gaInstance.plot_fitness()

#print(fitnessFunction(0, [1, 1], 0))