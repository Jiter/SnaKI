from pynput.keyboard import Key, Controller
import json

import time

from keras.models import Sequential
from keras.layers import Dense

from sklearn.model_selection import train_test_split
import numpy as np

####################################################

import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import to_categorical
from keras.utils import plot_model


classes = 3
batch_size = 7
population = 100
generations = 100
threshold = 2000

glob_gen = -1

logfname = "log-" + time.strftime("%Y%m%d-%H%M%S") + ".txt"

class KISnake():

    keyboard = Controller()

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
    def read_file(self):
        try:
            with open('interface.json', 'r') as file:
                self.dist = json.load(file)
                file.close()
        except: 
            pass

    def read_input(self):
        ret = []
        ret.extend(self.dist['food'].values())
        ret.extend(self.dist['block'].values())
        return ret


    def releasekeys(self):
        self.keyboard.release(Key.left)
        self.keyboard.release(Key.right)
        self.keyboard.release('f')
        self.keyboard.release('q')

    def out2keys(self):

        idx = np.argmax(self.output)

        if idx == 0:
            #print("f")
            self.keyboard.press('f')
            pass
        elif idx == 1:
            self.keyboard.press(Key.left)
            #print("left")
        elif idx == 2:
            self.keyboard.press(Key.right)
            #print("right")
        else:
            print("ERROR - SOMETHING Went wrong")

    def calc_fitness(self):
        scoredist = 0

        #print(f"last:{self.lastdistance} dist: {self.distance}")
        if (self.lastdistance > self.distance):
            scoredist = 1
        else:
            scoredist = -2

        self.fitness = self.fitness + scoredist
        #print(self.fitness)

        self.lastdistance = self.distance

    def get_fitness(self):

        ret = self.fitness + ((self.dist['length'] - 1) * 100) + (self.lastcycle - self.lastfoodcycle)
        self.returnfitness = ret
        self.fitnesslength = self.dist['length']

        #print(f"Fitness Returned: {ret}\n")
        return ret

    def play_game(self, model):

        while True:
            self.read_file()
            num = self.dist['cycles'] 
            self.distance = self.dist['dist']

            if num == 0 and self.gaming == False:
                #print(f"start game {num}")
                self.gaming = True
                self.lastfoodcycle = 0
                self.lastlength = 1
                self.lastcycle = -1
                self.lastdistance = 0
                self.fitness = 0
                self.returnfitness = 0

            if self.dist['length'] > self.lastlength:
                self.lastfoodcycle = num   

            self.lastlength = self.dist['length'] 

            # when we could read a new dataset with new cycles, then we can do new calcs.
            if((num != self.lastcycle) & (self.gaming)):
                self.releasekeys()     

                #print("NEU - {}".format(num))
                xtrain = np.array([self.read_input()])

                self.output = model.predict(xtrain, batch_size=None, verbose=0)
                #print(self.output)

                self.out2keys()
                self.calc_fitness()
                #print(f"{num},{self.lastfoodcycle}")

                if self.lastcycle > num:
                    print(f"LEAVE Game num:{num} lastcycle{self.lastcycle}")
                    self.returnfitness = self.returnfitness - 200
                    break
                elif (num - self.lastfoodcycle) > 200:
                    print("Starved")
                    self.get_fitness()
                    break
                else:
                    self.get_fitness()
                
                self.lastcycle = num
                
        self.gaming = False
        print(f"Cycles: {self.lastcycle}, Fitness: {self.returnfitness}, Length: {self.fitnesslength}")

        with open(logfname, "a+") as file_object:
            file_object.write(f"{self.fitnesslength}, {self.lastcycle}, {self.returnfitness}, ")
                    
        self.keyboard.press('q')

        return self.returnfitness  

                
    def main(self):
        global glob_gen

        networks = init_networks(population)

        for gen in range(generations):
                glob_gen = gen
                print ('Generation {}'.format(gen+1))
                
                with open(logfname, "a+") as file_object:
                    # Append text at the end of file
                    file_object.write(f"Generation: {gen+1}\n")

                print(f"1: {len(networks)}")
                networks = fitness(networks)
                print(f"2: {len(networks)}")
                networks = selection(networks)
                print(f"3: {len(networks)}")
                networks = crossover(networks)
                print(f"4: {len(networks)}")
                networks = mutate(networks)
                print(f"5: {len(networks)}")



def serve_model(epochs, units1, act1, units2, act2, classes, act3, loss, opt, summary=False):
    model = Sequential()
    model.add(Dense(units1, input_shape=[7,]))
    model.add(Activation(act1))
    model.add(Dense(units2))
    model.add(Activation(act2))
    model.add(Dense(classes))
    model.add(Activation(act3))
    model.compile(loss=loss, optimizer=opt, metrics=['acc'])
    if summary:
        model.summary()

    return model

class Network():
    def __init__(self):
        self._epochs = np.random.randint(1, 15)

        self._units1 = np.random.randint(1, 14)
        self._units2 = np.random.randint(1, 50)

        self._act1 = random.choice(['sigmoid', 'relu', 'softmax', 'tanh', 'elu', 'selu', 'linear'])
        self._act2 = random.choice(['sigmoid', 'relu', 'softmax', 'tanh', 'elu', 'selu', 'linear'])
        self._act3 = random.choice(['sigmoid', 'relu', 'softmax', 'tanh', 'elu', 'selu', 'linear'])

        self._loss = random.choice([
            'categorical_crossentropy',
            'binary_crossentropy',
            'mean_squared_error',
            'mean_absolute_error',
            'sparse_categorical_crossentropy'
        ])
        self._opt = random.choice(['sgd', 'rmsprop', 'adagrad', 'adadelta', 'adam', 'adamax', 'nadam'])

        self._accuracy = 0

    def init_hyperparams(self):
        hyperparams = {
            'epochs': self._epochs,
            'units1': self._units1,
            'act1': self._act1,
            'units2': self._units2,
            'act2': self._act2,
            'act3': self._act3,
            'loss': self._loss,
            'optimizer': self._opt
        }
        return hyperparams

def init_networks(population):
    return [Network() for _ in range(population)]

def fitness(networks):
    i=0
    for network in networks:
        i=i+1
        hyperparams = network.init_hyperparams()
        epochs = hyperparams['epochs']
        units1 = hyperparams['units1']
        act1 = hyperparams['act1']
        units2 = hyperparams['units2']
        act2 = hyperparams['act2']
        act3 = hyperparams['act3']
        loss = hyperparams['loss']
        opt = hyperparams['optimizer']

        try:
            model = serve_model(epochs, units1, act1, units2, act2, classes, act3, loss, opt)
            #plot_model(model, to_file=f'{glob_gen}_{i}_model.png', show_shapes=True, show_layer_names=False)
            accuracy = ki.play_game(model)

            network._accuracy = accuracy
            print ('Accuracy: {}'.format(network._accuracy))

            with open(logfname, "a+") as file_object:
                # Append text at the end of file
                file_object.write(f"{hyperparams}\n")

        except:
            network._accuracy = 0
            print ('Build failed.')

    return networks

def selection(networks):
    networks = sorted(networks, key=lambda network: network._accuracy, reverse=True)
    networks = networks[:int(0.5 * len(networks))]
    return networks

def crossover(networks):
    offspring = []
    for _ in range(int(population * 0.25)):
        parent1 = random.choice(networks)
        parent2 = random.choice(networks)
        child1 = Network()
        child2 = Network()

        # Crossing over parent hyper-params
        child1._epochs = int((parent1._epochs*4 + parent2._epochs*2)/6)
        child2._epochs = int((parent1._epochs*2 + parent2._epochs*4)/6)

        child1._units1 = int((parent1._units1*4 + parent2._units1*2)/6)
        child2._units1 = int((parent1._units1*2 + parent2._units1*4)/6)

        child1._units2 = int((parent1._units2*4 + parent2._units2*2)/6)
        child2._units2 = int((parent1._units2*2 + parent2._units2*4)/6)

        child1._act1 = parent2._act2
        child2._act1 = parent1._act2

        child1._act2 = parent2._act1
        child2._act2 = parent1._act1

        child1._act3 = parent2._act2
        child2._act3 = parent1._act2

        offspring.append(child1)
        offspring.append(child2)

        networks.extend(offspring)

    return networks

def mutate(networks):
    for network in networks:
        if np.random.uniform(0, 1) <= 0.05:
            network._epochs += np.random.randint(0,100)
            network._units1 += np.random.randint(0,100)
            network._units2 += np.random.randint(0,100)

    return networks

def kimain():
    global glob_gen

    networks = init_networks(population)

    for gen in range(generations):
        glob_gen = gen
        print ('Generation {}'.format(gen+1))

        with open(logfname, "a+") as file_object:
            # Append text at the end of file
            file_object.write(f"Generation: {gen+1}\n")

        print(f"1: {len(networks)}")
        networks = fitness(networks)
        print(f"2: {len(networks)}")
        networks = selection(networks)
        print(f"3: {len(networks)}")
        networks = crossover(networks)
        print(f"4: {len(networks)}")
        networks = mutate(networks)
        print(f"5: {len(networks)}")

        for network in networks:
            if network._accuracy > threshold:
                print ('Threshold met')
                print (network.init_hyperparams())
                print ('Best accuracy: {}'.format(network._accuracy))
                exit(0)

####################################################


if __name__ == "__main__":
    
    ki = KISnake()

    while True:
        #kimain()
        ki.main()
