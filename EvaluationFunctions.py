import math
import GameBoard2048 as gb
import numpy as np


def defaultEval(board):
    boardCenter = center(board)
    return math.log2(max(board)) + len(gb.emptyIndices(board)) - standardDeviation(board, boardCenter) - distanceCenterCorner(boardCenter)

def centerNumpy(board): # board is 2D numpy array
    loggedBoard = np.log2(board, where=board>0)
    return np.sum(loggedBoard*np.arange(4))/np.sum(loggedBoard), np.sum(np.transpose(loggedBoard)*np.arange(4))/np.sum(loggedBoard)

def center(board):
    '''
    log weighted average 2D position of board
    range is (0, 0) to (3, 3)
    '''
    loggedBoard = [math.log2(board[i]) if board[i] > 0 else 0 for i in range(16)]
    xyWeightedCords = [(loggedBoard[i]*gb.to2D(i)[0], loggedBoard[i]*gb.to2D(i)[1]) for i in range(16)]
    xWeightedSum = sum([cord[0] for cord in xyWeightedCords])
    yWeightedSum = sum([cord[1] for cord in xyWeightedCords])
    return xWeightedSum/sum(loggedBoard), yWeightedSum/sum(loggedBoard)

def standardDeviationNumpy(board, center):
    '''
    standard deviation of log weighted board using getCenter as average
    range is 0 to x < uhh
    ''' 
    loggedBoard = np.log2(board, where=board>0)
    return np.sqrt(np.sum(loggedBoard*np.sum(np.square(np.flip(np.stack(np.indices((4, 4)),axis=-1),axis=-1)-center),axis=-1)))
    

def standardDeviation(board, center):
    '''
    standard deviation of log weighted board using getCenter as average
    range is 0 to x < uhh
    ''' 
    loggedBoard = [math.log2(board[i]) if board[i] > 0 else 0 for i in range(16)]
    variance = sum([math.pow(math.dist(center, gb.to2D(i)), 2)*loggedBoard[i] if board[i] > 0 else 0 for i in range(16)])
    return math.sqrt(variance)

def distanceCenterCorner(center):
    '''
    Minimum distance from getCenter to a corner
    '''
    return transformDistanceCenterCorner(min([math.dist(center, corner) for corner in [(0, 0), (0, 3), (3, 0), (3, 3)]]))

def transformDistanceCenterCorner(d):
    return 5*d

def transformStandardDeviation(sd):
    return sd - 5

class EvaluationFunction:

    def __init__(self, parameters):
        self.parameters = parameters

    def evaluation(self, board):
        return 0

    def evaluateBoard(self, board):
        boardCenter = center(board)
        return np.dot([math.log2(max(board)), len([i for i in range(16) if board[i] == 0]), standardDeviation(board, boardCenter), distanceCenterCorner(boardCenter)], self.parameters)
    
    def maxTileEval(self, board):
        return max(board)*self.parameters
    
    def numEmptyEval(self, board):
        return len([i for i in range(16) if board[i] == 0])*self.parameters
    
    def standardDeviationEval(self, board):
        return standardDeviation(board, center(board))*self.parameters
    
    def distCenterCornerEval(self, board):
        return distanceCenterCorner(center(board))*self.parameters
    

'''board = gb.randomBoard()
gb.printBoard(board)
print("center: ", center(board))
print("SD: ", standardDeviation(board, center(board)))
print()
print("NUMPY")
numpyBoard = np.array(board).reshape(4, 4)
print(numpyBoard)
print("center: ", centerNumpy(numpyBoard))
print("SD: ", standardDeviationNumpy(numpyBoard, centerNumpy(numpyBoard)))'''