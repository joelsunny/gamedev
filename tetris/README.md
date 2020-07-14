# Tetris

A write-up about Tetris game implementation in Python

## How are Tetris blocks and their rotations handled

An individual block orientation is represented by its relative pixel coordinates, which forms a list. A block together with all possible orientations resulting from rotation of the block thus becomes a list of lists.
```
shapes = {
    "rod" : [
            [(0,0), (0,1), (0,2),(0,3), (0,4)], 
            [(-2,1), (-1,1), (0,1), (1,1),(2,1)]
            ],

    "square": [[(0,0), (0,1),(1,0),(1,1)]],

    "L" : [
            [(0,0), (0,1), (-1,0),(-2,0)], 
            [(0,0), (-1,0),(-1,1), (-1,2)], 
            [(-1,0), (-1,1),(0,1),(1,1)], 
            [(1,-1),(1,0),(1,1), (0,1)]
        ],

    "zig": 
        [
            [(-1,0), (-1,1),(0,1),(0,2)], 
            [(0,1),(1,1),(-0,2), (-1,2)]
        ],

    "T": [
            [(0,0), (0,1), (0,2), (-1,1)], 
            [(0,1), (-1,1), (1,1), (0,2)], 
            [(-1,0), (-1,1), (-1,2), (0,1)], 
            [(0,1), (-1,1), (1,1), (0,0)]
        ]
}
```
  
  
Checkout full code [here](https://github.com/joelsunny/gamedev/tree/master/tetris)