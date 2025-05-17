import numpy as np
from utils import colors
import pygame as pg

class Menu:
    '''
    Top right aligned text box with rows of items
    '''
    itemSpacing = 10
    itemWidthProportion = 0.75
    menuColor = (200, 100, 20)
    itemColor = colors["BOARD_COLOR"]

    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        
    def blitSurface(self, surface:pg.Surface, items:list):
        menuSurface = pg.Surface((self.width, self.height))
        menuSurface.fill(Menu.menuColor)
        for i, item in enumerate(items):
            itemSurface = pg.Surface((self.width*Menu.itemWidthProportion, self.height*Menu.itemWidthProportion/len(items)))
            itemSurface.fill(Menu.itemColor)
            text = pg.font.SysFont(None, size=20).render(str(item), True, (0,0,0))
            itemSurface.blit(text, (0, itemSurface.get_height()/2-text.get_height()/2))
            menuSurface.blit(itemSurface, (Menu.itemSpacing, i*(itemSurface.get_height()+Menu.itemSpacing)+Menu.itemSpacing))
        surface.blit(menuSurface, (surface.get_width()-menuSurface.get_width(), 0))

class Board:
    '''
    Top left aligned 2048 game board
    '''
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
    
    def blitSurface(self, surface:pg.Surface, board:np.ndarray) -> pg.Surface:
        boardSurface = pg.Surface((self.width, self.height))
        boardSurface.fill(colors['BOARD_COLOR'])
        tileSurface = pg.Surface((int(0.23*self.width), int(0.23*self.height)))
        between_tile_width = (boardSurface.get_width() - tileSurface.get_width()*4)/5
        between_tile_height = (boardSurface.get_height() - tileSurface.get_height()*4)/5
        for i in range(4):
            for j in range(4):
                if board[i, j] == 0:
                    tileSurface.fill(colors['TILE_EMPTY_COLOR'])
                else:
                    tileSurface.fill(colors['TILE_VALUE_COLORS'][board[i, j]])
                    if board[i, j] < 8:
                        text_surface = pg.font.SysFont(None, 40).render(str(int(board[i, j])), True, colors['TILE_TEXT_COLOR_LOW'])
                    else:
                        text_surface = pg.font.SysFont(None, 40).render(str(int(board[i, j])), True, colors['TILE_TEXT_COLOR_HIGH'])
                    tileTextWidth, tileTextHeight = text_surface.get_size()
                    tileSurface.blit(text_surface, ((tileSurface.get_width()-tileTextWidth)/2, (tileSurface.get_height()-tileTextHeight)/2))
                boardSurface.blit(tileSurface, ((j+1)*between_tile_width+j*(tileSurface.get_width()), (i+1)*between_tile_height+i*(tileSurface.get_height())))
        surface.blit(boardSurface, (0, 0))
    