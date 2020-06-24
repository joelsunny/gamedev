import pygame
import pygame.freetype
import random
from pprint import pprint
from collections import namedtuple

Point = namedtuple('Point', 'x y')

class Grid:
    WIDTH = 720
    HEIGHT = 720
    CELL = 1

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.writer = pygame.freetype.SysFont("Arial", 24)
    
    def color_cell(self, row, col, color = (255,255,255)):
        print(f"row = {row}, col = {col}")
        pygame.draw.rect(self.surface, color, (col*self.CELL+1, row*self.CELL+1, 20, 20))
        # self.writer.render_to(self.surface, (col*self.CELL + self.CELL/2, row*self.CELL + self.CELL//3), str(num), (0, 0, 0))

    def draw(self, b):
        self.surface.fill((0,0,0))
        self.color_cell(b.y, b.x)

class Pillar:
    def __init__(self, x, height, top = True):
        self.x = x
        self.y = 0
        self.v_x = -10
        self.h = height
        self.w = 80
        self.gap = 150
        self.t = 0

    def reset_height(self):
        self.h = random.randint(0,3)*100 + 100

    def move(self):
        self.t = clock.get_rawtime()/100
        self.x += self.v_x*self.t
        if self.x < -self.w:
            self.x = 720
            self.reset_height()

    def draw(self, surface):
        color = (0,255,0)
        print(f"pillar : {self.x, self.y}")
        self.move()
        pygame.draw.rect(surface, color, (self.x, self.y, self.w, self.h) )
        pygame.draw.rect(surface, color, (self.x, self.y + self.h + self.gap, self.w, 720-(self.y + self.h + self.gap)) )

class Bird:
    def __init__(self):
        self.x = 300
        self.y = 300
        self.v_x = 0
        self.g_y = 10
        self.v_y = 0
        self.t = 0

    def jump(self):
        self.g_y = -30
    
    def check_collision(self):
        global pillars
        def doOverlap(l1, r1, l2, r2, top=True): 
            
            # If one rectangle is on left side of other 
            if(l1.x >= r2.x or r1.x <= l2.x): 
                return False
        
            # If one rectangle is above other 
            if(l1.y >= r2.y and top): 
                return False
            
            if(r1.y <= l2.y and not top): 
                return False
            
            return True
  
        for pillar in pillars:
            if doOverlap(Point(self.x, self.y), Point(self.x+20, self.y+20), Point(pillar.x,pillar.y), Point(pillar.x+pillar.w,pillar.y+pillar.h)):
                return True
            elif doOverlap(Point(self.x, self.y), Point(self.x+20, self.y+20), Point(pillar.x, pillar.y + pillar.h + pillar.gap), Point(pillar.x+pillar.w,720), top=False):
                return True

        return False

    def move(self):
        if self.check_collision():
            pygame.quit()
            main()

        self.t = clock.get_rawtime()/100
        print(f"t = {self.t}")
        # self.x += self.v_x*self.t
        self.y += self.v_y*self.t
        self.v_y += self.g_y*self.t

        if self.v_y <=0:
            self.g_y = 10

        if self.y > 700:
            self.y = 700
            self.v_y = 0
        if self.y < 20:
            self.y = 20
            self.v_y = 0
        if self.x > 700:
            self.x = 700
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
 
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_UP]:
                    self.jump()
                    return
 
                elif keys[pygame.K_r]:
                    pygame.quit()
                    main()

def main():
    global g, clock, pillars
    done = False

    clock = pygame.time.Clock()
    g = Grid()
    b = Bird()
    # create 3 pillars
    p1 = Pillar(720, 200)
    p2 = Pillar(1000, 300)
    p3 = Pillar(1280, 100)
    pillars = [p1,p2,p3]

    while not done:
        pygame.time.delay(50)
        clock.tick(10)
        b.move()
        g.draw(b)
        p1.draw(g.surface)
        p2.draw(g.surface)
        p3.draw(g.surface)
        pygame.display.update()

main()