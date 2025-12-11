# This program takes in a series of dial turns of the form "(L/R) ##", e.g. L69, R22.
# The dial starts pointed at 50, and goes from 0 to 99.

FILENAME = "input1-2025.txt"  # contains the provided ordering rules and update batches

with open(FILENAME, 'r') as rawfile:
    rawarray = rawfile.read().splitlines()

dialarray = []

for entry in rawarray:
    direction = entry[0]
    full_distance = int(entry[1:])
    dialarray.append([direction, full_distance])

truespin = []
fullspin = []

for pair in dialarray:
    distance = pair[1] % 100 # the dial is of size 100 total; we can ignore any wraparound (at least for Part 1)
    if pair[0] == 'L':
        fullspin.append(-1 * pair[1])
        truespin.append(-1 * distance)
    else:
        fullspin.append(pair[1])
        truespin.append(distance)

# Part 1: The program outputs a list of all numbers the dial points to in between, as well as the number of times it points at 0, which is the password.

dial_ptr = 50
zero_count = 0
print(dial_ptr, zero_count)
for number in truespin:
    dial_ptr += number
    dial_ptr %= 100  # the dial is a circle
    if dial_ptr == 0:
        zero_count += 1
    # print(dial_ptr, zero_count)
print('\nThe final dial position is ' + str(dial_ptr) +', with total number of zeroes ' + str(zero_count) + '.')

# Part 2: The program no longer outputs a list of dial positions, and keeps track of every time the dial passes zero for the password count, not just when the dial ends up on zero. Note that some of the entries have spin numbers well over 100!

dial_ptr = 50
zero_pass = 0
for number in fullspin:
    # print(number, abs(number//100), abs(number)//100)
    zero_pass += abs(number) // 100 # exactly one additional zero-pass per full spin
    net_spin = number % 100 # now what about the partial spins?
    sgn = number/abs(number)
    if sgn < 0:
        net_spin -= 100
    # print(number, abs(number)//100, net_spin)
    print(dial_ptr, dial_ptr + net_spin, dial_ptr >= 100 or dial_ptr <= 0)
    dial_ptr += net_spin
    if dial_ptr != net_spin and (dial_ptr >= 100 or dial_ptr <= 0): # did we overflow? did we underflow? 
        zero_pass += 1
    dial_ptr %= 100 # reduce
print('\nThe final dial position is ' + str(dial_ptr) +', with total number of zero-passes ' + str(zero_pass) + '.')