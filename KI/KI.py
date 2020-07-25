from pynput.keyboard import Key, Controller
import json

import time

class KISnake():

    keyboard = Controller()

    dist = {}
    lastcycle = 0

    # try to read file. otherwise go ahead.
    def read_file(self):
        try:
            with open('interface.txt', 'r') as file:
                self.dist = json.load(file)
                file.close()
        except:
            pass
        


    def main(self):
        self.read_file()
        num = self.dist['cycles'] 

        # when we could read a new dataset with new cycles, then we can do new calcs.
        if(num != self.lastcycle):
            self.lastcycle = num
            print("NEU - {}".format(num))
            
            print(" {} - {} ".format(num, self.dist['cycles']))
            if num == 0:
                self.keyboard.release(Key.up)
                self.keyboard.release(Key.down)
                self.keyboard.release(Key.left)
                self.keyboard.release(Key.right)
            if num == 1:
                self.keyboard.press(Key.up)
            elif num == 2:
                self.keyboard.release(Key.up)
                self.keyboard.press(Key.left) 
            elif num == 3:
                self.keyboard.release(Key.left)
                self.keyboard.press(Key.down)             
            elif num == 4:
                self.keyboard.release(Key.down)
                self.keyboard.press(Key.right) 
            elif num == 5:
                self.keyboard.release(Key.right)
                self.keyboard.press(Key.up) 



if __name__ == "__main__":
    
    ki = KISnake()

    while True:

        ki.main()
