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


classes = 3
batch_size = 7
population = 20
generations = 100
threshold = 100

class KISnake():

    keyboard = Controller()

    dist = {}
    lastcycle = 0
    lastnum = 0
    lastlength = 0
    lastfoodcycle = 0
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
        self.keyboard.release('q')

    def out2keys(self):

        idx = np.argmax(self.output)

        if idx == 0:
            print("f")
            pass
        elif idx == 1:
            self.keyboard.press(Key.left)
            print("left")
        elif idx == 2:
            self.keyboard.press(Key.right)
            print("right")
        else:
            print("ERROR - SOMETHING Went wrong")

    def get_fitness(self):

        ret = 123

        return ret

    def play_game(self, model):

        while True:
            self.read_file()
            num = self.dist['cycles'] 

            if self.dist['length'] > self.lastlength:
                self.lastfoodcycle = num   

            self.lastlength = self.dist['length'] 

            if num == 0:
                self.gaming = True

            # when we could read a new dataset with new cycles, then we can do new calcs.
            if((num != self.lastcycle) & (self.gaming)):
                self.releasekeys()     
                self.lastcycle = num
                print("NEU - {}".format(num))
                xtrain = np.array([self.read_input()])

                self.output = model.predict(xtrain, batch_size=None, verbose=0)
                #print(self.output)

                self.out2keys()

                #print(f"{num},{self.lastfoodcycle}")

                if self.lastnum > num:
                    print("LEAVE Game")
                    self.lastnum = 0
                    break
                elif (num - self.lastfoodcycle) > 100:
                    print("Starved")
                    self.keyboard.press('q')
                    self.lastlength = 1
                    self.lastfoodcycle = 0
                    break
                
                self.lastnum = num

        self.gaming = False

        return self.get_fitness()   

                
    def main(self):

        networks = init_networks(population)

        for gen in range(generations):
                print ('Generation {}'.format(gen+1))
                networks = fitness(networks)
                networks = selection(networks)
                networks = crossover(networks)
                networks = mutate(networks)


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

        self._units1 = np.random.randint(1, 50)
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
    for network in networks:
        hyperparams = network.init_hyperparams()
        epochs = hyperparams['epochs']
        units1 = hyperparams['units1']
        act1 = hyperparams['act1']
        units2 = hyperparams['units2']
        act2 = hyperparams['act2']
        act3 = hyperparams['act3']
        loss = hyperparams['loss']
        opt = hyperparams['optimizer']

#        try:
        model = serve_model(epochs, units1, act1, units2, act2, classes, act3, loss, opt)

        accuracy = ki.play_game(model)

        network._accuracy = accuracy
        print ('Accuracy: {}'.format(network._accuracy))
#        except:
#            network._accuracy = 0
#            print ('Build failed.')

    return networks

def selection(networks):
    networks = sorted(networks, key=lambda network: network._accuracy, reverse=True)
    networks = networks[:int(0.2 * len(networks))]

    return networks

def crossover(networks):
    offspring = []
    for _ in range(int((population - len(networks)) / 2)):
        parent1 = random.choice(networks)
        parent2 = random.choice(networks)
        child1 = Network()
        child2 = Network()

        # Crossing over parent hyper-params
        child1._epochs = int(parent1._epochs/4) + int(parent2._epochs/2)
        child2._epochs = int(parent1._epochs/2) + int(parent2._epochs/4)

        child1._units1 = int(parent1._units1/4) + int(parent2._units1/2)
        child2._units1 = int(parent1._units1/2) + int(parent2._units1/4)

        child1._units2 = int(parent1._units2/4) + int(parent2._units2/2)
        child2._units2 = int(parent1._units2/2) + int(parent2._units2/4)

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
        if np.random.uniform(0, 1) <= 0.1:
            network._epochs += np.random.randint(0,100)
            network._units1 += np.random.randint(0,100)
            network._units2 += np.random.randint(0,100)

    return networks

def kimain():
    networks = init_networks(population)

    for gen in range(generations):
        print ('Generation {}'.format(gen+1))

        networks = fitness(networks)
        networks = selection(networks)
        networks = crossover(networks)
        networks = mutate(networks)

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
