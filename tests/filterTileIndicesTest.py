import numpy as np

def testFilterTileIndices(board, filterTileIndices):
    print(board)
    print(filterTileIndices(np.argwhere(board == 0)))