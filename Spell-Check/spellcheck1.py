import re, collections, sys
from misspell import Misspell
# re - Python Library for Regular Expressions
# collections - Python Library for High Performance Container Datatypes

# Spell Check program using algorithm originally
# summarized by Dr. Peter Norvig.
#     src: http://norvig.com/spell-correct.html
#     additional src: http://goo.gl/uaJ6DQ (Google)

# The algorithm used has 3 parts:
#     -The probability of the typed word being correctly typed by the user
#     -The offset probability of the user typing word, x, but initially meant word, y
#     -Iteration of all possible outputs, and choosing a word which has the best probability

class SpellCheck:

    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, path):
        self.dictPath = path

    # Returning the words in a list as lower case and defining a word as a list of alphabetic character
    # Works because the singular version of a word is more probably than the possessive notation (dog, dog's)
    def words(self, text):
        return re.findall('[a-z0-9]+', text.lower())

    #Returning dictionary = {'a':{abbey:1, abbreviated:2}, 'b':{},...,'z':{}}
    #Instead of iterating through the whole dictionary, iteration happens based on first letter
    def train(self, words):
        occurences = collections.defaultdict(lambda: 1)
        # for l in self.alphabet:
        #     occurences[l] = collections.defaultdict(lambda: 1) #Sets default values in a dictionary, less iteration to check if element is a part of the dictionary

        for w in words:
            occurences[w] += 1 #Incrementing occurence of word
        return occurences

    #Edits can be deletion (deletes), swapping adajent letters (transposes), alteration (replaces), or inserting a letter (inserts)
    #Returns a set of of all words one edit away from correct word
    def edits1(self, word):
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces = [a + c + b[1:] for a, b in splits for c in self.alphabet if b]
        inserts = [a + c + b     for a, b in splits for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)

    #Returns a set of words with the possible edits
    def known_edits2(self, word, wDict):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in wDict)

    def known_edits3(self, word, wDict):
        return set(e3 for e1 in self.edits1(word) for e2 in self.edits1(e1) for e3 in self.edits1(e2) if e3 in wDict)

    #A known word is most likely to be a word that has a vowel mistyped rather than 2 consonants, probable correct first letter, edit distances of around 1 or 2
    def known(self, word, wDict):
        return set(w for w in word if w in wDict)

    class ProbabilityAssigner:

        def __init__(self, wDict, word):
            self.wDict = wDict
            self.word = word

        def returnProbability(self, candidate):
            if candidate[0] == self.word[0]:
                sameFirstLetter = 1
            else:
                sameFirstLetter = 0
            return (sameFirstLetter, self.wDict.get(candidate))

    # Highest Level Method
    # Returns the possible word
    def correct(self, word, wDict):
        candidates = self.known([word], wDict) or self.known(self.edits1(word), wDict) or self.known_edits2(word, wDict) or [word] # gets a set of words with the shortest edit distance from the typed word.
        print candidates
        pa = self.ProbabilityAssigner(wDict, word)
        return sorted(candidates, key=pa.returnProbability, reverse = True)[:3] # returning the element of the set with the highest probability of being the correct word

    def run(self, option):
        lWords = self.words(file(self.dictPath).read())
        try:
            if option == '0':
                lWords = self.train(lWords)
                while True:
                    word = raw_input('>')
                    # if not word.isalpha():
                    #     continue
                    spellchk = self.correct(word.lower(), lWords)
                    if spellchk == word and spellchk not in lWords:
                        print 'NO SUGGESTION'
                    else:
                        print spellchk
                    print #'\n'
            elif option == '1':
                misspell = Misspell(lWords)
                lWords = self.train(lWords)
                while True:
                    word = misspell.genWord()
                    print 'Incorrect -', word
                    spellchk = self.correct(word, lWords)
                    if spellchk == word and spellchk not in lWords:
                        print 'NO SUGGESTION'
                    else:
                        print 'Correct   -',spellchk
                    print #'\n'
                    raw_input('<enter>\n') #Enter to continue
        except KeyboardInterrupt:
            #Cleaner way to exit program without a crash
            'exit'
        except EOFError:
            'exit'