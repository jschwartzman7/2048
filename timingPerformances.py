import time
from Bot2048.simulations import simulateGame
import Bot2048.searchAgents as sa


def timeAgent(agent, numRounds:int=1, startingBoard=None):
    print("timing agent ", agent, " for ", numRounds, " rounds")
    t0 = time.time()
    for i in range(numRounds):
       simulateGame(agent)
    print("time to run ", numRounds, " rounds: ", time.time()-t0)




def main():
    t0 = time.time()
    timeAgent(sa.MinimaxAlphaBeta())
    print("simulation", time.time()-t0, " seconds")

if __name__ == "__main__":
    main()