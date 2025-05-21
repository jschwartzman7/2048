from game.gameboard import getLegalMoves
from utils import np, rand

class Agent:

    def __str__(self):
        return 'Abstract Agent'
    
    def precompute(self):
        pass

    def getMove(self, board:np.ndarray) -> callable:
        pass
    
class Random(Agent):

    def __str__(self):
        return 'Random Agent'

    def getMove(self, board:np.ndarray) -> callable:
        legalMoves = getLegalMoves(board)
        if len(legalMoves) == 0:
            return None
        return legalMoves[rand.integers(0, len(legalMoves))]
        
class Priority(Agent):

    def __str__(self):
        return 'Priority Agent'

    def getMove(self, board:np.ndarray) -> callable:
        legalMoves = getLegalMoves(board)
        if len(legalMoves) == 0:
            return None
        return legalMoves[0]