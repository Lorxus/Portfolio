# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    seq_len = len(sequence)
    sequences = []

    if seq_len <= 1:
        return sequence
    else:
        head = sequence[0]
        rest = sequence[1:]

        for i in range(seq_len):
            for s in get_permutations(rest):
                t = s[:i] + head + s[i:]
                sequences.append(t)

    return sequences

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    example_input1 = 'abc'
    print('Input:', example_input1)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input1))

    example_input2 = 'xyz'
    print('Input:', example_input2)
    print('Expected Output:', ['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx'])
    print('Actual Output:', get_permutations(example_input2))

    example_input3 = 'defg'
    print('Input:', example_input3)
    print('Expected Output Properties:', 'Length: 24', 'Duplicates: False')
    g = get_permutations(example_input3)
    print('Actual Output:', 'Length:', len(g), 'Duplicates:', len(set(g)) != len(g))

