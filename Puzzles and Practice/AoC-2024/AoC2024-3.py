# Lorxus's solution for Advent of Code 2024, Puzzle 3

# Part 1:
# Cleans the provided file, looking only for substrings of the form "mul(m,n)" - no spaces, where m and n are digit strings.
# Returns the sum of the specified multiplications as the solution.

import re

FILENAME = "input3.txt"  # contains the provided nx2 list of location IDs

rawfile = open(FILENAME, 'r')
file = []
for line in rawfile:
    file.append(line)
    # print(line)
print('Reading file...')

pattern = re.compile('(?:mul)[(]\d+,\d+[)]')
# match a left paren, then the group 'mul', then one or more digits, then a comma, then one or more digits, then a right paren
# note the necessary use of a noncapturing group!

numpattern = re.compile('\d+')

mults = []
for entry in file:
    mults = mults + pattern.findall(entry)


total = 0
for mult in mults:
    factors = numpattern.findall(mult)
    # print(factors)
    product = int(factors[0]) * int(factors[1])
    total += product
    # print(product)

print('Part 1 solution!')
print('The total of the multiplications is:', total)

no_try_pattern = re.compile('(?:do\(\))|(?:don\'t\(\))|(?:mul)[(]\d+,\d+[)]')
shall_we_mults = []
for entry in file:
    shall_we_mults = shall_we_mults + no_try_pattern.findall(entry)

shalltot = 0
shall_flag = True
for entry in shall_we_mults:
    if entry == 'do()':
        shall_flag = True
    elif entry == 'don\'t()':
        shall_flag = False
    elif shall_flag:
        factors = numpattern.findall(entry)
        product = int(factors[0]) * int(factors[1])
        shalltot += product

print('Part 2 solution!')
print('The total of the multiplications as modulated by do() and don\'t() is:', shalltot)