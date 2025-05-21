import time
from utils import rand
from boardevaluation.evaluationfunctions import snakeStrength, numEmpty
from agents.searchagents import Search
from game.gameboard import getLegalMoves, hashInt
import game.boardnodes as nodes
import numpy as np
'''
MCTS
    cost grows linearly with tree depth
    random rollouts take advantage of chance nodes
        no need to visit all chance nodes
'''
class MonteCarlo(Search):

    def __init__(self, maxDepth=float('inf'), moveTimeLimit=0.1):
        super().__init__(maxDepth, moveTimeLimit)

    def __str__(self):
        return 'Abstract Monte Carlo Search Agent'

    def getMove(self, board:np.ndarray) -> callable:
        if (hashedBoard:=hashInt(board)) in self.calculatedMoves.keys():
            return self.calculatedMoves[hashedBoard]
        root:nodes.MonteCarloNode = self.runSearch(nodes.MonteCarloNode(board))
        if(len(root.children) == 0):
            return None
        self.calculatedMoves[hashedBoard] = max(root.children, key=lambda move: root.children[move].value)
        return self.calculatedMoves[hashedBoard]

    def rollout(self, state:nodes.MonteCarloNode):
        '''simulates a random game starting from 'state' ending after rolloutLength turns and returns states score'''
        rolloutBoard = state.board
        depth = 0
        legalMoves = getLegalMoves(rolloutBoard)
        while len(legalMoves) > 0 and depth < self.maxDepth:
            rolloutBoard = legalMoves[rand.integers(0, len(legalMoves))](rolloutBoard)
            rolloutBoard[tuple(rand.choice(np.argwhere(rolloutBoard == 0)))] = rand.choice([2,4], p=[0.9,0.1])    
            legalMoves = getLegalMoves(rolloutBoard)
            depth += 1
        if self.maxDepth == float('inf'):
            return depth
        return self.evaluationFunction(rolloutBoard)

    
    def runSearch(self, root:nodes.MonteCarloNode):
        '''runs MC search from root'''
        root.fillMoveChildren()
        t0 = time.time()
        while time.time()-t0 < self.timeToMove:
            self.monteCarloSearch(root)
        return root
    
    def monteCarloSearch(self, root):
        pass


'''Monte Carlo Search agents'''

class PureMonteCarlo(MonteCarlo):

    def __init__(self, rolloutLength=float('inf'), maxNodeRollouts=float("inf"),  moveTimeLimit=0.03):
        super().__init__(rolloutLength, moveTimeLimit)
        self.maxNodeRollouts = maxNodeRollouts

    def __str__(self):
        return 'Pure Monte Carlo Search Agent'

    def monteCarloSearch(self, root:nodes.MonteCarloNode):
        child = min([child for child in root.children.values()], key=lambda child: child.numVisits)

        rolloutScore = self.rollout(child)
        
        child.value += rolloutScore
        child.numVisits += 1



class MCTSAgent(MonteCarlo):
    '''
    Monte Carlo Tree Search Agent

    Move stages:
        s0 = current state, root of tree
        traverse to a leaf node descendant s1 of s0 based on UCT bound
        expand s1 by adding its successor state(s) c() to tree
        perform rollouts from c(), keeping track of scores
        backpropagate scores from c() up to root s0
    '''

    def __init__(self, rolloutLength=float('inf'), explorationConstant=np.sqrt(2), moveTimeLimit=0.1):
        super().__init__(rolloutLength, moveTimeLimit)
        self.explorationConstant = explorationConstant

    def __str__(self):
        return 'Monte Carlo Tree Search Agent'
    
    def backPropagate(self, state, score:int):
        '''updates the value and numVisits fields of 'state' and all its ancestors'''
        while state is not None:
            state.value += score
            state.numVisits += 1
            state = state.parent

    def moveBoard(self, board, moveFunction):
        board = moveFunction(board)
        board[tuple(rand.choice(np.argwhere(board == 0)))] = rand.choice([2,4], p=[0.9,0.1])
        return board

    def incrementTree(self, root):
        legalMoves = getLegalMoves(root.board)
        if len(legalMoves) == 0:
            return None
        if len(legalMoves) == 1:
            root
        curNode = root
        while all([move in curNode.children.keys() for move in legalMoves]) and len(legalMoves) > 0:
            curNode = max([child for child in curNode.children.values()], key=lambda child: child.calculateUCT(self.explorationConstant))
            legalMoves = getLegalMoves(curNode.board)
        if len(legalMoves) == 0:
            return None
        unexploredMove = [move for move in legalMoves if move not in curNode.children.keys()][0]
        curNode.children[unexploredMove] = nodes.MonteCarloNode(nodes.MonteCarloNode(curNode.board))
        curNode.children[unexploredMove].parent = curNode
        return curNode.children[unexploredMove]
       
    def monteCarloSearch(self, root:nodes.MonteCarloNode):
        '''runs MCTS from root with its descendants'''
        # add a node to tree representing unexplored state
        # perform a random simulation from the new node
        # backpropagate the results up to the root's children
        newChildNode = self.incrementTree(root)
        if newChildNode is None or newChildNode is root:
            
            return None
        rolloutScore = self.rollout(newChildNode)
        self.backPropagate(newChildNode, rolloutScore)
    
    def __str__(self):
        return 'Monte Carlo Tree Search Agent'