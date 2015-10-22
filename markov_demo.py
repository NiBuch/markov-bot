#!/usr/bin/python

from sys import argv
import json, random

# Selects a random word using weighted probabilities
#   Takes a dictionary of words, where the values are their probabilities
#   Ex. {"The":3, "I":4, "While":1}
def choose_word(probs):
    x = random.uniform(0,1)*sum(probs.values())
    cumulative_prob = 0
    for word in probs:
        cumulative_prob += probs[word]
        if x < cumulative_prob:
            break

    return word


def main():
    random.seed() # Seed the random number generator
    
    punct = [".",".",".",".","...","!","?"]

    # Open our markov chain file (json)
    with open("json/"+argv[1]+".json") as json_file:
        lang_data = json.load(json_file)

        sentence = []

        if len(argv) > 2:
            lines = range(int(argv[2]))
        else:
            lines = range(random.randint(1,3))

        for x in lines:
            word1 = "@#$"
            word2 = "$#@"

            while True:
                word1, word2 = word2, choose_word(lang_data[word1+" "+word2])
                if word2 == "#$%":
                    break
                sentence.append(word2)
            if sentence[-1][-1] not in punct:
                sentence[-1] = sentence[-1] + random.choice(punct)

        print ' '.join(sentence).replace(" ,",",")

if __name__ == "__main__":
    main()
