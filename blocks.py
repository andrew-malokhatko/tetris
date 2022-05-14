from collections import namedtuple

SCREENSIZE = (1600, 900)
BLOCKSIZE = 50
position = namedtuple("Position", ["x", "y"])

blocks_pattern = [  #firs block is main 
    (position(SCREENSIZE[0]/2, 0), position(SCREENSIZE[0]/2, 0 - BLOCKSIZE), 
    position(SCREENSIZE[0]/2, 0 - BLOCKSIZE * 2), position(SCREENSIZE[0]/2, 0 + BLOCKSIZE)),  # vert line

    (position(SCREENSIZE[0]/2, 0), position(SCREENSIZE[0]/2, 0 + BLOCKSIZE), 
    position(SCREENSIZE[0]/2 + BLOCKSIZE, 0), position(SCREENSIZE[0]/2 + BLOCKSIZE, 0 + BLOCKSIZE)),  # 2x2

    (position(SCREENSIZE[0]/2, 0), position(SCREENSIZE[0]/2, 0 - BLOCKSIZE), 
    position(SCREENSIZE[0]/2 + BLOCKSIZE, 0), position(SCREENSIZE[0]/2 - BLOCKSIZE, 0 - BLOCKSIZE)),  # s - shape

    (position(SCREENSIZE[0]/2, 0), position(SCREENSIZE[0]/2 + BLOCKSIZE, 0), 
    position(SCREENSIZE[0]/2, 0 - BLOCKSIZE), position(SCREENSIZE[0]/2, 0 - BLOCKSIZE*2)), # L - shape

    (position(SCREENSIZE[0]/2, 0), position(SCREENSIZE[0]/2 + BLOCKSIZE, 0), 
    position(SCREENSIZE[0]/2 - BLOCKSIZE, 0), position(SCREENSIZE[0]/2, 0 + BLOCKSIZE)), # T - shape
]