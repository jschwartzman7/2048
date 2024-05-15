from Bot2048 import Bot2048
import SearchAgents
from SearchAgents import Search
import random
import EvaluationFunctions


def runSimulations(strategies, roundsPerStrategy=10):
    
    for strategy in strategies:
        sumMaxTiles = 0
        maxTileTotal= 0
        #print(str(strategy))
        for i in range(roundsPerStrategy):
            maxTile = simulateGame(strategy)
            #print(maxTile)
            maxTileTotal = maxTile if maxTile > maxTileTotal else maxTileTotal
            sumMaxTiles += maxTile
        return sumMaxTiles/roundsPerStrategy
        print()
        print("Max max tile: ", maxTileTotal)
        print("Average max tile: ", sumMaxTiles/roundsPerStrategy)
        print()


def randomStartingBoard():
    board = [0 for i in range(16)]
    tile1Idx, tile2Idx = random.sample(range(16), 2)
    board[tile1Idx] = 2 if random.random() < .9 else 4
    board[tile2Idx] = 2 if random.random() < .9 else 4
    return board

def simulateGame(agent):
    bot = Bot2048(agent)
    bot.board = randomStartingBoard()
    while len(bot.agent.getLegalMoves(bot.board)) > 0:
        #bot.printBoard()
        bot.agent.move(bot.board)[0](bot.board)
        #bot.printBoard()
        generatePiece(bot.board)
    print("Game over. Top piece: ", bot.getMaxTile())

def userPlayGame():
    bot = Bot2048(Search())
    bot.board = randomStartingBoard()
    bot.printBoard()
    userMoved = False
    while len(bot.agent.getLegalMoves(bot.board)) > 0:
        while not userMoved:
            x = input("Your move: ")
            match x:
                case "up":
                    if bot.agent.canMoveUp(bot.board):
                        print("Moving up")
                        bot.agent.moveUp(bot.board)
                        bot.printBoard()
                        userMoved = True
                    else:
                        print("Cannot move up.  Make a different move")

                case "down":
                    if bot.agent.canMoveDown(bot.board):
                        print("Moving down")
                        bot.agent.moveDown(bot.board)
                        bot.printBoard()
                        userMoved = True
                    else:
                        print("Cannot move down.  Make a different move")
                    
                case "left":
                    if bot.agent.canMoveLeft(bot.board):
                        print("Moving left")
                        bot.agent.moveLeft(bot.board)
                        bot.printBoard()
                        userMoved = True
                    else:
                        print("Cannot move left.  Make a different move")
                    
                case "right":
                    if bot.agent.canMoveRight(bot.board):
                        print("Moving right")
                        bot.agent.moveRight(bot.board)
                        bot.printBoard()
                        userMoved = True
                    else:
                        print("Cannot move right.  Make a different move")
                    
                case _:
                    print("Invalid move.  Make a different move")
        print("New piece...")
        generatePiece(bot.board)
        bot.printBoard()
        userMoved = False
    print("Game Over. Highest tile: ", bot.getMaxTile())



def generatePiece(board):
    emptyCords = [i for i in range(16) if board[i] == 0]
    if len(emptyCords) == 0:
        return
    random.shuffle(emptyCords)
    board[emptyCords[0]] = 2 if random.random() < .9 else 4



simulateGame(SearchAgents.randomSearch())




 





 