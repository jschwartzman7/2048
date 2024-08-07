import math
from constants import snakePaths, cornerControl2, np
#import constants

'''
'Evaluate relative value of board to its current tile set'
bound [0, M]
ef: R^16 -> R
'''
M=100
def log2Board(board:np.ndarray) -> np.ndarray:
    return np.log2(board, where=board>0)

def defaultEval(board) -> float:
    loggedBoard = np.log2(board, where=board>0)
    snake = snakeStrength(loggedBoard)
    center = centerNumpy(loggedBoard)
    std = standardDeviationNumpy(loggedBoard, center)
    value = 2*(snake-np.count_nonzero(board)-std)
    value = min(100, max(-100, value))
    return value

def highestPiece(logBoard: np.ndarray) -> float:
    maxs = np.nonzero(logBoard==np.max(logBoard))

    diff = 0
    for i in range(len(maxs[0])):
        x, y = maxs[0][i], maxs[1][i]
        rows = [-1, 0, 1]
        cols = [-1, 0, 1]
        if x == 3:
            rows = [-1, 0]
        elif x == 0:
            rows = [0, 1]
        if y == 3:
            cols = [-1, 0]
        elif y == 0:
            cols = [0, 1]
        for row in rows:
            for col in cols:
                if logBoard[x+row, y+col] != 0 and (np.abs(row-col) == 1):
                    diff += abs(logBoard[x, y] - logBoard[x+row, y+col])
    return np.divide(1, diff/len(maxs[0]))


def cornerSnakeStrength(logBoard: np.ndarray) -> float:
    return np.mean([cornerStrength(logBoard), snakeStrength(logBoard)])


def constantEvaluationFunction(board=None):
    return 0

def snakeStrength(logBoard: np.ndarray) -> float:
    # relative strength of current board. 0 = worst, 1 = best
    snakedBoards = np.apply_along_axis(lambda path: logBoard[tuple(path)], 1, snakePaths)
    optimalBoard = np.flip(np.sort(logBoard.flatten()))
    return np.max(np.apply_along_axis(lambda masked: np.dot(masked, optimalBoard), 1, snakedBoards))/np.sum(np.square(logBoard))
   
def cornerStrength(logBoard: np.ndarray) -> float:
    optimalBoard = np.flip(np.sort(logBoard.flatten()))
    optimalVector = np.array([optimalBoard[0], np.mean(optimalBoard[1:3]), np.mean(optimalBoard[3:6]), np.mean(optimalBoard[6:10]), np.mean(optimalBoard[10:13]), np.mean(optimalBoard[13:15]), optimalBoard[15]])
    return np.max([np.dot(optimalVector, np.array([np.mean(logBoard[tuple(diag)]) for diag in corner])) for corner in cornerControl2])/np.dot(optimalVector, optimalVector)

def centerNumpy(logBoard): # board is 2D numpy array
    return np.sum(logBoard*np.arange(4))/np.sum(logBoard), np.sum(np.transpose(logBoard)*np.arange(4))/np.sum(logBoard)

def standardDeviationNumpy(logBoard, center):
    '''
    standard deviation of log weighted board using getCenter as average
    range is 0 to x < uhh
    ''' 
    return np.sqrt(np.sum(logBoard*np.sum(np.square(np.stack(np.indices((4, 4)),axis=-1)-center),axis=-1)))
    

if __name__ == "__main__":
    pass
  