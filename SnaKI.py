
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
        self.dirnx = 1
        self.dirny = 0
 
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            #print(keys)
 
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
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
        self.dirnx = 1
        self.dirny = 0
 
 
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


# Function to calculate the 24 distances (8 directions * 3 distances(food, body, wall))
def distances(snake_x_direction, snake_y_direction, snake_body, snack_pos):

    distance_list = []

    ##### Perspective straight right (rg)
    # Distance to food (1)
    '''if snake_body[0].pos[1] == snack_pos[1] and snake_body[0].pos[0] < snack_pos[0]:
        distance_list.append(snack_pos[0] - snake_body[0].pos[0])
    else:
        distance_list.append(0)'''

    # Distance to body (2)
    '''for body_part in snake_body:
        if snake_body[0] != body_part\
                and snake_body[0].pos[1] == body_part.pos[1]\
                and snake_body[0].pos[0] < body_part.pos[0]:
            distance_list.append(body_part.pos[0] - snake_body[0].pos[0])
            break
        elif body_part == snake_body[-1]:
            distance_list.append(0)'''

    # Distance to wall (3)
    '''distance_list.append(rows - snake_body[0].pos[0])'''

    ##### Perspective down right (dr)
    # Distance to food (4)
    '''if snake_body[0].pos[0] - snack_pos[0] == snake_body[0].pos[1] - snack_pos[1]\
            and (snake_body[0].pos[0] < snack_pos[0])\
            and (snake_body[0].pos[1] < snack_pos[1]):
        distance_list.append(snack_pos[1] - snake_body[0].pos[1])
    else:
        distance_list.append(0)'''

    # Distance to body (5)
    '''if snake_body[0].pos[0] < (rows - 1) and snake_body[0].pos[1] < (rows - 1):
        found = False
        if snake_body[0].pos[0] <= snake_body[0].pos[1]:
            for i in range((rows - 1) - snake_body[0].pos[1]):
                for body_part in snake_body:
                    if snake_body[0] != body_part\
                            and snake_body[0].pos[0] + i + 1 == body_part.pos[0]\
                            and snake_body[0].pos[1] + i + 1 == body_part.pos[1]:
                        distance_list.append(body_part.pos[1] - snake_body[0].pos[1])
                        found = True
                        break
                    elif body_part == snake_body[-1] and i == ((rows - 1) - snake_body[0].pos[1] - 1):
                        distance_list.append(0)
                if found:
                    break
        else:
            for i in range((rows - 1) - snake_body[0].pos[0]):
                for body_part in snake_body:
                    if snake_body[0] != body_part\
                            and snake_body[0].pos[0] + i + 1 == body_part.pos[0]\
                            and snake_body[0].pos[1] + i + 1 == body_part.pos[1]:
                        distance_list.append(body_part.pos[1] - snake_body[0].pos[1])
                        found = True
                        break
                    elif body_part == snake_body[-1] and i == ((rows - 1) - snake_body[0].pos[0] - 1):
                        distance_list.append(0)
                if found:
                    break
    else:
        distance_list.append(0)'''

    # Distance to wall (6)
    '''if snake_body[0].pos[0] <= snake_body[0].pos[1]:
        distance_list.append(rows - snake_body[0].pos[1])
    else:
        distance_list.append(rows - snake_body[0].pos[0])'''

    ##### Perspective down (dn)
    # Distance to food (7)
    '''if snake_body[0].pos[0] == snack_pos[0] and snake_body[0].pos[1] < snack_pos[1]:
        distance_list.append(snack_pos[1] - snake_body[0].pos[1])
    else:
        distance_list.append(0)'''

    # Distance to body (8)
    '''for body_part in snake_body:
        if snake_body[0] != body_part\
                and snake_body[0].pos[0] == body_part.pos[0]\
                and snake_body[0].pos[1] < body_part.pos[1]:
            distance_list.append(body_part.pos[1] - snake_body[0].pos[1])
            break
        elif body_part == snake_body[-1]:
            distance_list.append(0)'''

    # Distance to wall (9)
    '''distance_list.append(rows - snake_body[0].pos[1])'''

    ##### Perspective down left (dl)
    # Distance to food (10)
    '''if snack_pos[0] - snake_body[0].pos[0] == snake_body[0].pos[1] - snack_pos[1]\
            and (snake_body[0].pos[0] > snack_pos[0])\
            and (snake_body[0].pos[1] < snack_pos[1]):
        distance_list.append(snack_pos[1] - snake_body[0].pos[1])
    else:
        distance_list.append(0)'''

    # Distance to body (11)
    '''if snake_body[0].pos[0] > 0 and snake_body[0].pos[1] < (rows - 1):
        found = False
        if snake_body[0].pos[0] >= ((rows - 1) - snake_body[0].pos[1]):
            for i in range((rows - 1) - snake_body[0].pos[1]):
                for body_part in snake_body:
                    if snake_body[0] != body_part\
                            and snake_body[0].pos[0] - i - 1 == body_part.pos[0]\
                            and snake_body[0].pos[1] + i + 1 == body_part.pos[1]:
                        distance_list.append(body_part.pos[1] - snake_body[0].pos[1])
                        found = True
                        break
                    elif body_part == snake_body[-1] and i == ((rows - 1) - snake_body[0].pos[1] - 1):
                        distance_list.append(0)
                if found:
                    break
        else:
            for i in range(snake_body[0].pos[0]):
                for body_part in snake_body:
                    if snake_body[0] != body_part\
                            and snake_body[0].pos[0] - i - 1 == body_part.pos[0]\
                            and snake_body[0].pos[1] + i + 1 == body_part.pos[1]:
                        distance_list.append(body_part.pos[1] - snake_body[0].pos[1])
                        found = True
                        break
                    elif body_part == snake_body[-1] and i == (snake_body[0].pos[0] - 1):
                        distance_list.append(0)
                if found:
                    break
    else:
        distance_list.append(0)'''

    # Distance to wall (12)
    '''if ((rows - 1) - snake_body[0].pos[0]) <= snake_body[0].pos[1]:
        distance_list.append(rows - snake_body[0].pos[1])
    else:
        distance_list.append(snake_body[0].pos[0] + 1)'''

    ##### Perspective left (le)
    # Distance to food (13)
    '''if snake_body[0].pos[1] == snack_pos[1] and snake_body[0].pos[0] > snack_pos[0]:
        distance_list.append(snake_body[0].pos[0] - snack_pos[0])
    else:
        distance_list.append(0)'''

    # Distance to body (14)
    '''for body_part in snake_body:
        if snake_body[0] != body_part\
                and snake_body[0].pos[1] == body_part.pos[1]\
                and snake_body[0].pos[0] > body_part.pos[0]:
            distance_list.append(snake_body[0].pos[0] - body_part.pos[0])
            break
        elif body_part == snake_body[-1]:
            distance_list.append(0)'''

    # Distance to wall (15)
    '''distance_list.append(snake_body[0].pos[0] + 1)'''

    ##### Perspective up left (ul)
    # Distance to food (16)
    '''if snake_body[0].pos[0] - snack_pos[0] == snake_body[0].pos[1] - snack_pos[1]\
            and (snake_body[0].pos[0] > snack_pos[0])\
            and (snake_body[0].pos[1] > snack_pos[1]):
        distance_list.append(snake_body[0].pos[1] - snack_pos[1])
    else:
        distance_list.append(0)'''

    # Distance to body (17)
    '''if snake_body[0].pos[0] > 0 and snake_body[0].pos[1] > 0:
        found = False
        if snake_body[0].pos[0] >= (snake_body[0].pos[1]):
            for i in range(snake_body[0].pos[1]):
                for body_part in snake_body:
                    if snake_body[0] != body_part\
                            and snake_body[0].pos[0] - i - 1 == body_part.pos[0]\
                            and snake_body[0].pos[1] - i - 1 == body_part.pos[1]:
                        distance_list.append(snake_body[0].pos[1] - body_part.pos[1])
                        found = True
                        break
                    elif body_part == snake_body[-1] and i == (snake_body[0].pos[1] - 1):
                        distance_list.append(0)
                if found:
                    break
        else:
            for i in range(snake_body[0].pos[0]):
                for body_part in snake_body:
                    if snake_body[0] != body_part\
                            and snake_body[0].pos[0] - i - 1 == body_part.pos[0]\
                            and snake_body[0].pos[1] - i - 1 == body_part.pos[1]:
                        distance_list.append(snake_body[0].pos[1] - body_part.pos[1])
                        found = True
                        break
                    elif body_part == snake_body[-1] and i == (snake_body[0].pos[0] - 1):
                        distance_list.append(0)
                if found:
                    break
    else:
        distance_list.append(0)'''

    # Distance to wall (18)
    '''if snake_body[0].pos[0] >= snake_body[0].pos[1]:
        distance_list.append(snake_body[0].pos[1] + 1)
    else:
        distance_list.append(snake_body[0].pos[0] + 1)'''

    ##### Perspective up (up)
    # Distance to food (19)
    '''if snake_body[0].pos[0] == snack_pos[0] and snake_body[0].pos[1] > snack_pos[1]:
        distance_list.append(snake_body[0].pos[1] - snack_pos[1])
    else:
        distance_list.append(0)'''

    # Distance to body (20)
    '''for body_part in snake_body:
        if snake_body[0] != body_part\
                and snake_body[0].pos[0] == body_part.pos[0]\
                and snake_body[0].pos[1] > body_part.pos[1]:
            distance_list.append(snake_body[0].pos[1] - body_part.pos[1])
            break
        elif body_part == snake_body[-1]:
            distance_list.append(0)'''

    # Distance to wall (21)
    '''distance_list.append(snake_body[0].pos[1] + 1)'''

    ##### Perspective up right (ur)
    # Distance to food (22)
    '''if snack_pos[0] - snake_body[0].pos[0] == snake_body[0].pos[1] - snack_pos[1]\
            and (snake_body[0].pos[0] < snack_pos[0])\
            and (snake_body[0].pos[1] > snack_pos[1]):
        distance_list.append(snake_body[0].pos[1] - snack_pos[1])
    else:
        distance_list.append(0)'''

    # Distance to body (23)
    '''if snake_body[0].pos[0] < (rows - 1) and snake_body[0].pos[1] > 0:
        found = False
        if ((rows - 1) - snake_body[0].pos[0]) >= snake_body[0].pos[1]:
            for i in range(snake_body[0].pos[1]):
                for body_part in snake_body:
                    if snake_body[0] != body_part\
                            and snake_body[0].pos[0] + i + 1 == body_part.pos[0]\
                            and snake_body[0].pos[1] - i - 1 == body_part.pos[1]:
                        distance_list.append(snake_body[0].pos[1] - body_part.pos[1])
                        found = True
                        break
                    elif body_part == snake_body[-1] and i == (snake_body[0].pos[1] - 1):
                        distance_list.append(0)
                if found:
                    break
        else:
            for i in range((rows - 1) - snake_body[0].pos[0]):
                for body_part in snake_body:
                    if snake_body[0] != body_part\
                            and snake_body[0].pos[0] + i + 1 == body_part.pos[0]\
                            and snake_body[0].pos[1] - i - 1 == body_part.pos[1]:
                        distance_list.append(snake_body[0].pos[1] - body_part.pos[1])
                        found = True
                        break
                    elif body_part == snake_body[-1] and i == ((rows - 1) - snake_body[0].pos[0] - 1):
                        distance_list.append(0)
                if found:
                    break
    else:
        distance_list.append(0)'''

    # Distance to wall (24)
    if ((rows - 1) - snake_body[0].pos[0]) >= snake_body[0].pos[1]:
        distance_list.append(snake_body[0].pos[1] + 1)
    else:
        distance_list.append(rows - snake_body[0].pos[0])

    print(distance_list)
    #print(distance_list[10])
    #print(#"Distance to food (rg): ", distance_list[0],     # Right/rg
           #"Distance to body (rg): ", distance_list[1],
           #"Distance to wall (rg): ", distance_list[2],
           #"Distance to food (dr): ", distance_list[3],     # Down right/dr
           #"Distance to body (dr): ", distance_list[4],
           #"Distance to wall (dr): ", distance_list[5]
           #"Distance to food (dn): ", distance_list[6],     # Down/dn
           #"Distance to body (dn): ", distance_list[7],
           #"Distance to wall (dn): ", distance_list[8],
           #"Distance to food (dl): ", distance_list[9],    # Down left/dl
           #"Distance to body (dl): ", distance_list[10],
           #"Distance to wall (dl): ", distance_list[11],
           #"Distance to food (le): ", distance_list[12],   # Left/le
           #"Distance to body (le): ", distance_list[13],
           #"Distance to wall (le): ", distance_list[14])


def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True
 
    clock = pygame.time.Clock()
   
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        distances(s.dirnx, s.dirny, s.body, snack.pos)
        #snake_length = len(s.body)
        #print(snake_length)
        #print(s.body[0].pos)

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:]))\
                    or s.body[x].pos[0] < 0\
                    or s.body[x].pos[0] > 19\
                    or s.body[x].pos[1] < 0\
                    or s.body[x].pos[1] > 19:

                print("Score: ", len(s.body))
                message_box("You Lost!", "Play again...")
                s.reset((10, 10))
                break
           
        redrawWindow(win)
    pass


main()
