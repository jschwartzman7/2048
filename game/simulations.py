from game.gameboard import randomStartingBoard, generatePiece, randomTestBoardWeighted, stringToMove, getLegalMoves
from agents.basicagents import Agent


def simulateGame(agent:Agent, gameBoard=randomStartingBoard()):
    while getLegalMoves(gameBoard):
        gameBoard = agent.getMove(gameBoard)(gameBoard)
        generatePiece(gameBoard)
    return gameBoard

def userPlayGame():
    gameBoard = randomStartingBoard()
    print("board")
    print(gameBoard)
    while len(getLegalMoves(gameBoard)) > 0:
        text = input("Your move: ")
        if text in stringToMove:
            if stringToMove[text]['can'](gameBoard):
                print("Moving ", text)
                gameBoard = stringToMove[text]['move'](gameBoard)
                gameBoard = generatePiece(gameBoard)
                print(gameBoard)
            else:
                print("Cannot move ", text)
            print()
        else:
            print("Invalid move.  Re-enter your move")
    print("Game Over")
    print("Highest tile: ", max(gameBoard))
    print("Total score: ", sum(gameBoard))
