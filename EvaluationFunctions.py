import math
import numpy as np
'''
board = GameBoard2048()
'''



def calculateCenter(board):
    xPosSum = 0
    yPosSum = 0
    for i in range(16):
        x, y = board.get2DCord(i)
        xPosSum += board[i]*x
        yPosSum += board[i]*y
    return (xPosSum/board.getSumTiles(), yPosSum/board.getSumTiles())
            
def calculateSD(board, center):
    variance = 0
    for i in range(16):
        if board[i] != 0:
            variance += math.pow(math.dist(center, board.get2DCord(i)), 2)*board[i]
    return math.sqrt(variance)


def getMaxTile(board):
        return max(board)
    
   

def getEmptyIndices(board):
        return [i for i in range(16) if board[i] == 0]
        

class EvaluationFunction:

    def __init__(self, parameters):
        self.parameters = parameters

    def evaluateBoard(self, GameBoard):
        boardFeatures = [math.log2(getMaxTile(GameBoard)), len(getEmptyIndices(GameBoard))]
        return self.parameters[0]*boardFeatures[0] + self.parameters[1]*boardFeatures[1]

