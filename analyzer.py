# usage: analyzer.py [<directory=corpus/> [<output database file=database>]]

import os
import sys
import re
import json
import collections
import cPickle as pickle

def ProcessFile(filename, words_unique, database, paragraphs, MAX_WORDS):
    text = ''.join(open(filename).readlines())
    terminals = re.sub(r'([^\?!\n.])', r'', text)
    terminals = re.sub(r'([\?!])', r'.', terminals)
    
    current = 0
    for i in terminals:
        if i == "\n":
            paragraphs.append(current)
            current = 0
        else:
            current += 1

    words_unique["-"] = 0
    
    text = re.sub(r'([\n])', r' ', text)
    text = re.sub(r'([\?!\n.])', r' \1 @ ', text)
    text = re.sub(r'([,:;-])', r' \1 ', text)
    sentences = text.split('@')
    counter = 0
    for sentence in sentences:
        sentence_refined = re.sub(r'[^\w\.,-:?!; \n]+', '', sentence)
        sentence_refined = re.sub(r'[ ]+', ' ', sentence_refined).strip()
        words = sentence_refined.lower().split(" ")

        for i in xrange(len(words)):
            if words[i] not in words_unique:
                word_id = len(words_unique)
                words_unique[words[i]] = word_id
            else:
                word_id = words_unique[words[i]]
            value = word_id
            if i == 0:
                key = words_unique["-"] * (MAX_WORDS + 1)
            elif i == 1:
                key = words_unique["-"] + words_unique[words[i - 1]] * MAX_WORDS
            else:
                key = words_unique[words[i - 2]] + words_unique[words[i - 1]] * MAX_WORDS
            if key not in database:
                database[key] = []
            database[key].append(value)


def MAIN(argv):
    output_file = "database" if len(argv) < 3 else argv[2]
    walk_dir = "corpus/" if len(argv) < 2 else argv[1]
    words_unique = {}
    database = {}
    paragraphs = []
    MAX_WORDS = 1000000

    for root, subdirs, files in os.walk(walk_dir):
        for file in files:
            path = root + "/" + file
            print "Processing file: " + path
            ProcessFile(path, words_unique, database, paragraphs, MAX_WORDS)


    words_couples = {}

    print "Counting..."

    counters = {}
    
    for key in database:
        words_couples[key] = len(database[key])
        counters[key] = collections.Counter(database[key])

    print "Writing database to file..."
    with open(output_file, 'wb') as f:
        pickle.dump(MAX_WORDS, f, 1)
        pickle.dump(words_unique, f, 1)
        pickle.dump(words_couples, f, 1)
        pickle.dump(database, f, 1)
        pickle.dump(paragraphs, f, 1)

    print "Done!"

if __name__ == "__main__":
    MAIN(sys.argv)
