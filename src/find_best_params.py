#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from main import *

from deap import tools

select_best = [tools.selBest, {'k': 5}]
select_random = [tools.selRandom, {'k': 20}]
select_roulette = [tools.selRoulette, {'k': 20}]
select_tournament = [tools.selTournament, {'k': 10}]

mutation_probabilities = (0.01, 0.03, 0.05, 0.1, 0.2, 0.3)
mutation_change_probabilities = (0.01, 0.03, 0.05, 0.1, 0.2, 0.3)
crossover_probabilities = (0.01, 0.05, 0.1, 0.2, 0.3, 0.5)
select_methods = (select_best, select_random, select_roulette, select_tournament)

for select_method in select_methods:
    for mut_prob in mutation_probabilities:
        for mut_change_prob in mutation_change_probabilities:
            for cx_prob in crossover_probabilities:
                fitness = ga(pop_count=POPULATION_COUNT,
                             generations_number=GENERATIONS_NUMBER,
                             cx_prob=cx_prob,
                             mut_prob=mut_prob,
                             mut_change_exam_prob=mut_change_prob,
                             evaluate_func=evaluate,
                             available_timeslots=available_timeslots,
                             exams=exams,
                             timeslot_to_day=timeslot_to_day,
                             timeslot_to_dayslot=timeslot_to_dayslot,
                             print_best=True)
                print("RESULT: fit={}, mut = {}, mut_change = {}, cx = {}, select = {}"
                      .format(fitness, mut_prob, mut_change_prob, cx_prob,select_method))
