import pygad
import Bot2048.searchAgents as sa
import Bot2048.evaluationFunctions as ef
from Bot2048.simulations import simulateLateGame, simulateGame
import numpy as np

agent = sa.Reflex(None)

def fitnessFunction(gaInstance, parameters, solutionIdx):
    '''
    agent(evaluationFunction(parameters))
    Run n 2048 game simulations with agent
    return avg MaxTile
    '''
    print("parameters", parameters)
    agent.evaluationFunction.evaluationParameters = parameters
    return np.median([simulateGame(agent) for i in range(5)])
   



def generation(gad):
    print(gad.generations_completed)

def begin(gad):
    print("Running GA")
    print(gad.valid_parameters)

numGenerations = 10
numParentsMating = 3
numSolutionsPerGeneration = 5
solutionLength = 3
initialParameterMin = -1
initialParameterMax = 1
numSolutionsRetainedPerGeneration = 4
probabilityMutation = 0.35
probabilityCrossover = 0.25
mutationMinValue = -.5
mutationMaxVal = .5


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


print("BBB")
gaInstance.run()
solution, solution_fitness, solution_idx = gaInstance.best_solution()
print(f"Parameters of the best solution : {solution}")
print(f"Fitness value of the best solution = {solution_fitness}")
print(f"Index of the best solution : {solution_idx}")
gaInstance.plot_fitness()
gaInstance.plot_new_solution_rate()
gaInstance.plot_genes()


#print(fitnessFunction(0, [1, 1], 0))