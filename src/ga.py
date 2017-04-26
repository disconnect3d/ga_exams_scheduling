from __future__ import print_function
import random

from deap import base
from deap import creator
from deap import tools


def ga(pop_count, generations_number,
       cx_prob, mut_prob, mut_change_exam_prob,
       evaluate_func, available_timeslots, exams,
       timeslot_to_day, timeslot_to_dayslot,
       print_best, select_method=None):

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("random_timeslot", random.randint, 0, available_timeslots - 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.random_timeslot, n=len(exams))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # mate/crossover function
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutUniformInt, low=0, up=available_timeslots - 1, indpb=mut_change_exam_prob)
    toolbox.register("evaluate", evaluate_func)

    if select_method:
        select_func, select_kwargs = select_method
    else:
        select_func, select_kwargs = tools.selTournament, {'tournsize': 3}

    toolbox.register("select", select_func, **select_kwargs)

    pop = toolbox.population(n=pop_count)

    best_ever = pop[0]

    # Calculate fitness for first generation
    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)
        if ind.fitness.values > best_ever.fitness.values:
            best_ever = toolbox.clone(ind)

    print("Algorithm start")
    for gen in range(generations_number):
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = map(toolbox.clone, offspring)

        # Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cx_prob:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation on the offspring
        for mutant in offspring:
            if random.random() < mut_prob:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        current_best = tools.selBest(pop, k=1)[0]
        if current_best.fitness.values > best_ever.fitness.values:
            best_ever = toolbox.clone(ind)
    print("Algorithm end")

    # Printing result
    def print_individual(ind):
        print("Printing individual")
        print("Raw:", ind)
        print("Fitness:", ind.fitness.values)

        print(toolbox.evaluate(ind, inverse=False))

        for index, exam in enumerate(exams):
            timeslot = ind[index]
            day = timeslot_to_day(timeslot)
            slot = timeslot_to_dayslot(timeslot)
            print("Exam {} is on day {} - timeslot {}".format(exam, day, slot))

    if print_best:
        print_individual(best_ever)

    return best_ever.fitness.values[0]
