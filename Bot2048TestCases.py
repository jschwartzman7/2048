from Bot2048 import Bot2048
from Bot2048 import expectimaxSearch
import copy
import random


pieces = [' ', '2', '4', '8', '16', '32', '64', '128']

blankBoard = [[' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ']]
class Bot2048Test:
    bot = Bot2048(expectimaxSearch())
    newTestBoards = []
    for i in range(10):
        testBoard = copy.deepcopy(blankBoard)
        for row in range(4):
            for col in range(4):
                testBoard[row][col] = pieces[random.randint(0, 7)]
        newTestBoards.append(testBoard)

    testBoards =[
            [[' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ']],

            [['4', ' ', '4', ' '],
            [' ', ' ', ' ', '2'],
            ['4', ' ', ' ', ' '],
            [' ', '2', ' ', '2']],

            [['2', ' ', '2', '2'],
            [' ', ' ', ' ', '2'],
            ['2', ' ', ' ', ' '],
            ['2', '2', ' ', '2']],

            [['4', '4', '2', '2'],
            ['4', ' ', ' ', '2'],
            ['2', ' ', ' ', '8'],
            ['2', '2', '8', '8']],

            [['4', '2', '16', '8'],
            ['2', '8', '4', '2'],
            ['32', '4', '2', '8'],
            ['16', '2', '8', '128']],

            [['4', '2', '16', '8'],
            ['2', '8', '4', '2'],
            ['32', '4', '2', '8'],
            ['16', '2', '8', ' ']],

            [[' ', '2', '16', '8'],
            ['2', '8', '4', '2'],
            ['32', '4', '2', '8'],
            ['16', '2', '8', '128']],

            [['4', '2', '16', ' '],
            ['2', '8', '4', '2'],
            ['32', '4', '2', '8'],
            ['16', '2', '8', '128']],

            [['4', '2', '16', '8'],
            ['2', '8', '4', '2'],
            ['32', '4', '2', '8'],
            [' ', '2', '8', '128']],

            [['4', '2', '16', '8'],
            ['2', ' ', '4', '2'],
            ['32', '4', '2', '2'],
            ['8', '2', '8', '128']],

            [[' ', ' ', '8', '2'],
            [' ', ' ', '4', '2'],
            [' ', '4', '2', '4'],
            ['8', '32', '64', '128']],
    ]
    
    def testMoves(self):
        for board in self.newTestBoards:
            test.bot.printBoard(board)
            print("Can move down? ", test.bot.strategy.canMoveDown(board))
            print("Can move up? ", test.bot.strategy.canMoveUp(board))
            print("Can move right? ", test.bot.strategy.canMoveRight(board))
            print("Can move left? ", test.bot.strategy.canMoveLeft(board))
            legalMoves = test.bot.strategy.getLegalMoves(board)
            print("Legal moves: ", len(legalMoves))
            tiles = test.bot.strategy.countEmptyTiles(board)
            print("Empty tiles: ", tiles)
            print("Filled tiles: ", 16-tiles)
            print("Merges:")
            for move in legalMoves:
                print(move, test.bot.strategy.numMerges(board, move[0]))
            '''newBoard = board.copy()
            test.bot.printBoard(test.bot.strategy.moveDown(newBoard))
            test.bot.printBoard(board)'''
            print()
            print()

    def testExpectimax(self, startingBoard):
        self.bot.strategy.move(startingBoard)




print("Started")
test = Bot2048Test()
startingBoard = [
        [' ', ' ', ' ', ' '],
        ['2', ' ', ' ', ' '],
        [' ', ' ', '4', ' '],
        [' ', ' ', ' ', ' ']
    ]

#test.testExpectimax(startingBoard)
test.testMoves()

 