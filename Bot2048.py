import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as Options
from bs4 import BeautifulSoup
import time
import math
import copy
import Search
from Search import expectimaxSearch


class Bot2048:
    
    def __init__(self, strategy):
        options = Options()
        options.page_load_strategy = 'eager'
        self.driver = webdriver.Chrome(options=options)
        self.actions = ActionChains(self.driver)
        self.strategy = strategy
        self.maxTile = 0
        self.board = [
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ']
        ]

    def fillBoard(self):
            HTML = self.driver.page_source
            parsedHTML = BeautifulSoup(HTML, 'html.parser')
            tiles = parsedHTML.find_all(class_="tile")
            for tile in tiles:
                value = tile.contents[0].string
                position = tile['class'][2][-3:]
                self.board[int(position[2])-1][int(position[0])-1] = int(value)
                if int(value) > self.maxTile: self.maxTile = int(value)
            return parsedHTML

    def editHTML(self):
        gameContainer = self.driver.execute_script("return document.querySelector('.container')")
        popUpAd = self.driver.execute_script("return document.querySelector('.ezmob-footer-desktop')")
        self.driver.execute_script("arguments[0].style.cssText += ';visibility: hidden;'", popUpAd)
        self.driver.execute_script("var newContainer = document.createElement('div');"
                                   "newContainer.className = arguments[0].className;"
                                   "newContainer.classList.add('new-container');"
                                   "document.body.appendChild(newContainer);"
                                   "var borderElement = document.createElement('div');"
                                   "newContainer.appendChild(borderElement);"
                                   "borderElement.style.width = '500px';"
                                   "borderElement.style.height = '700px';"
                                   "borderElement.style.position = 'absolute';"
                                   "borderElement.style.top = '-1992px';"
                                   "borderElement.style.marginTop = '30px';"
                                   "borderElement.style.border = '2000px solid black';"
                                   "borderElement.style.borderColor = '#faf8ef';"
                                   "borderElement.style.opacity = '1';", gameContainer)
        newContainer = self.driver.execute_script("return document.querySelector('.new-container')")
        self.driver.execute_script("arguments[0].style.cssText += ';justify-content: center; display: flex;'", newContainer)
        aboveGame = self.driver.execute_script("return document.querySelector('.above-game')")
        #scoreBox = self.driver.execute_script("return document.querySelector('.score-container')")
        self.driver.execute_script("var maxTile = document.createElement('div');"
                                   "arguments[0].appendChild(maxTile);"
                                   "maxTile.classList.add('max-tile');"
                                   "maxTile.style.cssText += ';position: relative; top: -7px; display: flex; background: #bbada0; font-size: 15px; height: 55px; width: 100px; line-height: 33px; font-weight: bold; border-radius: 3px; color: #eee4da; text-align: center; justify-content: center;'", aboveGame)
        maxTile = self.driver.execute_script("return document.querySelector('.max-tile')")
        self.driver.execute_script("arguments[0].innerHTML = arguments[1]", maxTile, 'Max Tile')
        self.driver.execute_script("var maxTileValue = document.createElement('div');"
                                   "arguments[0].appendChild(maxTileValue);"
                                   "maxTileValue.classList.add('max-tile-value')", maxTile)
        maxTileValue = self.driver.execute_script("return document.querySelector('.max-tile-value')")
        self.driver.execute_script("arguments[0].innerHTML = arguments[1];"
                                   "arguments[0].style.cssText += ';top: 20px; position: absolute; color: white; font-size: 25px;'", maxTileValue, self.maxTile)
 
    def play(self):
        self.driver.get('https://play2048.co')
        self.editHTML()
        won = False
        maxTileValue = self.driver.execute_script("return document.querySelector('.max-tile-value')")
        while True:
            resetBoard(self.board)
            self.fillBoard()
            while len(Search.getLegalMoves(self.board)) > 0:
                if self.maxTile == 2048 and not won:
                    time.sleep(2)
                    won = True
                    keepGoingButton = self.driver.execute_script("return document.querySelector('.keep-playing-button')")
                    keepGoingButton.click()
                self.actions.send_keys(self.strategy.move(self.board)[1]).perform()
                self.actions.reset_actions()
                resetBoard(self.board)
                time.sleep(.1)
                self.fillBoard()
                self.driver.execute_script("arguments[0].innerHTML = arguments[1];", maxTileValue, self.maxTile)
            time.sleep(2.5)
            retryButton = self.driver.execute_script("return document.querySelector('.lower')")
            retryButton.click()
            time.sleep(1)
            

    
def printBoard(board):
    maxSize = 1
    for i in range(4):
        for j in range(4):
            size = len(str(board[i][j]))
            if size > maxSize:
                maxSize = size
    for row in range(4):
        for col in range(4):
            if col < 3:
                print(board[row][col], end=(maxSize-len(str(board[row][col])))*' ')
                print('|', end='')
            else:
                print(board[row][col])
        if row < 3:
            print((maxSize*4+3)*'-')

def resetBoard(board):
    for i in range(4):
        for j in range(4):
            board[i][j] = ' '

    


