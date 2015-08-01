#!/usr/bin/python

from sys import argv
import json, random

def main():
    random.seed() # Seed the random number generator
    
    punct = [".",".",".",".","...","!","?"]

    # Open our markov chain file (json)
    with open("json/"+argv[1]+".json") as json_file:
        lang_data = json.load(json_file)

        sentence = []
        for x in range(random.randint(1,2)):
            word1 = "@#$"
            word2 = "$#@"

            while True:
                word1, word2 = word2, random.choice(lang_data[word1+" "+word2])
                if word2 == "#$%":
                    break
                sentence.append(word2)
            if sentence[-1][-1] not in punct:
                sentence[-1] = sentence[-1] + random.choice(punct)

        print ' '.join(sentence)

if __name__ == "__main__":
    main()
