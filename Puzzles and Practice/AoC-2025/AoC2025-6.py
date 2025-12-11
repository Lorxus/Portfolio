# This program takes in a block of text where problems run vertically and are separated by whitespace, and each problem consists of a column of numbers followed by either '+' or '*'.
import copy
import math

FILENAME = "input6-2025.txt"  # contains the provided ordering rules and update batches

with open(FILENAME, 'r') as rawfile:
    rawarray = rawfile.read().splitlines()

full_hw = []
for line in rawarray:
    full_hw.append(line.split())

answers = []
numbers = []
operations = full_hw[-1]

for line in full_hw[:-1]:
    line = list(map(int, line))
    numbers.append(line)

# Part 1: The program calculates the sum or product of the column of numbers as indicated, then outputs the sum over all subanswers.

for problem in range(len(numbers[0])):
    op = operations[problem]
    acc = 0 if op == '+' else 1
    for idx in range(len(numbers)):
        acc = acc + numbers[idx][problem] if op == '+' else acc * numbers[idx][problem]
    answers.append(acc)

print('The sum of all answers to problems is ' + str(sum(answers)) + '.')

# Part 2: The program does the same as before, except that it takes into account that all numbers are actually read top-to-bottom, right-to-left. Note that the columnar numbers are whitespace-sensitive, so we'll need to go right back to rawarray!

answers = []
rawarray = rawarray[:-1]  # remove the operations
columnar_numbers = [[] for _ in range(len(numbers[0]))]  # one subarray for every problem

active_col = len(columnar_numbers) - 1
saw_digit = False

for col_idx in range(len(rawarray[0])-1, -1, -1):  # stepping through from right to left
    temp_str = ''
    for row_idx in range(len(rawarray)): # accumulate all characters in the textual column
        if rawarray[row_idx][col_idx] != ' ':  # if we don't hit a space, all's well
            temp_str += rawarray[row_idx][col_idx]
            saw_digit = True
        elif rawarray[row_idx][col_idx] == ' ' and saw_digit:  # if we do hit a space, check if we've hit a space so far this column - notably this will never happen at the very start of a new problem, and at the start of a new number, we can ignore spaces anyway
            temp_str += ''  #
        else:  # what if we haven't yet hit a digit? nothing, actually.
            temp_str += rawarray[row_idx][col_idx]
            saw_digit = False  # this never executes if we've already hit a digit this column - in that case we're not even in this branch!
    if temp_str.split() == []:  # check if it's all whitespace - if so, move to the left in columnar_numbers...
        active_col -= 1
        saw_digit = False
        continue
    else:  # ... and otherwise append the number and keep going
        columnar_numbers[active_col].append(int(temp_str))
        saw_digit = False

for problem in range(len(columnar_numbers)):
    op = operations[problem]
    acc = sum(columnar_numbers[problem]) if op == '+' else math.prod(columnar_numbers[problem])
    answers.append(acc)

print('The sum of all answers to columnar-read problems is ' + str(sum(answers)) + '.')