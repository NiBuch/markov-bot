#!/usr/bin/python

####
## Credit to @tonyfischetti. His code is the basis for much of this
##      http://www.onthelambda.com/2014/02/20/how-to-fake-a-sophisticated-knowledge-of-wine-with-markov-chains/
####

from sys import argv
import json, re

# Function to create trigrams from our input
def trigram(words):
    if len(words) < 3:
        return

    for n in xrange(len(words) - 2):
        yield (words[n], words[n+1], words[n+2])


def main():
    start1 = "@#$"
    start2 = "$#@"
    
    # Open our json file to load in old data (for updates)
    with open("json/"+argv[1]+".json") as json_file:
        json_data = json_file.read()
        try:
            lang_data = json.loads(json_data)
        except ValueError:
            lang_data = {}

    # Open our raw text files to process
    with open("raw_text/"+argv[1]+".raw") as raw_file:
        for line in raw_file:
            words = line.split()
            for word1, word2, word3 in trigram(words):
                digram = word1 + " " + word2
                if digram in lang_data:
                    lang_data[digram].append(word3)
                else:
                    lang_data[digram] = [word3]

    # Write our chain to a json file
    with open("json/"+argv[1]+".json", "w") as json_file:
        json.dump(lang_data, json_file)

if __name__ == "__main__":
    main()
