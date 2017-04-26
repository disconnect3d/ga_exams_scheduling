#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from itertools import chain

from ga import ga
from testcase import exams, students_exams

# Configuration
# Assuming that there are 4 timeslots per day
# and 5 days on which you can have an exam
timeslots_per_day = 4
DAYS = 5

# Genetic algorithm variables
POPULATION_COUNT = 100
GENERATIONS_NUMBER = 50
CROSSOVER_PROBABILITY = 0.2
MUTATION_PROBABILITY = 0.1
MUTATION_CHANGE_EXAM_PROBABILITY = 0.1

available_timeslots = DAYS * timeslots_per_day

# punishments weights
STUDENT_TAKING_TWO_EXAMS_AT_ONCE = 500
STUDENT_TAKING_MORE_THAN_TWO_EXAMS_IN_ONE_DAY = 10
STUDENT_TAKING_EXAMS_ONE_AFTER_ANOTHER = 5
STUDENT_TAKING_TWO_EXAMS_IN_ONE_DAY = 3


def timeslot_to_day(timeslot):
    return int(timeslot / timeslots_per_day)


def timeslot_to_dayslot(timeslot):
    return timeslot % timeslots_per_day


# The individual is a list of numbers
# Item position in the list is index of exam in `exams` list
# Item value is the starting time of exam
def evaluate(individual, inverse=True):
    """
    :param individual: List of numbers (timeslots) for exams (the position of number is the exam number.
    :param inverse: Whether we return inverse of punishments or punishment and is_valid values.
    The `inverse=False` is used for debugging/finding best parameters.
    """
    punishments = 0
    two_exams_at_once = 0
    exam_after_another = 0
    more_than_two_exams_at_one_day = 0
    two_exams_at_one_day = 0

    # Iterate over students from all years
    for student_exams in chain(*students_exams.values()):
        student_timeslots = [individual[exam] for exam in student_exams]
        student_timeslots.sort()

        # number of exams on particular day
        exams_per_day = [0] * DAYS

        prev_timeslot = student_timeslots[0]
        prev_day = timeslot_to_day(prev_timeslot)
        exams_per_day[prev_day] += 1

        for timeslot in student_timeslots[1:]:
            diff = timeslot - prev_timeslot

            day = timeslot_to_day(timeslot)

            if prev_day == day:
                if diff == 0:
                    two_exams_at_once += 1
                elif diff == 1:
                    exam_after_another += 1

            exams_per_day[day] += 1
            prev_timeslot = timeslot
            prev_day = day

        for exams_count in exams_per_day:
            if exams_count > 2:
                more_than_two_exams_at_one_day += 1
            elif exams_count == 2:
                two_exams_at_one_day += 1

    punishments += two_exams_at_once * STUDENT_TAKING_TWO_EXAMS_AT_ONCE
    punishments += exam_after_another * STUDENT_TAKING_EXAMS_ONE_AFTER_ANOTHER
    punishments += more_than_two_exams_at_one_day * STUDENT_TAKING_MORE_THAN_TWO_EXAMS_IN_ONE_DAY
    punishments += two_exams_at_one_day * STUDENT_TAKING_TWO_EXAMS_IN_ONE_DAY

    if inverse:
        return 1.0 / (1.0 + punishments),
    else:
        is_valid = two_exams_at_once == 0
        return punishments, is_valid, {
            "two exams at once": two_exams_at_once,
            "exam after another": exam_after_another,
            "more than two exams at one day": more_than_two_exams_at_one_day,
            "two exams at one day": two_exams_at_one_day
        }


# Launch this only if this script is launched directly (don't launch this if `from main import *` is invoked)
if __name__ == '__main__':
    ga(pop_count=POPULATION_COUNT,
       generations_number=GENERATIONS_NUMBER,
       cx_prob=CROSSOVER_PROBABILITY,
       mut_prob=MUTATION_PROBABILITY,
       mut_change_exam_prob=MUTATION_CHANGE_EXAM_PROBABILITY,
       evaluate_func=evaluate,
       available_timeslots=available_timeslots,
       exams=exams,
       timeslot_to_day=timeslot_to_day,
       timeslot_to_dayslot=timeslot_to_dayslot,
       print_best=True)
