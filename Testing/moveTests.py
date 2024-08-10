def testMove(board, moveFunction):
    print(board)
    print("Moving ", moveFunction.__name__)
    board = moveFunction(board)
    print(board)