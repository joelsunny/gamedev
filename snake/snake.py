import pygame
import pygame.freetype
import random
"""
pygame cheatsheet
    win = pygame.display.set_mode((width, width))

    eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == pygame.QUIT:
    
    pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))

    pygame.draw.line(surface, (125,125,125), (x,0),(x,width))

    pygame.display.update()

    surface.fill((0,0,0))
"""

class Cube:
    rows = 20
    width = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
 
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = ((self.pos[0] + self.dirnx)%rows, (self.pos[1] + self.dirny)%rows)
 
    def draw(self, surface, eyes=False):
        dis = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]
 
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))

class SnakeNode(Cube):
    def __init__(self, start,dirnx=1,dirny=0,color=(0,0,255) ):
        super().__init__(start, color=color)
        self.next = None
    
class Snake:
    UP = (0,-1)
    DOWN = (0,1)
    RIGHT = (1,0)
    LEFT = (-1,0)

    def __init__(self, start, color=(0,0,255)):
        self.head = SnakeNode(start,1,0,color)
        self.body = [self.head]
        self.tail = self.head
        self.dir = self.DOWN
        self.added = False

    def addNode(self):
        node = SnakeNode(self.tail.pos)
        self.tail.next = node
        self.tail = node
        self.body.append(node)
        
    def move(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
 
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    if self.dir != self.RIGHT:
                        self.dir = self.LEFT

                elif keys[pygame.K_RIGHT]:
                    if (self.dir) != self.LEFT:
                        self.dir = self.RIGHT

                elif keys[pygame.K_UP]:
                    if (self.dir) != self.DOWN:
                        self.dir = self.UP
 
                elif keys[pygame.K_DOWN]:
                    if (self.dir) != self.UP:
                        self.dir = self.DOWN

                elif keys[pygame.K_1]:
                    if not self.added:
                        self.addNode()
                        self.added = True
                
                elif keys[pygame.K_2]:
                    self.added = False
                
                elif keys[pygame.K_r]:
                    pygame.quit()
                    main()

        # move the snake body
        pos_prev = self.head.pos
        self.head.move(self.dir[0], self.dir[1])
        node = self.head.next

        while node != None:
            pos = node.pos
            node.pos = pos_prev
            pos_prev = pos
            if node.pos == self.head.pos:
                print("collision")
                main()
            node = node.next
            
            
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)
        

def drawgrid(surface, width, rows):
    n = width // rows
    x, y = 0,0
    for i in range(rows):
        x += n
        y += n

        pygame.draw.line(surface, (125,125,125), (x,0),(x,width))
        pygame.draw.line(surface, (125,125,125), (0,y),(width,y))

def randomSnack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)

def redrawScene(surface):
    global rows, width, s, snack, writer
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawgrid(surface, width,rows)
    score = f"Score: {len(s.body)-1}"
    writer.render_to(surface, (20, 520), score, (255, 255, 0))
    pygame.display.update()

def main():
    global width, rows, s, snack, writer
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width+50))
    pygame.freetype.init()
    writer = pygame.freetype.SysFont("Arial", 24)
    s = Snake([0,0])
    snack = Cube(randomSnack(rows,s), color=(0,255,0))
    done = False

    clock = pygame.time.Clock()
   
    while not done:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.head.pos == snack.pos:
            s.addNode()
            snack = Cube(randomSnack(rows, s))

        redrawScene(win)

main()