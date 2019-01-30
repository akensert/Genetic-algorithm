from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import string
from functools import partial, update_wrapper
from ga import GeneticAlgorithm



target = "Hello World!"

"""Create custom objective"""
def wrapped_partial(func, *args, **kwargs):
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func

def objective(individual, target):
    score = np.empty(len(target))
    for j, (key, letter) in enumerate(zip(individual, target)):
        score[j] = individual[key] in letter

    return score.sum()/len(score)

custom_objective = wrapped_partial(objective, target=target)


"""Parameters"""
parameters = {}
keys       = range(len(target))
for k in keys:
    parameters[k] = [string.printable[x] for x in range(len(string.printable))]

population_size = 75
num_generations = 1000
mutate_chance = .75/len(target)
retain = 0.15
random_select = 0.05

ga = GeneticAlgorithm(parameters, population_size, num_generations, mutate_chance, retain, random_select)
ga.initialize()
ga.simulate(custom_objective)
