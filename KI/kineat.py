"""
2-input XOR example -- this is most likely the simplest possible example.
"""

from __future__ import print_function
import os
import neat
#import visualize
import numpy as np
from pynput.keyboard import Key, Controller
import math
import json

import time

logfname = "log-" + time.strftime("%Y%m%d-%H%M%S")


keyboard = Controller()


current_index = 0
last_index = 0
index_counter_left = 0
index_counter_right = 0

dist = {}
lastcycle = 0
lastnum = 0
lastlength = 0
lastfoodcycle = 0
distance = 0
lastdistance = 0
fitness = 0
returnfitness = 0
fitnesslength = 0
gaming = False
output = []

# try to read file. otherwise go ahead.
def read_file():
    global dist
    try:
        with open('../interface.json', 'r') as file:
            dist = json.load(file)
            file.close()
    except: 
        pass

def read_input():
    global dist
    ret = tuple()
    ret = ret + tuple(dist['food'].values())
    ret = ret + tuple(dist['block'].values())
    return ret

def releasekeys():
    global keyboard
    keyboard.release(Key.left)
    keyboard.release(Key.right)
    keyboard.release('f')
    keyboard.release('q')

def out2keys():
    global keyboard, output
    global current_index
    idx = np.argmax(output)

    if idx == 0:
        #print("f")
        keyboard.press('f')
        current_index = 0
        pass
    elif idx == 1:
        keyboard.press(Key.left)
        current_index = 1
        #print("left")
    elif idx == 2:
        keyboard.press(Key.right)
        current_index = 2
        #print("right")
    else:
        print("ERROR - SOMETHING Went wrong")

def calc_fitness():
    scoredist = 0
    scorecircle = 0

    global last_index, lastdistance, distance, fitness
    global index_counter_left
    global index_counter_right

    if current_index == last_index:
        if current_index == 1:
            index_counter_left = index_counter_left + 1
            if index_counter_left == 3:
                scorecircle = -10
                index_counter_left = 0
        elif current_index == 2:
            index_counter_right = index_counter_right + 1
            if index_counter_right == 3:
                scorecircle = -10
                index_counter_right = 0
    elif current_index != last_index and current_index != 0:
        index_counter_left = 0
        index_counter_right = 0
    last_index = current_index

    #print(last_index, index_counter_left, index_counter_right, scorecircle)

    #print(f"last:{self.lastdistance} dist: {self.distance}")
    if (lastdistance > distance):
        scoredist = 1
    else:
        scoredist = -2

    if((distance == 1 and lastdistance != math.sqrt(2)) or \
        (distance == math.sqrt(2) and lastdistance != 1)):
        scoredist = scoredist + 5
    #print(scoredist)


    fitness = fitness + scoredist + scorecircle
    #print(self.fitness)

    lastdistance = distance

def get_fitness():

    global fitnesslength, dist, fitness, returnfitness
    fitnesslength = dist['length']
    ret = fitness + ((fitnesslength - 1) * 500) + (lastcycle - lastfoodcycle)
    returnfitness = ret
    
    #print(f"Fitness Returned: {ret}\n")
    return ret


def eval_genomes(genomes, config):

    global gaming, lastfoodcycle
    global lastlength, lastcycle, lastdistance 
    global fitness, returnfitness, distance
    global output

    for genome_id, genome in genomes:   

        net = neat.nn.FeedForwardNetwork.create(genome, config)

        while True:
            read_file()
            num = dist['cycles'] 
            distance = dist['dist']

            if num == 0 and gaming == False:
                #print(f"start game {num}")
                gaming = True
                lastfoodcycle = 0
                lastlength = 1
                lastcycle = -1
                lastdistance = 0
                fitness = 0
                returnfitness = 0

            if dist['length'] > lastlength:
                lastfoodcycle = num   

            lastlength = dist['length'] 

            # when we could read a new dataset with new cycles, then we can do new calcs.
            if((num != lastcycle) & (gaming)):
                releasekeys()     

                #print("NEU - {}".format(num))
                xtrain = read_input()

                output = net.activate(xtrain)
                # self.output = model.predict(xtrain, batch_size=None, verbose=0)
                # print(output)

                out2keys()
                calc_fitness()
                #print(f"{num},{self.lastfoodcycle}")

                if lastcycle > num:
                    print(f"LEAVE Game num:{num} lastcycle{lastcycle}")
                    returnfitness = returnfitness - 200
                    break
                elif (num - lastfoodcycle) > 200:
                    print("Starved")
                    get_fitness()
                    break
                else:
                    get_fitness()
                
                lastcycle = num
                
        gaming = False
        print(f"Cycles: {lastcycle}, Fitness: {returnfitness}, Length: {fitnesslength}")

        with open(f"{logfname}.txt", "a") as file_object:
            file_object.write(f"{genome_id}, {fitnesslength}, {lastcycle}, {returnfitness}, {genome}\n")

        time.sleep(0.5)

        keyboard.press('q')

        genome.fitness = returnfitness 
        


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    # visualize.draw_net(config, winner, True, node_names=node_names)
    # visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)

    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    # p.run(eval_genomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)
