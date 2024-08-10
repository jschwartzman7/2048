#import Simulations.gameBoard as gb
from simulations import simulateGame, scoreAgent
import searchAgents as sa
import evaluationFunctions as ef
import time
from constants import snakePaths, np

def main():
    t0 = time.time()
    for i in range(5):
        print(i)
        simulateGame(sa.MinimaxAlphaBeta(ef.cornerSnakeStrength, maxDepth=2))
    
    #board = np.array([256, 256, 128, 128, 0, 0, 64, 32, 0, 32, 0, 0, 0, 4, 4, 2])
    #board = np.array([2, 2, 2, 99])
    #print(shiftedArray(board))

    print("simulation", time.time()-t0, " seconds")

if __name__ == "__main__":
    main()