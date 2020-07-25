#Snake Tutorial Python


import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


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

    def turn(self, x, y):
        self.dirnx = x
        self.dirny = y
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

    def move(self):
        global debug_flag
        if debug_flag:
            key_flag = True
            while key_flag:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    keys = pygame.key.get_pressed()

                    for key in keys:
                        if keys[pygame.K_LEFT]:
                            '''self.dirnx = -1
                            self.dirny = 0
                            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]'''  # Old code to move left
                            self.turn(-1, 0)    # New code

                        elif keys[pygame.K_RIGHT]:
                            '''self.dirnx = 1
                            self.dirny = 0
                            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]'''  # Old code to move right
                            self.turn(1, 0)     # New code

                        elif keys[pygame.K_UP]:
                            '''self.dirnx = 0
                            self.dirny = -1
                            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]'''  # Old code to move up
                            self.turn(0, -1)    # New code

                        elif keys[pygame.K_DOWN]:
                            '''self.dirnx = 0
                            self.dirny = 1
                            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]'''  # Old code to move down
                            self.turn(0, 1)     # New code
                        elif keys[pygame.K_d]:
                            debug_flag = False
                    if sum(list(keys)):
                        key_flag = False
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                keys = pygame.key.get_pressed()

                for key in keys:
                    if keys[pygame.K_LEFT]:
                        '''self.dirnx = -1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]'''  # Old code to move left
                        self.turn(-1, 0)  # New code

                    elif keys[pygame.K_RIGHT]:
                        '''self.dirnx = 1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]'''  # Old code to move right
                        self.turn(1, 0)  # New code

                    elif keys[pygame.K_UP]:
                        '''self.dirnx = 0
                        self.dirny = -1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]'''  # Old code to move up
                        self.turn(0, -1)  # New code

                    elif keys[pygame.K_DOWN]:
                        '''self.dirnx = 0
                        self.dirny = 1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]'''  # Old code to move down
                        self.turn(0, 1)  # New code
                    elif keys[pygame.K_d]:
                        debug_flag = True


        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                ''' Must be commented out, otherwise the snake will still go through the walls
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

    #### Directions from SnakeHead
    #    
    #    ul    up    ur     
    #    le   [SN]   rg
    #    dl    dn    dr
    #     
    ####

    dist = {"wall" : {"up" : 0, "ur" : 0, "rg" : 0, "dr" : 0, "dn" : 0, "dl" : 0, "le" : 0, "ul" : 0}, \
           "snake" : {"up" : 0, "ur" : 0, "rg" : 0, "dr" : 0, "dn" : 0, "dl" : 0, "le" : 0, "ul" : 0}, \
            "food" : {"up" : 0, "ur" : 0, "rg" : 0, "dr" : 0, "dn" : 0, "dl" : 0, "le" : 0, "ul" : 0}}
    
    def __init__(self):
        pass

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

def get_distances():

    # Get Distance from Head to Walls

    ki.dist["wall"]["up"] = s.head.pos[1]
    ki.dist["wall"]["dn"] = rows - s.head.pos[1] - 1
    ki.dist["wall"]["le"] = s.head.pos[0]
    ki.dist["wall"]["rg"] = rows - s.head.pos[0] - 1

    if ((rows - 1) - s.body[0].pos[0]) >= s.body[0].pos[1]:
        ki.dist["wall"]["ur"] = s.body[0].pos[1]
    else:
        ki.dist["wall"]["ur"] = rows - s.body[0].pos[0] - 1

    if s.body[0].pos[0] <= s.body[0].pos[1]:
        ki.dist["wall"]["dr"] = rows - s.body[0].pos[1] - 1
    else:
        ki.dist["wall"]["dr"] = rows - s.body[0].pos[0] - 1

    if s.body[0].pos[0] >= s.body[0].pos[1]:
        ki.dist["wall"]["ul"] = s.body[0].pos[1]
    else:
        ki.dist["wall"]["ul"] = s.body[0].pos[0]

    if ((rows - 1) - s.body[0].pos[0]) <= s.body[0].pos[1]:
        ki.dist["wall"]["dl"] = rows - s.body[0].pos[1] - 1
    else:
        ki.dist["wall"]["dl"] = ki.dist["wall"]["dl"] = s.body[0].pos[0]

    # Get Distance from Head to Body
    for body_part in s.body:
        if s.body[0] != body_part \
                and s.body[0].pos[0] == body_part.pos[0] \
                and s.body[0].pos[1] > body_part.pos[1]:
            ki.dist["snake"]["up"] = s.body[0].pos[1] - body_part.pos[1] - 1
            break
        elif body_part == s.body[-1]:
            ki.dist["snake"]["up"] = 0

    for body_part in s.body:
        if s.body[0] != body_part \
                and s.body[0].pos[0] == body_part.pos[0] \
                and s.body[0].pos[1] < body_part.pos[1]:
            ki.dist["snake"]["dn"] = body_part.pos[1] - s.body[0].pos[1] - 1
            break
        elif body_part == s.body[-1]:
            ki.dist["snake"]["dn"] = 0

    for body_part in s.body:
        if s.body[0] != body_part \
                and s.body[0].pos[1] == body_part.pos[1] \
                and s.body[0].pos[0] > body_part.pos[0]:
            ki.dist["snake"]["le"] = s.body[0].pos[0] - body_part.pos[0] - 1
            break
        elif body_part == s.body[-1]:
            ki.dist["snake"]["le"] = 0

    for body_part in s.body:
        if s.body[0] != body_part \
                and s.body[0].pos[1] == body_part.pos[1] \
                and s.body[0].pos[0] < body_part.pos[0]:
            ki.dist["snake"]["rg"] = body_part.pos[0] - s.body[0].pos[0] - 1
            break
        elif body_part == s.body[-1]:
            ki.dist["snake"]["rg"] = 0

    if s.body[0].pos[0] < (rows - 1) and s.body[0].pos[1] > 0:
        found = False
        if ((rows - 1) - s.body[0].pos[0]) >= s.body[0].pos[1]:
            for i in range(s.body[0].pos[1]):
                for body_part in s.body:
                    if s.body[0] != body_part \
                            and s.body[0].pos[0] + i + 1 == body_part.pos[0] \
                            and s.body[0].pos[1] - i - 1 == body_part.pos[1]:
                        ki.dist["snake"]["ur"] = s.body[0].pos[1] - body_part.pos[1] - 1
                        found = True
                        break
                    elif body_part == s.body[-1] and i == (s.body[0].pos[1] - 1):
                        ki.dist["snake"]["ur"] = 0
                if found:
                    break
        else:
            for i in range((rows - 1) - s.body[0].pos[0]):
                for body_part in s.body:
                    if s.body[0] != body_part \
                            and s.body[0].pos[0] + i + 1 == body_part.pos[0] \
                            and s.body[0].pos[1] - i - 1 == body_part.pos[1]:
                        ki.dist["snake"]["ur"] = s.body[0].pos[1] - body_part.pos[1] - 1
                        found = True
                        break
                    elif body_part == s.body[-1] and i == ((rows - 1) - s.body[0].pos[0] - 1):
                        ki.dist["snake"]["ur"] = 0
                if found:
                    break
    else:
        ki.dist["snake"]["ur"] = 0

    if s.body[0].pos[0] < (rows - 1) and s.body[0].pos[1] < (rows - 1):
        found = False
        if s.body[0].pos[0] <= s.body[0].pos[1]:
            for i in range((rows - 1) - s.body[0].pos[1]):
                for body_part in s.body:
                    if s.body[0] != body_part \
                            and s.body[0].pos[0] + i + 1 == body_part.pos[0] \
                            and s.body[0].pos[1] + i + 1 == body_part.pos[1]:
                        ki.dist["snake"]["dr"] = body_part.pos[1] - s.body[0].pos[1] - 1
                        found = True
                        break
                    elif body_part == s.body[-1] and i == ((rows - 1) - s.body[0].pos[1] - 1):
                        ki.dist["snake"]["dr"] = 0
                if found:
                    break
        else:
            for i in range((rows - 1) - s.body[0].pos[0]):
                for body_part in s.body:
                    if s.body[0] != body_part \
                            and s.body[0].pos[0] + i + 1 == body_part.pos[0] \
                            and s.body[0].pos[1] + i + 1 == body_part.pos[1]:
                        ki.dist["snake"]["dr"] = body_part.pos[1] - s.body[0].pos[1] - 1
                        found = True
                        break
                    elif body_part == s.body[-1] and i == ((rows - 1) - s.body[0].pos[0] - 1):
                        ki.dist["snake"]["dr"] = 0
                if found:
                    break
    else:
        ki.dist["snake"]["dr"] = 0

    if s.body[0].pos[0] > 0 and s.body[0].pos[1] > 0:
        found = False
        if s.body[0].pos[0] >= (s.body[0].pos[1]):
            for i in range(s.body[0].pos[1]):
                for body_part in s.body:
                    if s.body[0] != body_part \
                            and s.body[0].pos[0] - i - 1 == body_part.pos[0] \
                            and s.body[0].pos[1] - i - 1 == body_part.pos[1]:
                        ki.dist["snake"]["ul"] = s.body[0].pos[1] - body_part.pos[1] - 1
                        found = True
                        break
                    elif body_part == s.body[-1] and i == (s.body[0].pos[1] - 1):
                        ki.dist["snake"]["ul"] = 0
                if found:
                    break
        else:
            for i in range(s.body[0].pos[0]):
                for body_part in s.body:
                    if s.body[0] != body_part \
                            and s.body[0].pos[0] - i - 1 == body_part.pos[0] \
                            and s.body[0].pos[1] - i - 1 == body_part.pos[1]:
                        ki.dist["snake"]["ul"] = s.body[0].pos[1] - body_part.pos[1] - 1
                        found = True
                        break
                    elif body_part == s.body[-1] and i == (s.body[0].pos[0] - 1):
                        ki.dist["snake"]["ul"] = 0
                if found:
                    break
    else:
        ki.dist["snake"]["ul"] = 0

    if s.body[0].pos[0] > 0 and s.body[0].pos[1] < (rows - 1):
        found = False
        if s.body[0].pos[0] >= ((rows - 1) - s.body[0].pos[1]):
            for i in range((rows - 1) - s.body[0].pos[1]):
                for body_part in s.body:
                    if s.body[0] != body_part \
                            and s.body[0].pos[0] - i - 1 == body_part.pos[0] \
                            and s.body[0].pos[1] + i + 1 == body_part.pos[1]:
                        ki.dist["snake"]["dl"] = body_part.pos[1] - s.body[0].pos[1] - 1
                        found = True
                        break
                    elif body_part == s.body[-1] and i == ((rows - 1) - s.body[0].pos[1] - 1):
                        ki.dist["snake"]["dl"] = 0
                if found:
                    break
        else:
            for i in range(s.body[0].pos[0]):
                for body_part in s.body:
                    if s.body[0] != body_part \
                            and s.body[0].pos[0] - i - 1 == body_part.pos[0] \
                            and s.body[0].pos[1] + i + 1 == body_part.pos[1]:
                        ki.dist["snake"]["dl"] = body_part.pos[1] - s.body[0].pos[1] - 1
                        found = True
                        break
                    elif body_part == s.body[-1] and i == (s.body[0].pos[0] - 1):
                        ki.dist["snake"]["dl"] = 0
                if found:
                    break
    else:
        ki.dist["snake"]["dl"] = 0

    # Get Distance from Head to food
    if s.body[0].pos[0] == snack.pos[0] and s.body[0].pos[1] > snack.pos[1]:
        ki.dist["food"]["up"] = s.body[0].pos[1] - snack.pos[1]
    else:
        ki.dist["food"]["up"] = 0

    if s.body[0].pos[0] == snack.pos[0] and s.body[0].pos[1] < snack.pos[1]:
        ki.dist["food"]["dn"] = snack.pos[1] - s.body[0].pos[1]
    else:
        ki.dist["food"]["dn"] = 0

    if s.body[0].pos[1] == snack.pos[1] and s.body[0].pos[0] > snack.pos[0]:
        ki.dist["food"]["le"] = s.body[0].pos[0] - snack.pos[0]
    else:
        ki.dist["food"]["le"] = 0

    if s.body[0].pos[1] == snack.pos[1] and s.body[0].pos[0] < snack.pos[0]:
        ki.dist["food"]["rg"] = snack.pos[0] - s.body[0].pos[0]
    else:
        ki.dist["food"]["rg"] = 0

    if snack.pos[0] - s.body[0].pos[0] == s.body[0].pos[1] - snack.pos[1] \
            and (s.body[0].pos[0] < snack.pos[0]) \
            and (s.body[0].pos[1] > snack.pos[1]):
        ki.dist["food"]["ur"] = s.body[0].pos[1] - snack.pos[1]
    else:
        ki.dist["food"]["ur"] = 0

    if s.body[0].pos[0] - snack.pos[0] == s.body[0].pos[1] - snack.pos[1] \
            and (s.body[0].pos[0] < snack.pos[0]) \
            and (s.body[0].pos[1] < snack.pos[1]):
        ki.dist["food"]["dr"] = snack.pos[1] - s.body[0].pos[1]
    else:
        ki.dist["food"]["dr"] = 0

    if s.body[0].pos[0] - snack.pos[0] == s.body[0].pos[1] - snack.pos[1] \
            and (s.body[0].pos[0] > snack.pos[0]) \
            and (s.body[0].pos[1] > snack.pos[1]):
        ki.dist["food"]["ul"] = s.body[0].pos[1] - snack.pos[1]
    else:
        ki.dist["food"]["ul"] = 0

    if snack.pos[0] - s.body[0].pos[0] == s.body[0].pos[1] - snack.pos[1] \
            and (s.body[0].pos[0] > snack.pos[0]) \
            and (s.body[0].pos[1] < snack.pos[1]):
        ki.dist["food"]["dl"] = snack.pos[1] - s.body[0].pos[1]
    else:
        ki.dist["food"]["dl"] = 0


def main():
    global width, rows, s, snack, font, titlefont, ki, debug_flag
    debug_flag = False
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

        '''if random.randint(0, 1):
            direction = random.randint(-1, 1)
            s.turn(direction, 0)
            print("X: ", direction)
        else:
            direction = random.randint(-1, 1)
            s.turn(0, direction)
            print("Y: ", direction)'''

        clock.tick(10)
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
                message_box("You Lost!", "Play again...")
                s.reset((10, 10))
                cycles = 0
                break

        get_distances()

        dbgout["Position"] = "{}, {}".format(s.body[0].pos[0], s.body[0].pos[1])
        dbgout["Length"] = len(s.body)
        dbgout["FPS"] = "{}".format(clock)
        dbgout["Cycles"] = cycles
        dbgout["Wall_u d l r: "] = "     {}, {}, {}, {},".format(ki.dist["wall"]["up"], ki.dist["wall"]["dn"],
                                                          ki.dist["wall"]["le"], ki.dist["wall"]["rg"])
        dbgout["Wall_ur dr dl ul: "] = "     {}, {}, {}, {},".format(ki.dist["wall"]["ur"], ki.dist["wall"]["dr"],
                                                          ki.dist["wall"]["dl"], ki.dist["wall"]["ul"])
        dbgout["Snake_u d l r: "] = "     {}, {}, {}, {},".format(ki.dist["snake"]["up"], ki.dist["snake"]["dn"],
                                                            ki.dist["snake"]["le"], ki.dist["snake"]["rg"])
        dbgout["Snake_ur dr dl ul: "] = "     {}, {}, {}, {},".format(ki.dist["snake"]["ur"], ki.dist["snake"]["dr"],
                                                            ki.dist["snake"]["dl"], ki.dist["snake"]["ul"])
        dbgout["Food_u d l r: "] = "     {}, {}, {}, {},".format(ki.dist["food"]["up"], ki.dist["food"]["dn"],
                                                            ki.dist["food"]["le"], ki.dist["food"]["rg"])
        dbgout["Food_ur dr dl ul: "] = "     {}, {}, {}, {},".format(ki.dist["food"]["ur"], ki.dist["food"]["dr"],
                                                            ki.dist["food"]["dl"], ki.dist["food"]["ul"])

        redrawWindow(win)
        update_dbg_view(win, dbgout)

        pygame.display.update()
    pass


main()

