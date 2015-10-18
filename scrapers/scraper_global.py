#!/usr/bin/python

import re

punct = ['?','.','!']

user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'

# Used to remove URLs and parse text into separate sentences
def parse_sentences(text):
    text = text.split()
    
    sentences = []
    new_sentence = "@#$ $#@"
    for word in text:
        if not re.search("(http://)?([A-z0-9]+\.){1,}[A-z]{2,4}/", word) and not isinstance(word, unicode):
            new_sentence += " " + word
        else:
            continue

        # Mark the end of a sentence
        if new_sentence[-1] in punct or (new_sentence[-2] in punct and new_sentence[-1] in ['"',"'"]):
            # Get rid of imbalanced quotes
            if new_sentence.count("'") % 2 or new_sentence.count('"') % 2:
                new_sentence = new_sentence.replace("'","")
                new_sentence = new_sentence.replace('"',"")
            new_sentence += " #$%"
            if len(new_sentence.split()) > 4:
                sentences.append(new_sentence)
            new_sentence = "@#$ $#@"

    if new_sentence != "@#$ $#@":
        new_sentence += " #$%"
        if len(new_sentence.split()) > 4:
            sentences.append(new_sentence)

    return sentences
