# This program takes in a block of text representing a tachyon beam splitting array and does something regarding predicting the splits.

FILENAME = "input7-2025.txt"  # contains the provided ordering rules and update batches

with open(FILENAME, 'r') as rawfile:
    rawarray = rawfile.read().splitlines()

# Part 1: The program outputs the number of times the beam is split.

beam_source = rawarray[0].index('S')
splits = 0
beam_locations = [beam_source]
temp_beams = []

for row_idx in range(len(rawarray)):
    for beam in beam_locations:
        if rawarray[row_idx][beam] == '^':
            splits += 1
            temp_beams.append(beam - 1)
            temp_beams.append(beam + 1)
        else:
            temp_beams.append(beam)
    
    beam_locations = temp_beams
    temp_beams = []
    
    beam_locations = list(set(beam_locations)) # dedupe

print('The tachyon beam will split ' + str(splits) + ' times.')

# Part 2: As Part 1, but now we count the number of possible timelines, i.e., the number of possible paths that the tachyon beam might have taken.

splits = 0
beam_counts = [0] * len(rawarray[0])
beam_counts[beam_source] = 1  # doing it pascal-style
temp_beam_counts = [0] * len(rawarray[0])

for row_idx in range(len(rawarray)):
    for col_idx in range(len(beam_counts)):
        if beam_counts[col_idx] == 0:
            continue
        elif rawarray[row_idx][col_idx] == '^':
            temp_beam_counts[col_idx - 1] += beam_counts[col_idx]
            temp_beam_counts[col_idx + 1] += beam_counts[col_idx]
        else:
            temp_beam_counts[col_idx] += beam_counts[col_idx]
    beam_counts = temp_beam_counts
    temp_beam_counts = [0] * len(rawarray[0])


print('The tachyon beam instantiates ' + str(sum(beam_counts)) + ' timelines.') 