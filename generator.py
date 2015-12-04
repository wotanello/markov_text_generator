# usage: generator.py <number of words in output file> [<output file=generated_text.txt> [<input database file=database>]]
# reads file named "database"
# writes to "generated_text"

import os
import sys
import re
import json
import collections
import random
import numpy
import cPickle as pickle

def MAIN(argv):
    iterations = int(argv[1])
    input_file = "database" if len(argv) < 4 else argv[3]
    output_file = "generated_text.txt" if len(argv) < 3 else argv[2]

    print "Reading database from file..."
    with open(input_file, 'rb') as f:
        MAX_WORDS = pickle.load(f)
        numbers_by_words  = pickle.load(f)
        words_couples = pickle.load(f)
        database_compressed = pickle.load(f)
        paragraphs = pickle.load(f)

    numbers_by_words["..."] = len(numbers_by_words)

    words_by_numbers = {}
    for x, y in numbers_by_words.items():
        words_by_numbers[y] = x

    database = {}

    print "Unpacking database..."

    for key in database_compressed:
        array = []
        for element in database_compressed[key]:
            array.append(element)
        database[key] = array

    word_first = numbers_by_words["-"]
    word_second = numbers_by_words["-"]

    paragraph_length = 0 if len(paragraphs) == 0 else paragraphs[random.randrange(0, len(paragraphs))]

    terminal_symbols = [numbers_by_words[z] for z in ['.', '!', '?', '...']]
    punctuation = [numbers_by_words[z] for z in [',', ':', ';']]

    print "Generating..."

    title = True
    space = False

    with open(output_file, 'w+') as f:
        for i in xrange(iterations):
            key = word_first + word_second * MAX_WORDS
            if key in words_couples:
                word_first = word_second
                number = random.randrange(0, words_couples[key])
                word_second = database[key][number]
            else:
                word_first = word_second
                word_second = numbers_by_words["..."]

            if word_second not in terminal_symbols:
                if space and word_second not in punctuation:
                    f.write(" ")
                space = True
                if title:
                    f.write(words_by_numbers[word_second].title())
                else:
                    f.write(words_by_numbers[word_second])
                if word_second != '"':  
                    title = False
            else:
                f.write(words_by_numbers[word_second])
                space = True
                title = True
                word_first = numbers_by_words["-"]
                word_second = numbers_by_words["-"]
                paragraph_length -= 1
                if paragraph_length <= 0:
                    f.write("\n")
                    space = False
                paragraph_length = 0 if len(paragraphs) == 0 else paragraphs[random.randrange(0, len(paragraphs))]
    print "Done!"


if __name__ == "__main__":
    MAIN(sys.argv)
