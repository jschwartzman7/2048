import pygame as pg
import numpy as np
from game.gameboard import randomStartingBoard, randomTestBoardWeighted, generatePiece, getLegalMoves, stringToMove
import agents.basicagents as basicagents
import agents.searchagents as sa
import game.boardnodes as nodes
from utils import colors, rand
import utils
import boardevaluation.evaluationfunctions as ef
from pyGame.surfaces import Board, Menu


class Display:
    '''object for pygame display uses'''

    displayWidth = 600
    displayHeight = 600
    fontSize = 40
    backgroundColor = colors['BACKGROUND_COLOR']

    def __init__(self):
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode((Display.displayWidth, Display.displayHeight))
        self.clock = pg.time.Clock()
        self.font:pg.font = self.myFont(Display.fontSize)

    def myFont(self, size:int=fontSize) -> pg.font.Font:
        return pg.font.SysFont(None, size)
    
    def renderFont(self, font:pg.font.Font, text:str, color:tuple) -> pg.Surface:
        return font.render(text, True, color)

    def updateDisplay(self):
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
        self.clock.tick(10)
        self.screen.fill(Display.backgroundColor)
    
class Modes(Display):

    def __init__(self, agents:list[basicagents.Agent]):
        super().__init__()
        self.agents = agents
        self.menuList = ["User Play 2048"]+agents
        self.gameboard = randomStartingBoard()
        self.currentMode = 0
        self.movesFile = open("datacollection/moves.txt", "w")

    def updateDisplay(self):
        Board(0.5*Display.displayWidth, 0.5*Display.displayHeight).blitSurface(self.screen, self.gameboard)
        self.menuList[self.currentMode] = "-> " + str(self.menuList[self.currentMode])
        Menu(0.5*Display.displayWidth, 0.6*Display.displayHeight).blitSurface(self.screen, self.menuList)
        self.menuList[self.currentMode] = self.menuList[self.currentMode][3:]
        if self.currentMode > 0 and self.currentMode < len(self.agents)+1: # agent move
            move = self.agents[self.currentMode-1].getMove(self.gameboard)
            if move is not None:
                self.gameboard = move(self.gameboard)
                generatePiece(self.gameboard)
            else:
                self.gameboard = randomStartingBoard()
        for event in pg.event.get():
            if self.currentMode == 0:
                move = None
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT and stringToMove['left']['can'](self.gameboard):
                        move = stringToMove['left']['move']
                    if event.key == pg.K_RIGHT and stringToMove['right']['can'](self.gameboard):
                        move = stringToMove['right']['move']
                    if event.key == pg.K_UP and stringToMove['up']['can'](self.gameboard):
                        move = stringToMove['up']['move']
                    if event.key == pg.K_DOWN and stringToMove['down']['can'](self.gameboard):
                        move = stringToMove['down']['move']
                if move is not None:
                    currentMove = move.__name__
                    for vale in self.gameboard.flatten():
                        self.movesFile.write(f"{int(vale)} ")
                    self.movesFile.write(f"{currentMove}\n")
                    self.gameboard = move(self.gameboard)
                    generatePiece(self.gameboard)   
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    self.currentMode = 0
                if event.key == pg.K_2:
                    if len(self.agents) > 0:
                        self.currentMode = 1
                if event.key == pg.K_3:
                    if len(self.agents) > 1:
                        self.currentMode = 2
                if event.key == pg.K_4:
                    if len(self.agents) > 2:
                        self.currentMode = 3
                if event.key == pg.K_5:
                    if len(self.agents) > 3:
                        self.currentMode = 4
                if event.key == pg.K_6:
                    if len(self.agents) > 4:
                        self.currentMode = 5
                if event.key == pg.K_7:
                    if len(self.agents) > 5:
                        self.currentMode = 6
                if event.key == pg.K_8:
                    if len(self.agents) > 6:
                        self.currentMode = 7
                if event.key == pg.K_9:
                    if len(self.agents) > 7:
                        self.currentMode = 8
            

    def run(self):
        self.running = True
        self.gameboard = randomStartingBoard()
        while self.running:
            self.updateDisplay()
            super().updateDisplay()

class UserPlay2048(Display):

    def __init__(self):
        self.boardSurface = Board(0.8*Display.displayWidth, 0.8*Display.displayHeight)
        self.running = True

    def run(self):
        running = True
        self.gameboard = randomStartingBoard()
        while running:
            self.updateDisplay()
            super().updateDisplay()


    def updateDisplay(self):
        self.boardSurface = self.boardSurface.blitSurface((self.gameboard))
        self.screen.blit(self.boardSurface, (0, 0))
        move = None
        for event in pg.event.get():
            if event.type == pg.QUIT or len(getLegalMoves(gameBoard)) == 0:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT and stringToMove['left']['can'](gameBoard):
                    move = stringToMove['left']['move']
                if event.key == pg.K_RIGHT and stringToMove['right']['can'](gameBoard):
                    move = stringToMove['right']['move']
                if event.key == pg.K_UP and stringToMove['up']['can'](gameBoard):
                    move = stringToMove['up']['move']
                if event.key == pg.K_DOWN and stringToMove['down']['can'](gameBoard):
                    move = stringToMove['down']['move']
        if move is not None:
            gameBoard = move(gameBoard)
            generatePiece(gameBoard)

class EvaluationAnalysis(Display):

    def __init__(self):
        super().__init__()
        self.evaluationFuntions = [ef.snakeStrength, ef.cornerStrength, ef.tileCompactness, ef.surrounded, ef.highestPiece]
        self.boardSurface = Board(0.5*Display.displayWidth, 0.5*Display.displayHeight)
        self.gameboard = randomStartingBoard()
        self.font:pg.font = self.myFont(25)
    
    def renderEvaluationStatistics(self, gameBoard):
        for i, eval in enumerate(self.evaluationFuntions):
            functionNameText = self.font.render(eval.__name__, True, (0,0,0))
            self.screen.blit(functionNameText, (self.screen.get_width()*.5, 2*self.font.get_height()*i))
            evaluationFunctionText = self.font.render(str(round(eval(gameBoard), 3)), True, (0,0,0))
            self.screen.blit(evaluationFunctionText, (self.screen.get_width()*.5, 2*self.font.get_height()*i+self.font.get_height()))
        
    def runEvaluationAnalysis(self):
        '''start with an empty board and toggle 2 tile when user clicks a tile'''
        #gameBoard = np.zeros((4,4))
        gameBoard = self.gameboard
        running = True
        curTileSelected = 2
        curIndexSelected = (0, 0)
        while running:
            self.screen.blit(self.boardSurface.blitSurface(gameBoard), (0, 0))
            selectedTileText = self.myFont(50).render(str(curTileSelected), True, (0,0,0))
            self.screen.blit(selectedTileText, (self.screen.get_width()*4/5, self.screen.get_height()-50))
            selectedIndexText = self.myFont(50).render(str(curIndexSelected), True, (0,0,0))
            self.screen.blit(selectedIndexText, (self.screen.get_width()*4/5, self.screen.get_height()-100))
            self.renderEvaluationStatistics(gameBoard)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        gameBoard[curIndexSelected] = curTileSelected
                        self.screen.blit(self.boardSurface.blitSurface(gameBoard), (0, 0))
                    if event.key == pg.K_r:
                        gameBoard = randomTestBoardWeighted(numFilled=rand.integers(5, 14))
                    if event.key == pg.K_c:
                        gameBoard = np.zeros((4,4))
                    if event.key == pg.K_a and stringToMove['left']['can'](gameBoard):
                        gameBoard = stringToMove['left']['move'](gameBoard)
                    if event.key == pg.K_d and stringToMove['right']['can'](gameBoard):
                        gameBoard = stringToMove['right']['move'](gameBoard)
                    if event.key == pg.K_w and stringToMove['up']['can'](gameBoard):
                        gameBoard = stringToMove['up']['move'](gameBoard)
                    if event.key == pg.K_s and stringToMove['down']['can'](gameBoard):
                        gameBoard = stringToMove['down']['move'](gameBoard)
                    if event.key == pg.K_UP:
                        if curTileSelected != max(colors['TILE_VALUE_COLORS'].keys()):
                            curTileSelected *= 2
                        else:
                            curTileSelected = 2
                    if event.key == pg.K_DOWN:
                        if curTileSelected != 2:
                            curTileSelected /= 2
                        else:
                            curTileSelected = max(colors['TILE_VALUE_COLORS'].keys())
                    if event.key == pg.K_LEFT:
                        if curIndexSelected[1] > 0:
                            curIndexSelected = (curIndexSelected[0], curIndexSelected[1]-1)
                        else:
                            curIndexSelected = ((curIndexSelected[0]-1)%4, 3)
                    if event.key == pg.K_RIGHT:
                        if curIndexSelected[1] < 3:
                            curIndexSelected = (curIndexSelected[0], curIndexSelected[1]+1)
                        else:
                            curIndexSelected = ((curIndexSelected[0]+1)%4, 0)

            super().updateDisplay()

class GameTree(Display):

    '''draws the tree representing a BoardNode and its child subtrees'''

    def __init__(self, evaluationFunction=ef.snakeStrength):
        super().__init__()
        self.evaluationFunction = evaluationFunction
        self.BRANCH_TO_BOARD_HEIGHT_RATIO = 0.5

    def drawTreeRecursive(self, root:nodes.BoardNode, surface:pg.Surface):
        # fill the current surface with board info
        curDepth = root.getDepth()
        surface.fill(colors['BACKGROUND_COLOR'])
        #pg.draw.rect(surface, (0,0,0), (0, 0, surface.get_width(), surface.get_height()), 1)
        boardLength = min(max(surface.get_width(), 50), surface.get_height()/(curDepth+1))
        boardSurface = pg.Surface((boardLength, boardLength))
        #boardEvaluation = self.font.render(str(round(self.evaluationFunction(root.board), 3)), True, (0,0,0))
        #surface.blit(boardEvaluation, (x-boardLength*.5, boardLength))
        Board(boardLength, boardLength).blitSurface(boardSurface, root.board)
        surface.blit(boardSurface, (surface.get_width()/2-boardLength/2, 0))
        
        # recurse drawing board info for each child surface
        if len(root.children) == 0:
            return surface
        partitionHorizontal = surface.get_width()/min(len(root.children), 4)
        for i, key in enumerate(root.children):
            if i >= 4:
                break
            #if self.evaluationFunction(root.children[move].board) == max([self.evaluationFunction(root.children[move].board) for move in root.children]):
            pg.draw.line(surface, (0, 0, 255), (surface.get_width()/2, boardLength), ((i+0.5)*partitionHorizontal, (1+self.BRANCH_TO_BOARD_HEIGHT_RATIO)*boardLength), 3)
            #moveName = self.myFont(15).render(str(move), True, (0,0,0))
            #surface.blit(moveName, ((i+0.5)*partitionHorizontal, (self.BRANCH_TO_BOARD_HEIGHT_RATIO)*boardLength-self.font.get_height()))
            surface.blit(self.drawTreeRecursive(root.children[key], pg.Surface((partitionHorizontal, int(surface.get_height()-(boardLength)*(1+self.BRANCH_TO_BOARD_HEIGHT_RATIO))))), (i*partitionHorizontal, (boardLength)*(1+self.BRANCH_TO_BOARD_HEIGHT_RATIO)))
        return surface
        
    def runGameTree(self, root:nodes.BoardNode):
        self.running = True
        while self.running:
            self.screen.blit(self.drawTreeRecursive(root, pg.Surface((self.screen.get_width(), self.screen.get_height()))), (0,0))
            super().updateDisplay()
        

if __name__ == "__main__":
    EvaluationAnalysis().runEvaluationAnalysis()


    