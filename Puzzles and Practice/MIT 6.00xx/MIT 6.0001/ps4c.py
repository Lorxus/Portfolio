# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|:;'<>?,./\\\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words4.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
        pass #delete this line and replace with your code here
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        valid_words = self.valid_words.copy() 
        return valid_words
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        tpose_dict = {}
        
        for i in range(26):
            if string.ascii_lowercase[i] in CONSONANTS_LOWER:
                tpose_dict[string.ascii_lowercase[i]] = string.ascii_lowercase[i]
                tpose_dict[string.ascii_uppercase[i]] = string.ascii_uppercase[i]
            else:
                # print(vowels_permutation[VOWELS_LOWER.index(string.ascii_lowercase[i])])
                tpose_dict[string.ascii_lowercase[i]] = vowels_permutation[VOWELS_LOWER.index(string.ascii_lowercase[i])]
                tpose_dict[string.ascii_uppercase[i]] = vowels_permutation[VOWELS_LOWER.index(string.ascii_lowercase[i])].upper()
        # print(tpose_dict)
        return tpose_dict
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        
        tpose_dict = self.build_transpose_dict(transpose_dict)
        mytxt = self.get_message_text()
        ciphertxt = ''

        for char in mytxt:
            # print(char)
            if char.isalpha():
                ciphertxt += tpose_dict[char]
            else:
                ciphertxt += char
        
        return ciphertxt
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        valid_word_count = {}  # we'll use the max over this later - this time we need a dict
        vowelperms = get_permutations(VOWELS_LOWER)
        for p in vowelperms:
            count_good_words = 0
            decodedtxt_list = self.apply_transpose(p).split()  # turn the message into a list of words. some of them will end in punctuation and we will deal with that later.

            for word in decodedtxt_list:
                if is_word(self.get_valid_words(), word):
                    count_good_words += 1
            
            valid_word_count[p] = count_good_words

        bestperm = max(valid_word_count, key=valid_word_count.get)
        cleartext = self.apply_transpose(bestperm)
        return (bestperm, cleartext) 
    

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    # enc_dict = message.build_transpose_dict(permutation)

    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(permutation))

    enc_message = EncryptedSubMessage(message.apply_transpose(permutation))
    print("Decrypted message:", enc_message.decrypt_message())

    permutation = 'uiaeo'
    msg = SubMessage('never gonna give you up')
    print("Original message:", msg.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "nivir gennu gavi yeo op")
    print("Actual encryption:", msg.apply_transpose(permutation))

    enc_msg = EncryptedSubMessage(msg.apply_transpose(permutation))
    print("Decrypted message:", enc_msg.decrypt_message())

    permutation = 'uoiea'
    msg2 = SubMessage('Never, gonna? give: you! up;')
    print("Original message:", msg2.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", 'Novor, gennu? givo: yea! ap;')
    print("Actual encryption:", msg2.apply_transpose(permutation))

    enc_msg2 = EncryptedSubMessage(msg2.apply_transpose(permutation)) # gonna is not a word in word4 so this should not be inverse
    print("Decrypted message:", enc_msg2.decrypt_message())
    

