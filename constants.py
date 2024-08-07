import numpy as np

rand = np.random.default_rng()

maxExponent = 11

indices2D = [(0,0), (0,1), (0,2), (0,3), 
             (1,0), (1,1), (1,2), (1,3),
             (2,0), (2,1), (2,2), (2,3),
             (3,0), (3,1), (3,2), (3,3)]

primeBoard = np.array([[2, 3, 5, 7],
                     [11, 13, 17, 19],
                     [23, 29, 31, 37],
                     [41, 43, 47, 53]])

snakePaths = np.array([[[0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3], [0,1,2,3,3,2,1,0,0,1,2,3,3,2,1,0]],
                       [[0,1,2,3,3,2,1,0,0,1,2,3,3,2,1,0], [0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3]],
                       [[0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3], [3,2,1,0,0,1,2,3,3,2,1,0,0,1,2,3]],
                       [[0,1,2,3,3,2,1,0,0,1,2,3,3,2,1,0], [3,3,3,3,2,2,2,2,1,1,1,1,0,0,0,0]],
                       [[3,3,3,3,2,2,2,2,1,1,1,1,0,0,0,0], [0,1,2,3,3,2,1,0,0,1,2,3,3,2,1,0]],
                       [[3,2,1,0,0,1,2,3,3,2,1,0,0,1,2,3], [0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3]],
                       [[3,3,3,3,2,2,2,2,1,1,1,1,0,0,0,0], [3,2,1,0,0,1,2,3,3,2,1,0,0,1,2,3]],
                       [[3,2,1,0,0,1,2,3,3,2,1,0,0,1,2,3], [3,3,3,3,2,2,2,2,1,1,1,1,0,0,0,0]]])

cornerControl2 =         [[[[0],[0]],
                         [[1,0],[0,1]],
                       [[2,1,0],[0,1,2]],
                     [[3,2,1,0],[0,1,2,3]],
                       [[3,2,1],[1,2,3]],
                         [[3,2],[2,3]],
                           [[3],[3]]],

                           [[[3],[3]],
                          [[3,2],[2,3]],
                        [[3,2,1],[1,2,3]],
                      [[3,2,1,0],[0,1,2,3]],
                        [[2,1,0],[0,1,2]],
                          [[1,0],[0,1]],
                            [[0],[0]]],

                          [[[0],[3]],
                         [[1,0],[3,2]],
                       [[2,1,0],[3,2,1]],
                     [[3,2,1,0],[3,2,1,0]],
                       [[3,2,1],[2,1,0]],
                         [[3,2],[1,0]],
                           [[3],[0]]],
                           
                          [[[3],[0]],
                         [[3,2],[1,0]],
                       [[3,2,1],[2,1,0]],
                     [[3,2,1,0],[3,2,1,0]],
                       [[2,1,0],[3,2,1]],
                         [[1,0],[3,2]],
                           [[0],[3]]]]
testBoards = [
    np.array([[0, 0, 0,  2],
              [0, 0, 2,  8], 
              [0, 2, 8,  64],
              [2, 8, 64, 512]]),

    np.array([[0, 0, 0,  0],
              [0, 2, 4,  8], 
              [128, 64, 32,  16],
              [256, 512, 1024, 2048]]),

    np.array([[2,  16, 64,  8],
              [2,  2, 4,   32],
              [64, 8, 512, 128],
              [0,  2, 1024,   8]]),

    np.array([[0, 0, 0, 0],
               [4, 0, 0, 0],
               [16, 0, 4, 0],
               [4, 4, 4, 2]]),

    np.array([[0, 0, 5, 0],
               [0, 0, 0, 3],
               [2, 4, 1, 0],
               [0, 0, 0, 0]]), 
    
    np.array([[0,  64, 512,  64],
              [  0,   0,   4, 512],
              [  0 ,  0 ,  8 , 64],
              [  0 ,  2 , 16 , 32]]),

    np.array([[4, 0, 2, 4],
               [4, 2, 4, 0],
               [2, 4, 0, 0],
               [4, 0, 0, 0]]),
               
      np.array([[4, 0, 2, 2],
                [2, 2, 2, 0],
                [0, 4, 0, 2],
                [4, 2, 0, 2]])]

if __name__ == "__main__":
    pass