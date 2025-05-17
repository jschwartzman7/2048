def testEvalutaionFunctions(evaluationFunctions:list, board):
    print(board)
    for eval in evaluationFunctions:
        print(eval.__name__, ": ", eval(board))