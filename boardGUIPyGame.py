import pygame as pg
from gameBoard import randomStartingBoard, randomTestBoardWeighted, randomPositions
from searchAgents import getLegalMoves, moveInDirection, canMoveInDirection
from evaluationFunctions import snakeStrength, cornerStrength, cornerSnakeStrength, highestPiece
import numpy as np
from constants import rand

tileValueColors = {
    2:(239,228,218),
    4:(238,225,201),
    8:(243,178,123),
    16:(246,150,101),
    32:(247,124,95),
    64:(248,96,59),
    128:(237,208,115),
    256:(237,204,99),
    512:(237,201,80),
    1024:(237,197,63),
    2048:(237,194,46)
}
evaluationFuntions = [snakeStrength, cornerStrength, cornerSnakeStrength, highestPiece]

pg.init()
DISPLAY_WIDTH, DISPLAY_HEIGHT = 800, 400
displayScreen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pg.time.Clock()
boardSurface = pg.Surface((int(0.75*DISPLAY_WIDTH), int(0.75*DISPLAY_HEIGHT)))
tileSurface = pg.Surface((int(0.23*boardSurface.get_width()), int(0.23*boardSurface.get_height())))
backgroundColor = (250, 248, 239)
boardColor = (187, 173, 161)
tileEmptyColor = (205, 193, 181)

pg.font.init()
tileFont = pg.font.SysFont(None, size=min(tileSurface.get_width(), tileSurface.get_height())//3)
tileTextColorLow = (119,110,101)
tileTextColorHigh = (250,246,243)
gameOverFont = pg.font.SysFont(None, 100)
    

def updateBoardTestValues(board:np.ndarray, mouseClickedPos:list, curTileSelected:int) -> None:
    boardSurface.fill(boardColor)
    space_width = (boardSurface.get_width() - tileSurface.get_width()*4)/5
    space_height = (boardSurface.get_height() - tileSurface.get_height()*4)/5
    for i in range(4):
        for j in range(4):
            if tileSurface.get_rect(topleft=((j+1)*space_width+j*(tileSurface.get_width()), (i+1)*space_height+i*(tileSurface.get_height()))).collidepoint(mouseClickedPos):
                if board[i, j] == curTileSelected:
                    board[i, j] = 0
                else:
                    board[i, j] = curTileSelected
            if board[i, j] == 0:
                tileSurface.fill(tileEmptyColor)
            else:
                if board[i, j] < 8:
                    text_surface = tileFont.render(str(board[i, j]), True, tileTextColorLow)
                else:
                    text_surface = tileFont.render(str(board[i, j]), True, tileTextColorHigh)
                tileSurface.fill(tileValueColors[board[i, j]])
                tileSurface.blit(text_surface, (tileSurface.get_width()/3, tileSurface.get_height()/3))
            boardSurface.blit(tileSurface, ((j+1)*space_width+j*(tileSurface.get_width()), (i+1)*space_height+i*(tileSurface.get_height())))
    

def updateBoardPlayGame(board:np.ndarray, newTileIdx:list) -> None:
    boardSurface.fill(boardColor)
    space_width = (boardSurface.get_width() - tileSurface.get_width()*4)/5
    space_height = (boardSurface.get_height() - tileSurface.get_height()*4)/5
    for i in range(4):
        for j in range(4):
            if board[i, j] == 0:
                tileSurface.fill(tileEmptyColor)
            else:
                if board[i, j] < 8:
                    text_surface = tileFont.render(str(board[i, j]), True, tileTextColorLow)
                else:
                    text_surface = tileFont.render(str(board[i, j]), True, tileTextColorHigh)
                tileSurface.fill(tileValueColors[board[i, j]])
                tileSurface.blit(text_surface, (tileSurface.get_width()/3, tileSurface.get_height()/3))
            if newTileIdx[0] == i and newTileIdx[1] == j:
                pg.draw.rect(tileSurface, (255, 0, 0), (0, 0, tileSurface.get_width(), tileSurface.get_height()), 5)
            boardSurface.blit(tileSurface, ((j+1)*space_width+j*(tileSurface.get_width()), (i+1)*space_height+i*(tileSurface.get_height())))
           

def userTestGameboardValues():
    gameBoard = np.zeros((4,4))
    running = True
    curTileSelected = 2
    mouseClicked = [-1,-1]
    while running:
        displayScreen.fill(backgroundColor)
        updateBoardTestValues(gameBoard, mouseClicked, curTileSelected)
        mouseClicked = [-1,-1]
        displayScreen.blit(boardSurface, (0, 0))
        selectedTileText = tileFont.render(str(curTileSelected), True, (0,0,0))
        displayScreen.blit(selectedTileText, (boardSurface.get_width(), 0))
        
        gameBoard = np.array(gameBoard)
        
        for i, eval in enumerate(evaluationFuntions):
            
            boardValue = eval(np.log2(gameBoard, where=gameBoard>0))
            functionNameTest = tileFont.render(eval.__name__, True, (0,0,0))
            evaluationFunctionText = tileFont.render(str(boardValue), True, (0,0,0))
            displayScreen.blit(functionNameTest, (boardSurface.get_width(), tileSurface.get_height()*(i+1)*1.05))
            displayScreen.blit(evaluationFunctionText, (boardSurface.get_width()+tileSurface.get_width(), tileSurface.get_height()*(i+1)))
            
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
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
        clock.tick(30)
        



def userPlayGameboardVisuals():
    gameBoard = randomStartingBoard()
    running = True
    newTileX = -1
    newTileY = -1
    while len(getLegalMoves(gameBoard)) > 0 and running:
        displayScreen.fill(backgroundColor)
        updateBoardPlayGame(gameBoard, [newTileX, newTileY])
        displayScreen.blit(boardSurface, (0, 0))
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
            gameBoard, newTileX, newTileY = generatePieceNewTileIdx(gameBoard, newTileX, newTileY)
        
        pg.display.update()
        pg.display.flip()
        clock.tick(30)
        
    while running:
        displayScreen.fill(backgroundColor)
        updateBoardTestValues(gameBoard, [newTileX, newTileY])
        gameOverText = gameOverFont.render('Game Over', True, (0, 0, 0))
        boardSurface.blit(gameOverText, (0,0))
        displayScreen.blit(boardSurface, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        pg.display.update()
        pg.display.flip()
        clock.tick(30)

def generatePieceNewTileIdx(board:np.ndarray, newX, newY) -> np.ndarray:
    emptyCords = np.argwhere(board == 0)
    if emptyCords.size > 0:
        newIdx = rand.choice(emptyCords)
        newX, newY = newIdx
        board[newIdx[0],newIdx[1]] = rand.choice([2,4], p=[0.9,0.1])
    return board, newX, newY

if __name__ == "__main__":
    userTestGameboardValues()