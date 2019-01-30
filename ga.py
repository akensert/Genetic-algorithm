from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import os

class GeneticAlgorithm:

    def __init__ (self,
                  parameters,
                  population_size,
                  num_generations,
                  mutate_chance,
                  retain,
                  random_select):

        if not isinstance(parameters, dict):
            raise TypeError("instance 'parameters' has to be a dictionary")

        if not all(isinstance(i, (int, float)) for i in [population_size, num_generations, mutate_chance, retain, random_select]):
            raise TypeError("""instances 'population_size', 'num_generations', 'mutate_chance',\n
                              'retain' and 'random_select' have to be of type int or float""")

        self.parameters = parameters
        self.population_size = int(population_size)
        self.num_generations = num_generations
        self.mutate_chance = mutate_chance
        self.retain = retain
        self.random_select = random_select


    def initialize(self):
        """Output:
                         Parameters        Mutate NewGen Score
        initialize = [({'foo': 2, 'bar': 3}, False, True, None),
                      ({'foo': 4, 'bar': 2}, False, True, None)]

        """


        self.population = []
        for i in range(self.population_size):
            individual = {}
            for key in self.parameters:
                index = np.random.choice(range(len(self.parameters[key])))
                individual[key] = self.parameters[key][index]
            self.population.append([individual, False, True, None])


    def fitness(self, objective):
        for i, individual in enumerate(self.population):
            if any([individual[1]==True, individual[2]==True]):

                score = objective(individual[0])
                self.population[i] = [individual[0], individual[1], individual[2], score]


    def selection(self):
        """Outputs:
                        Parameters        Mutate NewGen Score
        selection = [({'foo': 5, 'bar': 3}, False, True, 0.75)]

        """
        pop_sort_by_fitness = sorted(self.population, key=lambda x: x[3], reverse=True) # reverse if low is better
        retain_N = int(len(pop_sort_by_fitness)*self.retain)
        self.population = pop_sort_by_fitness[:retain_N]

        for individual in pop_sort_by_fitness[retain_N:]:
            if self.random_select > np.random.random():
                self.population.append(individual)

        for individual in self.population:
            individual[2] = False


    def mating(self):
        """Outputs:

                          Parameters          Mutate    NewGen  Score
        mutate = [({'foo': 2, 'bar': 3}, True/False, True, 0.75),
                  ({'foo': 2, 'bar': 3}, False,      True, None)]

        """
        def mutate(individual):
            """Outputs:

                          Parameters          Mutate    NewGen  Score
            mutate = [({'foo': 2, 'bar': 3}, True/False, True, 0.75)]

            """

            for key in self.parameters:
                if self.mutate_chance > np.random.random():
                    index = np.random.choice(range(len(self.parameters[key])))
                    individual[0][key] = self.parameters[key][index]
                    individual[1]      = True    # Mutation set to True
                    individual[3]      = None    # score is now None for that individual

            return individual

        def breed(mother, father):
            """Outputs:
                        Parameters        Mutate  NewGen Score
            breed = [({'foo': 2, 'bar': 3}, False, True, None)]

            """

            child = {}
            for key in self.parameters:
                child[key] = mother[0][key] if np.random.choice([0,1]) == 0 else father[0][key]

            return [child, False, True, None]


        for i, individual in enumerate(self.population):
            self.population[i] = mutate(individual)

        while len(self.population) < self.population_size:
            male = np.random.randint(0, len(self.population))
            female = np.random.randint(0, len(self.population))

            if male != female:
                male = self.population[male]
                female = self.population[female]

                self.population.append(breed(male, female))


    def simulate(self, objective):
        """simulates one generation of the evolutionit's a bit

        namely calls the 'fitness', 'selection' and 'mating' functions

        """
        for _ in range(self.num_generations):
            self.fitness(objective)
            self.selection()
            self.mating()

            sentence=''
            for key,value in self.population[0][0].items():
               # print(value)
                sentence = sentence + value

            try:
                os.system('clear')    # for linux/macos
            except:
                os.system('cls')      # for windows

            print(sentence) #+ "    generation {}".format(_))    # prints out the current best sentence
            # print("\r" + sentence + "    generation {}".format(_)) # works only if "/n" isn't in the printable list of letters
            if self.population[0][3] == 1: # If score is 1: stop.
                break
