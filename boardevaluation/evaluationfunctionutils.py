from utils import np
import math

MAX = 3

def regularizeDiscrete(value: float) -> float:
    if value < MAX:
        return value
    else:
        return MAX
    
def regularizeContinuous(value: float) -> float:
    return MAX/(1+math.exp(2-4*value/MAX))

def getOptimalTileset(board:np.ndarray) -> np.ndarray:
    optimalBoard = []
    tileSum = board.sum()
    while tileSum > 0:
        maxTile = np.power(2, int(np.log2(tileSum)))
        optimalBoard.append(maxTile)
        tileSum -= maxTile
    return np.pad(optimalBoard, (0, 16-len(optimalBoard)))