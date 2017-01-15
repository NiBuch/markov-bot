#!/usr/bin/python

from scraper_global import parse_sentences, punct, user_agent
from sys import argv
import random, re, urllib2, time

with open("raw_text/4chan_"+argv[1]+".raw", "w") as out_file:

    # Setup the connection
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', user_agent)]
    crawled = set([])
    threads = set([])

    for page in range(1,10):
        if page == 1:
            page = ""
#        print "http://boards.4chan.org/"+argv[1]+"/"+str(page)
        mainpage = opener.open("http://boards.4chan.org/"+argv[1]+"/"+str(page)).read()
        threads = threads.union(set(re.findall('/'+argv[1]+'(/thread/[0-9]+)', mainpage)))
        time.sleep(5)


    for thread in threads:
        if thread in crawled:
            continue

        try:        
            threadpage = opener.open("http://boards.4chan.org/"+argv[1]+"/"+ thread).read()
        except urllib2.HTTPError, err:
            print "\n***\thttp://boards.4chan.org/"+argv[1]+"/"+ thread + ":\t"+str(err.code) + "\n"
            crawled.add(thread)
            continue

        text = re.findall('"quotelink">&gt;&gt;[0-9]+</a><br>(?!<blockquote>)([^<]+)</blockquote>', threadpage)

        for line in text:
            if "only visible to 4chan gold members" in line:
                continue
            line = re.sub("([\n\r()]+)","",line)
            line = line.replace("&#039;","'")
            line = line.replace("&quot;",'"')

            if " " in line: # Weed out small posts/replies that won't work with our chain
                for sentence in parse_sentences(line):
                    print sentence
                    out_file.write(sentence + "\n")

        crawled.add(thread)
        time.sleep(5)
