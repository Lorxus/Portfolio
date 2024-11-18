# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    return set(secret_word) <= set(letters_guessed)
    
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''

def get_guessed_word(secret_word, letters_guessed):
    length = len(secret_word)
    display = ['_'] * length

    for i in range(length):
        if secret_word[i] in letters_guessed:
            display[i] = secret_word[i]
    
    temp = ''
    for d in display:
        temp += d
    
    return temp
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''

def get_available_letters(letters_guessed):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for c in letters_guessed:
        if c in alphabet:
            alphabet.remove(c)
    
    temp = ''
    for l in alphabet:
        temp += l
    
    return temp
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    
    

def hangman(secret_word):
    guesses_left = 6
    letters_guessed = []
    print('~~~~~~~~~~~~')
    print('Let\'s play Hangman!', get_guessed_word(secret_word, letters_guessed))
    print('My word is', len(secret_word), 'letters long. You have', guesses_left, 'wrong guesses remaining.')
    
    while not is_word_guessed(secret_word, letters_guessed) and guesses_left > 0:
        print('~~~~~~~~~~~~')
        print('Guess a letter. Your options are:', get_available_letters(letters_guessed))
        print('You have', guesses_left, 'wrong guesses remaining.')
        guessletter = input()
        if not guessletter.isalpha() and len(guessletter) == 1:
            print('That\'s not a letter. You lose your guess. Try again.')
            guesses_left -= 1
            continue
        else:
            guessletter = guessletter.lower()
            if guessletter in letters_guessed:
                print('You\'ve already guessed that! Try again.')
                continue
            else:
                letters_guessed.append(guessletter)
                letters_guessed.sort()
                print('You guessed', guessletter+'.')
                if guessletter in list(secret_word):
                    print('Good guess!', get_guessed_word(secret_word, letters_guessed))
                    if is_word_guessed(secret_word, letters_guessed):
                        print('Yeah, you got it! Good job!')
                        break
                    continue
                else:
                    print('Oh no! That\'s not in my word.', get_guessed_word(secret_word, letters_guessed))
                    guesses_left -= 1
                    
                    continue
    
    print('~~~~~~~~~~~~')
    print('My secret word was', secret_word+'.')
    if not is_word_guessed(secret_word, letters_guessed):
        print('Better luck next time. Maybe try some more common letters?')
        

    
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    if len(my_word) != len(other_word):
      return False
    else:
      return all([(my_word[i] == other_word[i]) or my_word[i] == '_' for i in range(len(my_word))])
    
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''



def show_possible_matches(my_word):
    definitely_guessed = [c for c in my_word if c != '_']
    definitely_guessed.sort()
    gap_list = [idx for idx in range(len(my_word)) if my_word[idx] == '_']
    print(gap_list)
    for word in filter(lambda w: (len(w) == len(my_word)), wordlist):
        gapperparts = [word[c] for c in gap_list]
        overlap = [char for char in gapperparts if char in my_word]
        if match_with_gaps(my_word, word) and not overlap:
            print(word)
    return None
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''



def hangman_with_hints(secret_word):
    
    guesses_left = 6
    letters_guessed = []
    print('~~~~~~~~~~~~')
    print('Let\'s play Hangman!', get_guessed_word(secret_word, letters_guessed))
    print('My word is', len(secret_word), 'letters long. You have', guesses_left, 'wrong guesses remaining.')
    
    while not is_word_guessed(secret_word, letters_guessed) and guesses_left > 0:
        print('~~~~~~~~~~~~')
        print('Guess a letter. Your options are:', get_available_letters(letters_guessed)+', but if you want a hint, guess \'*\'.')
        print('You have', guesses_left, 'wrong guesses remaining.')
        guessletter = input()
        if not guessletter.isalpha() and len(guessletter) == 1:
            if guessletter == '*':
                print('Very well, a hint! And it won\'t even cost you a guess.')
                show_possible_matches(get_guessed_word(secret_word, letters_guessed))
                continue
            else:
              print('That\'s not a letter. You lose your guess. Try again.')
              guesses_left -= 1
              continue
        else:
            guessletter = guessletter.lower()
            if guessletter in letters_guessed:
                print('You\'ve already guessed that! Try again.')
                continue
            else:
                letters_guessed.append(guessletter)
                letters_guessed.sort()
                print('You guessed', guessletter+'.')
                if guessletter in list(secret_word):
                    print('Good guess!', get_guessed_word(secret_word, letters_guessed))
                    if is_word_guessed(secret_word, letters_guessed):
                        print('Yeah, you got it! Good job!')
                        break
                    continue
                else:
                    print('Oh no! That\'s not in my word.', get_guessed_word(secret_word, letters_guessed))
                    guesses_left -= 1
                    
                    continue
    
    print('~~~~~~~~~~~~')
    print('My secret word was', secret_word+'.')
    if not is_word_guessed(secret_word, letters_guessed):
        print('Better luck next time. Maybe try some more common letters?')
    
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
