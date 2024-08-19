import pygame as pg
from Bot2048.gameBoard import randomStartingBoard, randomTestBoardWeighted, randomPositions, generatePiece
from Bot2048.searchAgents import getLegalMoves, moveInDirection, canMoveInDirection, ExpectimaxAlpha, MCTSAgent
from Bot2048.evaluationFunctions import snakeStrength, cornerStrength, cornerSnakeStrength, highestPiece
import numpy as np
from Bot2048.constants import rand, tileValueColors

class GameDisplay:
    '''object for 2048 display uses'''

    def __init__(self, displayWidth:int=800, displayHeight:int=800, boardWidth:int=0, boardHeight:int=0, tileFontSize:int=12, font2Size:int=100):
        pg.init()
        self.width = displayWidth
        self.height = displayHeight
        self.screen = pg.display.set_mode((displayWidth, displayHeight))
        self.clock = pg.time.Clock()
        self.boardSurface = pg.Surface((boardWidth, boardWidth))
        self.tileSurface = pg.Surface((int(0.23*boardWidth), int(0.23*boardHeight)))
        self.backgroundColor = (250, 248, 239)
        self.boardColor = (187, 173, 161)
        self.tileEmptyColor = (205, 193, 181)
        pg.font.init()
        self.tileFont = pg.font.SysFont(None, size=tileFontSize)
        self.tileTextColorLow = (119,110,101)
        self.tileTextColorHigh = (250,246,243)
        self.font2 = pg.font.SysFont(None, size=font2Size)


    def updateBoardSurface(self, board:np.ndarray, boardWidth:int, boardHeight:int):
        self.boardSurface = pg.Surface((boardWidth, boardHeight))
        self.tileSurface = pg.Surface((int(0.23*boardWidth), int(0.23*boardHeight)))
        self.boardSurface.fill(self.boardColor)
        between_tile_width = (self.boardSurface.get_width() - self.tileSurface.get_width()*4)/5
        between_tile_height = (self.boardSurface.get_height() - self.tileSurface.get_height()*4)/5
        for i in range(4):
            for j in range(4):
                if board[i, j] == 0:
                    self.tileSurface.fill(self.tileEmptyColor)
                else:
                    if board[i, j] < 8:
                        text_surface = self.tileFont.render(str(board[i, j]), True, self.tileTextColorLow)
                    else:
                        text_surface = self.tileFont.render(str(board[i, j]), True, self.tileTextColorHigh)
                    self.tileSurface.fill(tileValueColors[board[i, j]])
                    self.tileSurface.blit(text_surface, (self.tileSurface.get_width()/3, self.tileSurface.get_height()/3))
                self.boardSurface.blit(self.tileSurface, ((j+1)*between_tile_width+j*(self.tileSurface.get_width()), (i+1)*between_tile_height+i*(self.tileSurface.get_height())))
        return self.boardSurface
    
class BoardEvaluationAnalysis():


    display = GameDisplay(800, 800, 500, 500, tileFontSize=30)

    evaluationFuntions = [snakeStrength, cornerStrength, cornerSnakeStrength, highestPiece]

    def handleMouseClick(self, mouseClickedPos, board, curTileSelected):
        between_tile_width = (self.display.boardSurface.get_width() - self.display.tileSurface.get_width()*4)/5
        between_tile_height = (self.display.boardSurface.get_height() - self.display.tileSurface.get_height()*4)/5
        for i in range(4):
            for j in range(4):
                if self.display.tileSurface.get_rect(topleft=((j+1)*between_tile_width+j*(self.display.tileSurface.get_width()), (i+1)*between_tile_height+i*(self.display.tileSurface.get_height()))).collidepoint(mouseClickedPos):
                    if board[i, j] == curTileSelected:
                        board[i, j] = 0
                    else:
                        board[i, j] = curTileSelected
        return board

    def userTestGameboardValues(self):
        gameBoard = np.zeros((4,4))
        running = True
        curTileSelected = 2
        mouseClicked = [-1,-1]
        while running:
            self.display.screen.fill(self.display.backgroundColor)
            if mouseClicked != [-1,-1]:
                gameBoard = self.handleMouseClick(mouseClicked, gameBoard, curTileSelected)
            self.display.updateBoardSurface(gameBoard, self.display.boardSurface.get_width(), self.display.boardSurface.get_height())
            mouseClicked = [-1,-1]
            self.display.screen.blit(self.display.boardSurface, (0, 0))
            selectedTileText = self.display.tileFont.render(str(curTileSelected), True, (0,0,0))
            self.display.screen.blit(selectedTileText, (self.display.boardSurface.get_width(), 0))
            
            gameBoard = np.array(gameBoard)
            
            for i, eval in enumerate(self.evaluationFuntions):
                
                boardValue = eval(np.log2(gameBoard, where=gameBoard>0))
                functionNameTest = self.display.tileFont.render(eval.__name__, True, (0,0,0))
                evaluationFunctionText = self.display.tileFont.render(str(boardValue), True, (0,0,0))
                self.display.screen.blit(functionNameTest, (self.display.boardSurface.get_width(), self.display.tileSurface.get_height()*(i+1)*1.05))
                self.display.screen.blit(evaluationFunctionText, (self.display.boardSurface.get_width()+self.display.tileSurface.get_width(), self.display.tileSurface.get_height()*(i+1)))
                
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        gameBoard = randomTestBoardWeighted(numFilled=rand.integers(5, 14))
                    if event.key == pg.K_0:
                        curTileSelected = 0
                    if event.key == pg.K_1:
                        curTileSelected = 2
                    if event.key == pg.K_2:
                        curTileSelected = 4
                    if event.key == pg.K_3:
                        curTileSelected = 8
                    if event.key == pg.K_4:
                        curTileSelected = 16
                    if event.key == pg.K_5:
                        curTileSelected = 32
                    if event.key == pg.K_6:
                        curTileSelected = 64
                    if event.key == pg.K_7:
                        curTileSelected = 128
                    if event.key == pg.K_8:
                        curTileSelected = 256
                    if event.key == pg.K_9:
                        curTileSelected = 512
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouseClicked = pg.mouse.get_pos()

            
            pg.display.update()
            pg.display.flip()
            self.display.clock.tick(30)

class GameTree():

    display = GameDisplay(800, 800, tileFontSize=10)

    agent = MCTSAgent(moveTimeLimit=1)

    def displaySearchTree(self, board:np.ndarray):
        print(board)
        legalMoves = getLegalMoves(board)
        if len(legalMoves) == 0:
            print("No legal moves")
            return 
        self.agent.getMove(board, legalMoves)
        self.runGameTree(self.agent.searchTreeRoots[0])

    def drawTree(self, root, depth, surface:pg.Surface, maxDepth:int):
        backgroundColor = (self.display.backgroundColor[0]*(depth/maxDepth), self.display.backgroundColor[1]*(depth/maxDepth), self.display.backgroundColor[2]*(depth/maxDepth))
        surface.fill(backgroundColor)
        #surface.fill(self.display.backgroundColor)
        #surface.fill((backgroundColor[0]*(1-1/(depth+1)), backgroundColor[1]*(1-1/(depth+1)), backgroundColor[2]*(1-1/(depth+1))))
        y = 0
        x = surface.get_width()/2
        self.display.updateBoardSurface(root.board, surface.get_width()/(depth+2), surface.get_height()/(depth+2))
        surface.blit(self.display.boardSurface, (x-self.display.boardSurface.get_width()/2,y))
        #pg.draw.circle(surface, (0,0,255), (x, y), 3)
        if all([child == None for child in root.children.values()]):
            return surface
        partitionHorizontal = surface.get_width()/len(root.children)
        verticalDrop = surface.get_height()/(depth+1)
        children = [(move, child) for move, child in root.children.items() if child != None]
        for i, child in enumerate(children):
            pg.draw.line(surface, (255-backgroundColor[0], 255-backgroundColor[1], 255-backgroundColor[2]), (x, y), ((i+0.5)*partitionHorizontal, verticalDrop), 2)
            moveString = self.display.tileFont.render(child[0].__name__, True, (0,0,0))
            surface.blit(moveString, ((i+0.5)*partitionHorizontal, verticalDrop*(3/4)))
            surface.blit(self.drawTree(child[1], child[1].getDepth(), pg.Surface((partitionHorizontal, surface.get_height()-verticalDrop)), maxDepth), (i*partitionHorizontal, verticalDrop))
        return surface
        
    def runGameTree(self, root):
        self.display.screen.fill(self.display.backgroundColor)
        pg.display.update()
        pg.display.flip()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            self.display.screen.fill(self.display.backgroundColor)
            #treeSurface.blit(self.drawTree(root, self.getDepth(root), pg.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))), (0,0))
            self.display.screen.blit(self.drawTree(root, root.getDepth(), pg.Surface((0.9*self.display.width, 0.9*self.display.height)), root.getDepth()), (0.05*self.display.width,0.05*self.display.height))
            pg.display.update()
            pg.display.flip()
            self.display.clock.tick(30)
        
        

class UserPlayGameboard(GameDisplay):

    display = GameDisplay(800, 800, 700, 700)

    def highlightNewTile(self, board:np.ndarray, newTileIdx:list) -> None:
        space_width = (self.display.boardSurface.get_width() - self.display.tileSurface.get_width()*4)/5
        space_height = (self.display.boardSurface.get_height() - self.display.tileSurface.get_height()*4)/5
        for i in range(4):
            for j in range(4):
                if newTileIdx[0] == i and newTileIdx[1] == j:
                    pg.draw.rect(self.display.tileSurface, (255, 0, 0), (0, 0, self.display.tileSurface.get_width(), self.display.tileSurface.get_height()), 5)
                    self.display.boardSurface.blit(self.display.tileSurface, ((j+1)*space_width+j*(self.display.tileSurface.get_width()), (i+1)*space_height+i*(self.display.tileSurface.get_height())))
                    return


    def userPlayGameboardVisuals(self):
        gameBoard = randomStartingBoard()
        running = True
        newTileX = -1
        newTileY = -1
        while len(getLegalMoves(gameBoard)) > 0 and running:
            self.display.screen.fill(self.display.backgroundColor)
            self.display.updateBoardSurface(gameBoard, self.display.boardSurface.get_width(), self.display.boardSurface.get_height())

            self.highlightNewTile(gameBoard, [newTileX, newTileY])
            
            self.display.screen.blit(self.display.boardSurface, (0, 0))
            moveDirection = None
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT and canMoveInDirection('left', gameBoard):
                        moveDirection = 'left'
                    if event.key == pg.K_RIGHT and canMoveInDirection('right', gameBoard):
                        moveDirection = 'right'
                    if event.key == pg.K_UP and canMoveInDirection('up', gameBoard):
                        moveDirection = 'up'
                    if event.key == pg.K_DOWN and canMoveInDirection('down', gameBoard):
                        moveDirection = 'down'
            if moveDirection != None:
                gameBoard = moveInDirection(moveDirection)(gameBoard)
                gameBoard, newTileX, newTileY = self.generatePieceNewTileIdx(gameBoard)
            
            pg.display.update()
            pg.display.flip()
            self.display.clock.tick(30)
            
        while running:
            self.display.screen.fill(self.display.backgroundColor)
            self.highlightNewTile(gameBoard, [newTileX, newTileY])
            gameOverText = self.display.font2.render('Game Over', True, (0, 0, 0))
            self.display.boardSurface.blit(gameOverText, (0,0))
            self.display.screen.blit(self.display.boardSurface, (0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            pg.display.update()
            pg.display.flip()
            self.display.clock.tick(30)

    def generatePieceNewTileIdx(self, board:np.ndarray) -> np.ndarray:
        emptyCords = np.argwhere(board == 0)
        if emptyCords.size > 0:
            newIdx = rand.choice(emptyCords)
            newX, newY = newIdx
            board[newX, newY] = rand.choice([2,4], p=[0.9,0.1])
        return board, newX, newY

class AgentSimulationAnalysis:

    display = GameDisplay(800, 800, 800, 800)

    def simulateGame(self, agent):
        gameBoard = randomStartingBoard()
        legalMoves = getLegalMoves(gameBoard)
        running = True
        while len(legalMoves) > 0 and running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            self.display.screen.fill((50,50,50))
            self.display.updateBoardSurface(gameBoard, self.display.boardSurface.get_width(), self.display.boardSurface.get_height())
            self.display.screen.blit(self.display.boardSurface, (0, 0))
            moveDirection = agent.getMove(gameBoard, legalMoves)
            moveText = self.display.tileFont.render(moveDirection.__name__, True, self.display.tileTextColorHigh)
            self.display.screen.blit(moveText, (self.display.boardSurface.get_width()/2, self.display.boardSurface.get_width()*.7))
            gameBoard = moveDirection(gameBoard)
            
            gameBoard = generatePiece(gameBoard)
            legalMoves = getLegalMoves(gameBoard)
            pg.display.update()
            pg.display.flip()
        print("max tile", max(gameBoard.flatten()))
        return max(gameBoard.flatten())



if __name__ == "__main__":
    BoardEvaluationAnalysis().userTestGameboardValues()
    