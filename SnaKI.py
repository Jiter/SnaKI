#Snake Tutorial Python
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

import json

class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
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

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 1
        self.dirny = 0

        self.currdir  = 1
        self.directions = {     0: (0, 1),
                                1: (1, 0),
                                2: (0, -1),
                                3: (-1, 0)}

    def turn(self, x, y):
        self.dirnx = x
        self.dirny = y
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

    def move(self):

        global debug_flag, cycles

        if debug_flag:
            key_flag = True
            while key_flag:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    if event.type == pygame.KEYDOWN:
                        #print("f")
                        key_flag = False

                        if event.key == pygame.K_LEFT:
                            #print("l")
                            self.currdir = (self.currdir + 1) % 4
                            self.turn( self.directions[self.currdir][0] , self.directions[self.currdir][1] )  # New code

                        if event.key == pygame.K_RIGHT:
                            #print("r")
                            self.currdir = (self.currdir - 1) % 4
                            self.turn( self.directions[self.currdir][0] , self.directions[self.currdir][1] )  # New code

                        if event.key == pygame.K_d:
                            #print("d")
                            debug_flag = False

                        if event.key == pygame.K_q:
                            #print("s")
                            s.reset((9, 9))
                            cycles = 0

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    #print("f")

                    if event.key == pygame.K_LEFT:
                        #print("l")
                        self.currdir = (self.currdir + 1) % 4
                        self.turn( self.directions[self.currdir][0] , self.directions[self.currdir][1] )  # New code

                    if event.key == pygame.K_RIGHT:
                        #print("r")
                        self.currdir = (self.currdir - 1) % 4
                        self.turn( self.directions[self.currdir][0] , self.directions[self.currdir][1] )  # New code

                    if event.key == pygame.K_d:
                        #print("d")
                        debug_flag = True

                    if event.key == pygame.K_q:
                        #print("s")
                        s.reset((9, 9))
                        cycles = 0


        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}

        self.dirnx = 1
        self.dirny = 0
 
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


class SnaKI(object):

    #### Directions are from SnakeView
    #    
    #          fw     
    #    le   [SN]   rg
    #         [SN]   
    #          be
    #
    #   Block is blocked Field with View Distance 1
    #   food is direction of food over the whole Field
    #
    ####

    dist = {"block" : {"fw" : 0, "rg" : 0, "le" : 0}, \
            "food" : {"fw" : 0, "rg" : 0, "be" : 0, "le" : 0}}
    
    fileinterface = {}

    def __init__(self):
        pass

    def get_foodquad(self):

        ki.dist["food"]["fw"] = False
        ki.dist["food"]["rg"] = False
        ki.dist["food"]["be"] = False
        ki.dist["food"]["le"] = False

        if s.currdir == 0: # DOWN
            if s.head.pos[0] == snack.pos[0] and s.head.pos[1] < snack.pos[1]:
                ki.dist["food"]["fw"] = True
            elif s.head.pos[1] > snack.pos[1]:
                ki.dist["food"]["be"] = True
            elif s.head.pos[0] < snack.pos[0] and s.head.pos[1] <= snack.pos[1]:
                ki.dist["food"]["le"] = True
            elif s.head.pos[0] > snack.pos[0] and s.head.pos[1] <= snack.pos[1]:
                ki.dist["food"]["rg"] = True
        elif s.currdir == 1: # RIGHT
            if s.head.pos[1] == snack.pos[1] and s.head.pos[0] < snack.pos[0]:
                ki.dist["food"]["fw"] = True
            elif s.head.pos[0] > snack.pos[0]:
                ki.dist["food"]["be"] = True
            elif s.head.pos[1] > snack.pos[1] and s.head.pos[0] <= snack.pos[0]:
                ki.dist["food"]["le"] = True
            elif s.head.pos[1] < snack.pos[1] and s.head.pos[0] <= snack.pos[0]:
                ki.dist["food"]["rg"] = True
        elif s.currdir == 2: # UP
            if s.head.pos[0] == snack.pos[0] and s.head.pos[1] > snack.pos[1]:
                ki.dist["food"]["fw"] = True
            elif s.head.pos[1] < snack.pos[1]:
                ki.dist["food"]["be"] = True
            elif s.head.pos[0] > snack.pos[0] and s.head.pos[1] >= snack.pos[1]:
                ki.dist["food"]["le"] = True
            elif s.head.pos[0] < snack.pos[0] and s.head.pos[1] >= snack.pos[1]:
                ki.dist["food"]["rg"] = True
        elif s.currdir == 3: # LEFT
            if s.head.pos[1] == snack.pos[1] and s.head.pos[0] > snack.pos[0]:
                ki.dist["food"]["fw"] = True
            elif s.head.pos[0] < snack.pos[0]:
                ki.dist["food"]["be"] = True
            elif s.head.pos[1] < snack.pos[1] and s.head.pos[0] >= snack.pos[0]:
                ki.dist["food"]["le"] = True
            elif s.head.pos[1] > snack.pos[1] and s.head.pos[0] >= snack.pos[0]:
                ki.dist["food"]["rg"] = True

        ki.dist["dist"] = math.sqrt(pow(abs(s.head.pos[0]-snack.pos[0]), 2) \
                                            +pow(abs(s.head.pos[1]-snack.pos[1]), 2))
        #print(ki.dist["dist"])



    def get_blocks(self):

        next_xcoord = s.body[0].pos[0] + s.head.dirnx 
        next_ycoord = s.body[0].pos[1] + s.head.dirny
        next_lxcoord = s.body[0].pos[0] + s.directions[(s.currdir + 1) % 4][0] 
        next_lycoord = s.body[0].pos[1] + s.directions[(s.currdir + 1) % 4][1] 
        next_rxcoord = s.body[0].pos[0] + s.directions[(s.currdir - 1) % 4][0]  
        next_rycoord = s.body[0].pos[1] + s.directions[(s.currdir - 1) % 4][1] 

        #print("fw: {}, {}\nle: {}, {}\nre: {}, {}\n".format(next_xcoord, next_ycoord, next_lxcoord, next_lycoord, next_rxcoord, next_rycoord))
        if ((next_ycoord not in range(0, 20)) or (next_xcoord not in range(0, 20))) or \
            (next_xcoord, next_ycoord) in map(lambda z: z.pos, s.body[1:]):
            ki.dist["block"]["fw"] = True
        else:
            ki.dist["block"]["fw"] = False
        if ((next_lycoord not in range(0, 20)) or (next_lxcoord not in range(0, 20))) or \
            (next_lxcoord, next_lycoord) in map(lambda z: z.pos, s.body[1:]):
            ki.dist["block"]["le"] = True
        else:
            ki.dist["block"]["le"] = False
        if ((next_rycoord not in range(0, 20)) or (next_rxcoord not in range(0, 20))) or \
            (next_rxcoord, next_rycoord) in map(lambda z: z.pos, s.body[1:]):
            ki.dist["block"]["rg"] = True
        else:
            ki.dist["block"]["rg"] = False
       
        



def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0

    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)

def randomSnack(rows, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


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


def write_file():
    with open('interface.json', 'w') as file:
        file.write(json.dumps(ki.fileinterface)) # use `json.loads` to do the reverse
        file.close()


def main():
    global width, rows, s, snack, font, titlefont, ki, debug_flag, cycles
    debug_flag = True
    reset_flag = 0
    
    width = 500
    rows = 20
    cycles = 0
    win = pygame.display.set_mode((width*2, width))
    s = snake((255, 0, 0), (9, 9))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    ki = SnaKI()
    flag = True

    pygame.init()

    titlefont = pygame.font.SysFont("consolas", 16, True, False)
    font = pygame.font.SysFont("consolas", 12, True, False)

    # Dictionary für Debugausgaben einfach im Code erweitern
    dbgout = {"Position": " "}

    clock = pygame.time.Clock()

    while flag:

        #pygame.time.delay(50)

        cycles = cycles + 1

        s.move()

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:]))\
                    or (len(s.body) > 1
                        and ((s.body[0].dirnx == -s.body[1].dirnx and s.body[0].dirnx != 0)
                             or (s.body[0].dirny == -s.body[1].dirny and s.body[0].dirny != 0)))\
                    or s.body[x].pos[0] < 0\
                    or s.body[x].pos[0] > 19\
                    or s.body[x].pos[1] < 0\
                    or s.body[x].pos[1] > 19:

                print("Score: ", len(s.body))
                #message_box("You Lost!", "Play again...")
                s.reset((9, 9))
                cycles = 0
                snack = cube(randomSnack(rows, s), color=(0, 255, 0))
                break
        
        ki.get_blocks()
        ki.get_foodquad()

        dbgout["Position"] = "{}, {}".format(s.body[0].pos[0], s.body[0].pos[1])
        dbgout["Length"] = len(s.body)
        dbgout["FPS"] = "{}".format(clock)
        dbgout["Cycles"] = cycles
         
        dbgout["dirx"] = s.head.dirnx
        dbgout["diry"] = s.head.dirny
        dbgout["blocks"] = ki.dist['block']   
        dbgout["food"] = ki.dist['food']  
        dbgout["distance"] = ki.dist['dist']

        #update the interfacetextfile
        ki.fileinterface.update([('cycles', cycles)])
        ki.fileinterface.update([('length', len(s.body))])
        ki.fileinterface.update(ki.dist)

        redrawWindow(win)
        update_dbg_view(win, dbgout)
        write_file()
        pygame.display.update()
        clock.tick(20)
    pass


main()

