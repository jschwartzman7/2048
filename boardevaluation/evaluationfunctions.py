from utils import snakePaths, cornerControls, np
from game.gameboard import log2Board
from boardevaluation.evaluationfunctionutils import getOptimalTileset

'''
'Evaluate relative value of board to its current tile set'
bound [0, M]
ef: N^16 -> R
'''

def cornerStrength(board: np.ndarray) -> float:
    ''' corner correlation accuracy of current board. 0 = worst, 1 = best'''
    optimalBoard = np.flip(np.sort(board.flatten()))
    optimalVector = np.array([optimalBoard[0], np.mean(optimalBoard[1:3]), np.mean(optimalBoard[3:6]), np.mean(optimalBoard[6:10]), np.mean(optimalBoard[10:13]), np.mean(optimalBoard[13:15]), optimalBoard[15]])
    return np.max([np.dot(optimalVector, np.array([np.mean(board[tuple(diag)]) for diag in corner])) for corner in cornerControls])/np.sum(np.square(optimalVector))

def snakeStrength(board: np.ndarray) -> float:
    ''' snake correlation accuracy of current board. 0 = worst, 1 = best'''
    snakedBoards = np.apply_along_axis(lambda path: board[tuple(path)], 1, snakePaths)
    return np.max(np.apply_along_axis(lambda masked: np.dot(masked, np.sort(board.flatten())[::-1]), 1, snakedBoards))/np.sum(np.square(board))

def tileCompactness(board:np.ndarray) -> float:
    if np.count_nonzero(board) == 0: return 1
    return np.count_nonzero(getOptimalTileset(board))/np.count_nonzero(board)

def surrounded(board:np.ndarray) -> float:
    '''each tile should be adjacent to a non-exceeding tile'''
    logBoard = log2Board(board)
    worstTileDifference = 1
    for x, y in np.argwhere(logBoard != 0):
        bestNeighbor = 0
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            if 0 <= x+dx < 4 and 0 <= y+dy < 4:
                if logBoard[x+dx, y+dy] > logBoard[x, y]:
                    bestNeighbor = max(bestNeighbor, 1/(logBoard[x+dx, y+dy] - logBoard[x, y]+1))
                else:
                    bestNeighbor = 1
                    break
        worstTileDifference = min(worstTileDifference, bestNeighbor)
    return worstTileDifference

def highestPiece(board:np.ndarray) -> float:
    maxs = np.nonzero(board==np.max(board))
    paddedBoard = np.pad(board, 1)
    minDifference = np.min([np.min([board[maxs[0][i], maxs[1][i]] - paddedBoard[maxs[0][i]+1+row, maxs[1][i]+1+col] if paddedBoard[maxs[0][i]+1+row, maxs[1][i]+1+col] != 0 and paddedBoard[maxs[0][i]+1+row, maxs[1][i]+1+col] != paddedBoard[maxs[0][i]+1, maxs[1][i]+1] else 0 for row, col in [(0, 1), (0, -1), (1, 0), (-1, 0)] ]) for i in range(len(maxs[0]))])
    if minDifference == 0: return 1
    # reciprocal of difference
    return 1/minDifference

def numEmpty(board:np.ndarray) -> float:
    return board[board==0].size

def highestTile(board:np.ndarray) -> float:
    return np.max(board)

def boardSum(board:np.ndarray) -> float:
    return np.sum(board)