#!/usr/bin/env python
# -*- coding: utf-8 -*-

from exams import exams, exams1_indexes, exams2_indexes, exams3_indexes, extra_exams_indexes


# Number of students for particular year
students1 = 100
students2 = 70
students3 = 60

# Maps year to list of students (each student is represented as a list of exams)
students_exams = {
    1: [exams1_indexes[:] for _ in range(students1)],
    2: [exams2_indexes[:] for _ in range(students2)],
    3: [exams3_indexes[:] for _ in range(students3)],
}

# Introducing real life situations that some students from year 2 and 3 didn't pass
# exams from previous year


# 10 students didn't pass 'Fizyka 1'
physics_exam = exams.index('Fizyka 1')
for i in range(10):
    students_exams[2][i].append(physics_exam)

# 5 students didn't pass 'Fizyka 2'
physics_exam = exams.index('Fizyka 2')
for i in range(5):
    students_exams[3][i].append(physics_exam)


extra_exams_count = len(extra_exams_indexes)
# each student has 2 extra subjects exams
for student_year in students_exams.keys():
    for student_index, student_exams_list in enumerate(students_exams[student_year]):
        first_exam_index = student_index % (extra_exams_count-1)
        second_exam_index = first_exam_index + 1

        student_exams_list.append(extra_exams_indexes[first_exam_index])
        student_exams_list.append(extra_exams_indexes[second_exam_index])
