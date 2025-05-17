
import numpy as np
from game.gameboard import filterTileIndices, getLegalMoves

'''Node classes used to represent game states'''

class BoardNode():

    count = 0

    def __init__(self, board:np.ndarray=np.zeros((4,4))):
        self.board:np.ndarray = board
        self.value:float = 0
        self.children:dict[callable:BoardNode] = dict()
        self.position:int = BoardNode.count
        BoardNode.count += 1

    def fillMoveChildren(self):
        ''' Fills self.children with move : Child pairs for each legal move of self.board '''
        if(len(self.children) != 0):
            self.children = dict()
        legalMoves = getLegalMoves(self.board)
        for move in legalMoves:
            self.children[move] = BoardNode(move(self.board.copy()))

    def fillTileChildren(self):
        ''' Fills self.children with ((x,y),tile) : Child pairs for each empty tile of self.board'''
        if(len(self.children) != 0):
            self.children = dict()
        newTilesX, newTilesY = filterTileIndices(np.argwhere(self.board == 0))
        #newTilesX, newTilesY = np.where(self.board == 0)
        for idx in range(len(newTilesX)):
            self.board[newTilesX[idx], newTilesY[idx]] = 2
            self.children[(newTilesX[idx], newTilesY[idx]),2] = BoardNode(self.board.copy())
            self.board[newTilesX[idx], newTilesY[idx]] = 4
            self.children[(newTilesX[idx], newTilesY[idx],4)] = BoardNode(self.board.copy())
            self.board[newTilesX[idx], newTilesY[idx]] = 0

    def getDepth(self):
        if(len(self.children) == 0):
            return 0
        return 1 + max([child.getDepth() for child in self.children.values()])

class MonteCarloNode(BoardNode):

    def __init__(self, board:np.ndarray=np.zeros((4,4))):
        super().__init__(board)
        self.numVisits:int = 0
        self.parent:BoardNode = None

    def fillMoveChildren(self):
        ''' Fills self.children with move : Child pairs for each legal move of self.board '''
        if(len(self.children) != 0):
            self.children = dict()
        legalMoves = getLegalMoves(self.board)
        for move in legalMoves:
            self.children[move] = MonteCarloNode(move(self.board.copy()))

    def calculateUCT(self, explorationConstant:float=np.sqrt(2)) -> float:
        if self.parent is None or self.numVisits == 0 or self.parent.numVisits == 0:
            return float('inf')
        return self.value/self.numVisits + explorationConstant*np.sqrt(np.log(self.parent.numVisits)/self.numVisits)
    