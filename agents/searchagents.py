from boardevaluation.evaluationfunctions import snakeStrength
from boardevaluation.boardevaluator import BoardEvaluator
from boardevaluation.evaluationfunctionutils import MAX
from utils import np, rand
from agents.basicagents import Agent
from game.gameboard import filterTileIndices, hashInt, getLegalMoves
import game.boardnodes as nodes
import time

'''
Expecti/Mini Max (ab pruning)
    cost grows exponentially with tree depth
    cannot visit all chance nodes up to depth in time
    must filter tile indices to reduce branching factor
'''
'''Search Agent base classes defining shared methods'''

class Reflex(Agent):

    def __init__(self, boardEvaluator:BoardEvaluator=None):
        super().__init__()
        
        # evaluator to evaluate boards
        self.boardEvaluator:BoardEvaluator = BoardEvaluator()

        # boards encountered in other moves to avoid re-searching
        self.calculatedMoves:dict[np.ndarray:callable] = dict()

        # boards encountered in evaluation to avoid re-evaluating
        self.hashedBoardEvaluations:dict[np.ndarray:float] = dict()

    def getMove(self, board:np.ndarray) -> callable:
        if (hashedBoard:=hashInt(board)) in self.calculatedMoves.keys():
            return self.calculatedMoves[hashedBoard]
        root:nodes.BoardNode = nodes.BoardNode(board)
        root.fillMoveChildren()
        for move in root.children.keys():
            if (hashedChildBoard:=hashInt(move(root.board))) in self.hashedBoardEvaluations.keys():
                root.children[move].value = self.hashedBoardEvaluations[hashedChildBoard]
            else:
                root.children[move].value = self.boardEvaluator.evaluate(move(root.board)) 
        self.calculatedMoves[hashedBoard] = max(root.children, key=lambda move: root.children[move].value)
        return self.calculatedMoves[hashedBoard]

class Search(Reflex):

    def __init__(self, maxDepth:int=3, moveTimeLimit:float=0.1):
        super().__init__()
        
        # max search depth / rollout length
        self.maxDepth:int = maxDepth

        # time limit for each move
        self.timeToMove:float = moveTimeLimit

    def __str__(self):
        return 'Abstract Search Agent'
    
    # checks if board has been encountered before, if not maximizes over legal moves and returns move
    def getMove(self, board:np.ndarray) -> callable:
        if (hashedBoard:=hashInt(board)) in self.calculatedMoves.keys():
            return self.calculatedMoves[hashedBoard]
        root:nodes.BoardNode = self.runSearch(nodes.BoardNode(board))
        if(len(root.children) == 0):
            return None
        self.calculatedMoves[hashedBoard] = max(root.children, key=lambda move: root.children[move].value)
        return self.calculatedMoves[hashedBoard]
    
    def iterativeDeepeningSearch(self, boardnode:nodes.BoardNode) -> float:
        defaultMaxDepth = self.maxDepth
        self.maxDepth = 1
        t0 = time.time()
        while time.time()-t0 < self.timeToMove and self.maxDepth <= defaultMaxDepth:
            root = nodes.BoardNode(boardnode.board)
            self.search(root, 0)
            self.maxDepth += 1
        self.maxDepth = defaultMaxDepth
        return root
    
    def preSearch(self, board:nodes.BoardNode, curDepth:int) -> float:
        '''call this at beginning of child().search'''
        if curDepth > self.maxDepth:
            if (hashedBoard := hashInt(board.board)) not in self.hashedBoardEvaluations:
                self.hashedBoardEvaluations[hashedBoard] = self.boardEvaluator.evaluate(board.board)
            return self.hashedBoardEvaluations[hashedBoard]
        else:
            return None
        
    
    # returns the value of the board after running the search algorithm iterative deepening
    def runSearch(self, boardnode:nodes.BoardNode) -> float:
        pass

    def search(self, board:nodes.BoardNode, curDepth:int) -> float:
        pass


        
'''Expectimax and Minimax agents'''

class Expectimax(Search):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'Expectimax Search with ' + self.boardEvaluator.__str__()
    
    def runSearch(self, boardnode):
        return self.iterativeDeepeningSearch(boardnode)

    def search(self, board: nodes.BoardNode, curDepth: int) -> float:
        if (boardValue:=self.preSearch(board, curDepth)) is not None:
            return boardValue
        if(curDepth % 2 == 0): # max player
            board.fillMoveChildren()
            if len(board.children) == 0:
                return 0
            for child in board.children.values():
                child.value = self.search(child, curDepth + 1)    
            return max(board.children.values(), key=lambda child: child.value).value
        else: # chance player
            board.fillTileChildren()
            if len(board.children) == 0:
                return 0
            boardExpectedValue = 0
            for tile, child in board.children.items():
                if tile[1] == 2:
                    child.value = self.search(child, curDepth + 1)   
                    boardExpectedValue += 0.9 * child.value
                else:
                    child.value = self.search(child, curDepth + 1)   
                    boardExpectedValue += 0.1 * child.value
            return 2*boardExpectedValue / len(board.children) 
        
class ExpectimaxAlpha(Search):

    def __init__(self, maxDepth=3, moveTimeLimit=0.1):
        super().__init__(maxDepth, moveTimeLimit)

    def __str__(self):
        return 'Expectimax Alpha Pruning Search with ', self.boardEvaluator.__str__
    
    def runSearch(self, boardnode):
        return self.iterativeDeepeningSearch(boardnode)

    def search(self, board:nodes.BoardNode, curDepth: int, alpha:float=float("-inf")):
        if (boardValue:=super().preSearch(board, curDepth)) is not None:
            return boardValue
        if(curDepth % 2 == 0): # max player
            board.fillMoveChildren()
            if len(board.children) == 0:
                return 0
            for child in board.children.values():
                child.value = self.search(child, curDepth + 1, alpha)
                alpha = max(alpha, child.value)    
            return max(board.children.values(), key=lambda child: child.value).value
        else: # chance player
            board.fillTileChildren()
            if len(board.children) == 0:
                return 0
            boardExpectedValue = 0
            for i, item in enumerate(board.children.items()):
                if boardExpectedValue + MAX*(len(board.children) - i)/len(board.children) < alpha:
                    return alpha
                if item[0][1] == 2:
                    item[1].value = self.search(item[1], curDepth + 1)   
                    boardExpectedValue += 0.9 * item[1].value
                else:
                    item[1].value = self.search(item[1], curDepth + 1)   
                    boardExpectedValue += 0.1 * item[1].value
            return 2*boardExpectedValue / len(board.children)

class MinimaxAlphaBeta(Search):

    def __init__(self, maxDepth=2, moveTimeLimit=0.1):
        super().__init__(maxDepth, moveTimeLimit)
        
    def __str__(self):
        return 'Minimax Alpha Beta Pruning Search with ', self.boardEvaluator.__str__
    
    def runSearch(self, boardnode):
        return self.iterativeDeepeningSearch(boardnode)
    
    def search(self, board:nodes.BoardNode, curDepth:int, alpha:float=float('-inf'), beta:float=float('inf')):
        if (boardValue:=super().preSearch(board, curDepth)) is not None:
            return boardValue
        if(curDepth % 2 == 0): # max player
            board.fillMoveChildren()
            if len(board.children) == 0:
                return 0
            for child in board.children.values():
                child.value = self.search(child, curDepth + 1, alpha, beta)
                alpha = max(alpha, child.value)    
            return max(board.children.values(), key=lambda child: child.value).value
        else: # min player
            board.fillMoveChildren()
            if len(board.children) == 0:
                return 0
            for child in board.children.values():
                child.value = self.search(child, curDepth + 1, alpha, beta)
                beta = min(beta, child.value)    
            return min(board.children.values(), key=lambda child: child.value).value

'''Agent that uses other agents' strategies based on current number of tiles present'''

    

    


   
   