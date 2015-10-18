#!/usr/bin/python

import re
from scraper_global import parse_sentences, punct
from sys import argv

out_file = open(argv[1]+".raw", "wb")

full_text = ""

with open(argv[1]) as book_file:
    for line in book_file:
        line = line.replace("\n", " ")
        line = line.replace("\r", "")
        line = line.split()

        for word in line:
            skipword = 0
            for letter in word:
                if ord(letter) > 126:
                    skipword = 1
                    break
            if skipword:
                skipword = 0
                continue
            else:
                full_text += " "
                full_text += word

sentences = parse_sentences(full_text)

for line in sentences:
    out_file.write(line + "\n")


out_file.close()
