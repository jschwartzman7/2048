from agents.basicagents import Agent, Random, Priority
import agents.searchagents as sa
import agents.montecarloagents as ma
import boardevaluation.evaluationfunctions as ef
from simulations import simulateGame
import matplotlib.pyplot as plt
import time
import numpy as np
from utils import colors

'''
Statistics for scoring agents performance with varying configurations: evaluation function, search strategy, time,...
For scoring agent a over n rounds:
- tileSums: sum of all tiles on the board at the end of each round
- maxTiles: maximum tile on the board at the end of each round
- roundTimes: time taken to complete each round
'''

basicAgents = [Random(), Priority()]
searchAgents = [sa.Reflex(), sa.Expectimax(), sa.ExpectimaxAlpha(), sa.MinimaxAlphaBeta()]
monteCarloAgents = [ma.PureMonteCarlo(), ma.MCTSAgent()]

def testBasicAgents():
    for agent in basicAgents:
        print("Simulating" + agent)
        print(simulateGame(agent))
        print()

def testSearchAgents():
    for agent in searchAgents:
        print("Simulating" + agent)
        print(simulateGame(agent))
        print()

def testMonteCarloAgents():
    for agent in monteCarloAgents:
        print("Simulating" + agent)
        print(simulateGame(agent))
        print()

def testAllAgents():
    for agent in basicAgents + searchAgents + monteCarloAgents:
        print("Simulating" + agent)
        print(simulateGame(agent))
        print()

def testAgents(agents:list[Agent]=basicAgents):
    for agent in agents:
        print("Simulating" + agent)
        print(simulateGame(agent))
        print()


def assessAgent(agent:Agent, numRounds:int):
    maxTiles = []
    tileSums = []
    for i in range(numRounds):
        if i % 25 == 0:
            print(agent, i)
        endBoard = simulateGame(agent)
        maxTile = endBoard.max()
        tileSum = endBoard.sum()
        maxTiles.append(maxTile)
        tileSums.append(tileSum)
    return maxTiles, tileSums

def displayAssessAgents(agents:list[Agent], numRounds:int):
    fig, axes = plt.subplots(2, len(agents), figsize=(14, 5))
    for i, agent in enumerate(agents):
        maxTiles, tileSums = assessAgent(agent, numRounds)
        
        # Plot max tiles
        curPlot = axes[0][i]
        curPlot.set_title(str(agent)+' - Max Tiles')
        minMaxTiles = int(np.log2(min(maxTiles)))
        maxMaxTiles = int(np.log2(max(maxTiles)))
        exponentRange = range(minMaxTiles, maxMaxTiles+1)
        usedColors = [(colors['TILE_VALUE_COLORS'][np.exp2(lv)][0]/255, colors['TILE_VALUE_COLORS'][np.exp2(lv)][1]/255, colors['TILE_VALUE_COLORS'][np.exp2(lv)][2]/255) for lv in exponentRange]
        curPlot.bar(exponentRange, [maxTiles.count(np.exp2(lv)) for lv in exponentRange], width=1, color=usedColors)
        curPlot.set_xticks(exponentRange, [str(int(np.exp2(lv))) for lv in exponentRange])
        curPlot.set_xlabel('Max Tile')
        
        # Plot tile sums
        curPlot = axes[1][i]
        curPlot.hist(tileSums)
        curPlot.set_xlabel('Tile Sum')
        
    plt.show()
   
def main():
    displayAssessAgents([Random(), sa.Reflex(ef.snakeStrength), sa.Expectimax(ef.snakeStrength)], numRounds=100)

if __name__ == "__main__":
    main()