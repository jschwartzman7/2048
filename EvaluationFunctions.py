import Search
import math
import copy

tileWeights = {
        (0, 0) : 0,
        (0, 1) : .1,
        (0, 2) : .4,
        (0, 3) : .7,
        (1, 0) : .1,
        (1, 1) : .4,
        (1, 2) : .7,
        (1, 3) : 1,
        (2, 0) : .4,
        (2, 1) : .7,
        (2, 2) : 1,
        (2, 3) : 2,
        (3, 0) : .7,
        (3, 1) : 1,
        (3, 2) : 2,
        (3, 3) : 4.8,

    }

tileWeights2 = {
        (0, 0) : 1.75,
        (0, 1) : 1,
        (0, 2) : 1,
        (0, 3) : 1.75,
        (1, 0) : 1,
        (1, 1) : .25,
        (1, 2) : .25,
        (1, 3) : 1,
        (2, 0) : 1,
        (2, 1) : .25,
        (2, 2) : .25,
        (2, 3) : 1,
        (3, 0) : 1.75,
        (3, 1) : 1,
        (3, 2) : 1,
        (3, 3) : 1.75,

    }

def getMergeInfo(board):
    legalMoves = Search.getLegalMoves(board)
    sumNumMerges = 0
    sumMergeValues = 0
    for move in legalMoves:
        newBoard =  move[0](copy.deepcopy(board))
        sumNumMerges += len(newBoard[1].values())
        sumMergeValues += sum(newBoard[1].values())
    return sumNumMerges, sumMergeValues

def getTileInfo(board):
    sum = 0
    #maxTile = 0
    numEmpty = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] == ' ':
                numEmpty += 1
            else:
                sum += board[i][j]
                #if board[i][j] > maxTile:
                    #maxTile = board[i][j]
    return sum, numEmpty

def calculateCenter(board, tileSum):
    xCord = 0
    yCord = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != ' ':
                xCord += (board[i][j]/tileSum)*i
                yCord += (board[i][j]/tileSum)*j
    return (xCord, yCord)
            
def calculateSD(board, center, sum):
    variance = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != ' ':
                variance += math.pow(math.dist(center, (i, j)), 2)*(board[i][j]/sum)
    return math.sqrt(variance)

def evaluate(board, mergeValues, weights):
    '''
    Evaluation function: 4x4 matrix -> num >= 0
    Board with no legal moves has eval(board) = 0
    Way of measuring "distance" to a game over (full board)
    '''
    sum, numEmpty = getTileInfo(board)
    center = calculateCenter(board, sum)
    distanceToCenter = math.dist((center[0], center[1]), (1.5, 1.5))
    sd = calculateSD(board, center, sum)

    features = [(numEmpty, lambda x: 3*math.sqrt(x), 'numEmpty'),
                (mergeValues, lambda x: math.log2(x), 'merges'),
                (distanceToCenter, lambda x: 5*x, 'distanceToCenter'),
                (sd, lambda x: -5*x, 'sd')]
    
    #weights = [1 for i in range(len(features))]
    
    evaluation = 0
    for i, feature in enumerate(features):
        if feature[0] != mergeValues or mergeValues != 0:
            evaluation += weights[i]*feature[1](feature[0])
        
            
    #print()
    #print("distance to center: ", w[i]*distanceToCenter)
    #return -1*stats['sum'] + .6*stats['maxTile'] + 1.5*stats['numEmpty'] + 1*mergeInfo['numMerges'] + 0*mergeInfo['mergeValues'] + 2*merges
    return evaluation
    return w['sum']*stats['sum'] + w['maxTile']*stats['maxTile'] + w['numEmpty']*stats['numEmpty'] + w['numMerges']*mergeInfo['numMerges'] + w[4]*mergeInfo['mergeValues'] + w[5]*mergeValues + w[6]*distanceToCenter
    





def getValue2(board):
    x = 1
    y = .5
    boardScore = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != ' ':
                for entry in [((1, 0), x), ((-1, 0), x), ((0, 1), x), ((0, -1), x), ((1, 1), y), ((1, -1), y), ((-1, 1), y), ((-1, -1), y)]:
                    if (i + entry[0][0], j + entry[0][1]) in tileWeights.keys() and board[i+entry[0][0]][j+entry[0][1]] != ' ':
                        boardScore += math.log2(board[i][j])*math.log2(board[i+entry[0][0]][j+entry[0][1]])*entry[1]
    return boardScore





def getValue(board):
    #print("getting value")
    #Heuristic that determines how "compact" a board is
    #Higher score for:
    #   larger tiles close to a corner
    #   larger tiles near other larger tiles for potential merging
    #   largest tile at a corner
    largestTile = (0, 0)
    curMax = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != ' ':
                if board[i][j] > curMax:
                    curMax = board[i][j]
                    largestTile = (i, j)
    visited = set()
    queue = [(largestTile, tileWeights2[largestTile])]
    score = 0
    factor = 0
    while len(visited) < 16:
        curTile = queue[0]
        queue.remove(curTile)
        visited.add(curTile[0])
        #score += curTile[1]*board[curTile[0][0]][curTile[0][1]]
        if board[curTile[0][0]][curTile[0][1]] != ' ':
            score += curTile[1]*board[curTile[0][0]][curTile[0][1]]
            factor = math.log2(int(board[curTile[0][0]][curTile[0][1]]))
        for cord in [(curTile[0][0]+1, curTile[0][1]), (curTile[0][0]-1, curTile[0][1]), (curTile[0][0], curTile[0][1]+1), (curTile[0][0], curTile[0][1]-1)]:
            if cord in tileWeights.keys() and cord not in visited:
                queue.append((cord, factor))
    #print("returning score: ", score)
    return score