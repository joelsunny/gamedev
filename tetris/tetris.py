import pygame
import pygame.freetype
import random
from pprint import pprint

shapes = {
    "rod" : [[(0,0), (0,1), (0,2),(0,3), (0,4)], [(-2,1), (-1,1), (0,1), (1,1),(2,1)]],
    "square": [[(0,0), (0,1),(1,0),(1,1)]],
    "L" : [[(0,0), (0,1), (-1,0),(-2,0)], [(0,0), (-1,0),(-1,1), (-1,2)], [(-1,0), (-1,1),(0,1),(1,1)], [(1,-1),(1,0),(1,1), (0,1)]],
    "zig": [[(-1,0), (-1,1),(0,1),(0,2)], [(0,1),(1,1),(-0,2), (-1,2)]],
    "arrow": [[(0,0), (0,1), (0,2), (-1,1)], [(0,1), (-1,1), (1,1), (0,2)], [(-1,0), (-1,1), (-1,2), (0,1)], [(0,1), (-1,1), (1,1), (0,0)]]
}

class Piece:
    def __init__(self, shape, row, col, grid_h, grid_w):
        self.shape = shape
        self.curr_orientation = 0
        self.row   = row
        self.col   = col
        self.grid_h = grid_h
        self.grid_w = grid_w
        self.cells = list(map(lambda cell: (cell[0] +  self.row, cell[1] + self.col), self.shape[self.curr_orientation]))
        
    def is_valid_cell(self, cell, grid):
        # check if cell is within the grid bounds
        if cell[0] >= self.grid_h:
            if cell[0] == self.grid_h:
                grid.on_bottom()
                return False
            return False
        elif cell[1] < 0 or cell[1] >= self.grid_w:
            return False        
        else:
            return True

    def is_occupied_cell(self, cell, grid):
        # pprint(grid.mat)
        if cell[0] < 0:
            return False
        if grid.mat[cell[0]][cell[1]] == 1:
            return True
        else:
            return False

    def move(self, dir, grid):
        new_r = self.row + dir[1]
        new_c = self.col + dir[0]

        new_cells = list(map(lambda cell: (cell[0] +  new_r, cell[1] + new_c), self.shape[self.curr_orientation]))
        # print(self.cells, new_cells)
        # if move is invalid return without changing
        for cell in new_cells:
            if self.is_valid_cell(cell, grid) == False:
                # print("invalid")
                return True

        # if new pos is occupied signal False
        for cell in new_cells:
            if self.is_occupied_cell(cell, grid) == True:
                # print(f"occupied: {cell}")
                # check if reached bottom
                if dir == (0,1):
                    grid.on_bottom()
                if cell[0] == 1:
                    grid.on_failure()
                return False

        self.row = new_r
        self.col = new_c
        
        self.cells = new_cells
        
    def rotate(self, grid):
        # print("rotating")
        new_orientation  = (self.curr_orientation + 1) % len(self.shape)
        # print(f"orientation = {new_orientation}")
        new_cells = list(map(lambda cell: (cell[0] +  self.row, cell[1] + self.col), self.shape[new_orientation]))

        # print(f"current = {self.cells}, new cells = {new_cells}")
        # if move is invalid return without changing
        for cell in new_cells:
            if self.is_valid_cell(cell, grid) == False:
                # print("invalid")
                return True

        # if new pos is occupied return without changing
        for cell in new_cells:
            if self.is_occupied_cell(cell, grid) == True:
                # print("occupied")
                return False

        # move the shape to new pos in mat
        self.cells = new_cells
        self.curr_orientation = new_orientation

class Grid: 
    DOWN = (0,1)
    LEFT = (-1,0)
    RIGHT = (1,0)

    def __init__(self, startx, starty, width, height, space):
        self.sx    = startx
        self.sy    = starty
        self.w     = width
        self.h     = height
        self.space = space
        self.rows = 25
        self.cols = 15
        self.mat   = [ [0]*self.cols for i in range(0,self.rows) ]
        self.curr_piece = self.next_piece()
        self.score = 0

    def move_piece(self):
        global fall_time, clock
        fall_speed = 0.1

        fall_time += clock.get_rawtime()
        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            self.curr_piece.move(self.DOWN, self)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
 
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.curr_piece.move(self.LEFT, self)
                    return

                elif keys[pygame.K_RIGHT]:
                    self.curr_piece.move(self.RIGHT, self)
                    return

                elif keys[pygame.K_UP]:
                    self.curr_piece.rotate(self)
                    return
 
                elif keys[pygame.K_DOWN]:
                    self.curr_piece.move(self.DOWN, self)
                    return
                
                elif keys[pygame.K_r]:
                    pygame.quit()
                    main()

    def row_collapse(self):

        for row in range(self.rows):
            if self.mat[row] == [1]*self.cols:
                print("collapsing")
                self.score += 15
                self.mat = [[0]*self.cols] + self.mat[0:row] + self.mat[row+1:]
                pprint(self.mat)

    
    def on_bottom(self):
        print("on_bottom")
        # move piece body to mat body
        for cell in self.curr_piece.cells:
            self.mat[cell[0]][cell[1]] = 1
        
        self.row_collapse()
        self.curr_piece = self.next_piece()

    def on_failure(self):
        main()

    def next_piece(self):
        x = random.randrange(len(shapes))
        key = list(shapes.keys())[x]
        print(f"key = {key}")
        return Piece(shapes[key], 0, 7, 25, 15)

    def color_cell(self, row, col, surface, color):
        pygame.draw.rect(surface, color, (self.sx + col*self.space, self.sy + row*self.space, self.space, self.space))

    def color_piece(self, surface, color=(0,255,0)):
        for cell in self.curr_piece.cells:
            if cell[0] >= 0:
                self.color_cell(cell[0], cell[1], surface, color)

    def draw(self, surface, writer):
        cols = self.w // self.space
        rows = self.h // self.space
        x, y = self.sx, self.sy

        surface.fill((0,0,0))
        
        for row in range(self.rows):
            for col in range(self.cols):
                if self.mat[row][col] == 1 and (row,col) not in self.curr_piece.cells:
                    self.color_cell(row, col, surface, (255,0,0))

        self.move_piece()
        self.color_piece(surface)
        for i in range(cols+1):
            pygame.draw.line(surface, (125,125,125), (x, self.sy), (x, self.sy+self.h ))
            x += self.space
        
        for i in range(rows+1):
            pygame.draw.line(surface, (125,125,125), (self.sx, y), (self.sx + self.w, y))
            y += self.space
        
        # print score
        score = f"Score: {self.score}"
        writer.render_to(surface, (160, 630), score, (255, 255, 0))


def main():
    global width, height, space, writer, g, clock, fall_time
    width  = 300
    height = 500
    space  = 20

    win = pygame.display.set_mode((width+100, height+200))
    pygame.init()
    writer = pygame.freetype.SysFont("Arial", 24)
    g = Grid(50, 100, width, height, 20)
    fall_time = 0

    done = False

    clock = pygame.time.Clock()
    win.fill((0,0,0))
    
    while not done:
        pygame.time.delay(50)
        clock.tick(10)
        g.draw(win, writer)
        pygame.display.update()

main()