#Snake Tutorial Python
 
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
 
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
 
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
 
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
 
 
class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def turn(self, x, y):
        self.dirnx = x
        self.dirny = y
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            #print(keys)
 
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.turn(-1, 0)
 
                elif keys[pygame.K_RIGHT]:
                    self.turn(1, 0)
 
                elif keys[pygame.K_UP]:
                    self.turn(0, -1)
 
                elif keys[pygame.K_DOWN]:
                    self.turn(0, 1)
 
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                ''' Must be commented out, otherwise the snake will go through the walls
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)'''
                c.move(c.dirnx, c.dirny)
       
 
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
 
 
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
 
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
 
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
       
 
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)
 
 
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
 
    x = 0
    y = 0

    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
 
        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
       
 
def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()
 
 
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
 
 
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
 
def update_dbg_view(surface, output):

    ypos = 510
    xpos = 5

    ## Print Title
    text = titlefont.render("SnaKI/2020", True, (128, 0, 0))
    surface.blit(text, (ypos, xpos)) 
    xpos = xpos + 20

    for text, val in output.items():
        text = font.render(str(text), True, (0, 128, 0))
        surface.blit(text, (ypos, xpos))
        text = font.render(str(val), True, (0, 128, 0))
        surface.blit(text, (ypos + 100, xpos))
        xpos = xpos + 12
    

def main():
    global width, rows, s, snack, font, titlefont
    width = 500
    rows = 20
    cycles = 0
    win = pygame.display.set_mode((width*2, width))
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    flag = True
 
    pygame.init()

    titlefont = pygame.font.SysFont("consolas", 16, True, False)
    font = pygame.font.SysFont("consolas", 12, True, False)

    dbgout = {"Position" : " "} # Dictionary für Debugausgaben einfach im Code erweitern

    clock = pygame.time.Clock()

    while flag:
        cycles = cycles + 1
        pygame.time.delay(1)

        if random.randint(0, 1):
            s.turn(random.randint(-1, 1), 0)
        else:
            s.turn(0, random.randint(-1, 1))

        clock.tick(100)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:]))\
                    or s.body[x].pos[0] < 0\
                    or s.body[x].pos[0] > 19 \
                    or s.body[x].pos[1] < 0 \
                    or s.body[x].pos[1] > 19:

                print("Score: ", len(s.body))
                message_box("You Lost!", "Play again...")
                s.reset((10, 10))
                break

        dbgout["Position"] = "{}, {}".format(s.body[0].pos[0], s.body[0].pos[1])
        dbgout["FPS"] = "{}".format(clock)
        dbgout["Cycles"] = cycles

        redrawWindow(win)
        update_dbg_view(win, dbgout)
        pygame.display.update()
    pass

main()