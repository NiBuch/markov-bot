#!/usr/bin/python

import json, random, re, socket, string, ssl, time, urllib, urllib2

#### Server config ####        
server = "XXXXXXXX"
password = "XXXXXXXX"
channel = "#channel"
botnick = "ArbitraryCode"
#######################

## Markov chains ##
chains = ["~4chan_b","~4chan_pol","~4chan_r9k","~4chan_v","~pornhub"]

## Bot Commands ##
commands = ["~urban"]

# Deal with IRC Ping/Pong transactions
def ping(pingmsg):
    ircsock.send("PONG %s\r\n" % pingmsg[5:])

# Send messages to channel
def sendmsg(chan , msg):
    # Deal with unicode shenanigans
    msg = msg.encode('utf-8')

    # Break up long messages
    while len(msg) > 350:
            ircsock.send("PRIVMSG "+ chan + " :"+msg[:msg.index(" ",350)]+"\r\n")
            print "<--","PRIVMSG "+ chan + " :"+msg[:msg.index(" ",350)]
            msg = msg[msg.index(" ",350):]
    ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\r\n") 
    print "<--","PRIVMSG "+ chan +" :"+ msg

# Join a channel
def joinchan(chan):
    print "<--", ("JOIN %s" % chan)
    ircsock.send("JOIN %s\r\n" % chan)

# Send "Hello!"
def hello():
    print "<--","PRIVMSG "+ channel +" :ayy lmao"
    ircsock.send("PRIVMSG "+ channel +" :ayy lmao")

# Load language data or change data set
def load_lang_data(dataset):
    random.seed() # reseed the RNG
    punct = [".",".",".",".","...","!","?"] # Makes periods more probable than other expressions
    with open("json/"+dataset+".json") as json_file:
        chain_data = json.load(json_file)

    return chain_data, punct

# Picks words from a dictionary of word-probability pairs
def choose_word(probs):
    x = random.uniform(0,1)*sum(probs.values())
    cumulative_prob = 0
    for word in probs:
        cumulative_prob += probs[word]
        if x < cumulative_prob:
            break

    return word

# Used for generating sentences from a lang_data file
def generate_sentences(dataset, punct, total=0):
    if total:
        lines = range(total)
    else:
        lines = range(random.randint(1,2))

    sentence = []
    for x in lines:
        word1 = "@#$"
        word2 = "$#@"
        while True:
            word1, word2 = word2, choose_word(dataset[word1+" "+word2])
            if word2 == "#$%":
                break
            sentence.append(word2)
        if sentence[-1][-1] not in punct:
            sentence[-1] = sentence[-1] + random.choice(punct)
    
    return ' '.join(sentence).replace(" ,",",")

# Urban Dictionary Lookups
def urban(search_term):

    print search_term
    # In case we're passed a list
    search_term = " ".join(search_term)
    
    # Make our request
    request = urllib2.Request("http://api.urbandictionary.com/v0/define?term="+search_term.replace(" ","+"))
    request.add_header("User-agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36")
    results = urllib2.urlopen(request)

    # Check results, then parse down to a single, random one
    results = json.load(results)
    if results["result_type"] == "no_results":
        return "Result not found"

    else:
        results = results["list"]
        results = random.choice(results)["definition"]
        results = re.sub("[[\]]","",results)
        results = re.sub("[\n\r]+"," ",results)
        return search_term + ": " + results

###=============================###

# Establish our connection
ircsock = ssl.wrap_socket(socket.socket())
ircsock.connect((server, 16697))
ircsock.send("PASS %s\r\n" % password)
ircsock.send("NICK %s\r\n" % botnick)
ircsock.send("USER %s %s %s :ArbitraryCode Markov Bot\r\n" % (botnick, botnick, botnick)) # user authentication

cur_lang = 0
lang_data = 0

# Placeholder for the last received message
lastmsg = "Do they speak English in what?"

while 1:

    # Receive and parse out the latest message
    ircmsg = ircsock.recv(2048)
    ircmsg = string.rstrip(ircmsg)
    user = ircmsg.split("!")[0][1:]

    if (ircmsg[0:4] != "PING") and ircmsg:
        print "-->",ircmsg

    # Wait for MOTD to end before joining a channel
    if "MODE" in ircmsg and botnick in ircmsg:
        joinchan(channel)

    # Process commands
    if ircmsg.find(":~") != -1:
        ircmsg = ircmsg.split()
        command = ircmsg[3][1:]
        print "--> ~Command~:", command

        if command == "~help":
            sendmsg(channel, "Available Markov chains: "+", ".join(chains))
            sendmsg(channel, "Availabe commands: " + ", ".join(commands))
            continue
        elif command == "~urban":
            sendmsg(channel, user + ", " + "".join(urban(ircmsg[4:])))
            continue

        # Make sure the user picks a usable makrov chain
        if command not in chains:
        #    sendmsg(channel, user+", not a valid command")
            continue
        # If we haven't loaded a chain yet, or if we need to load a new one
        elif (not lang_data) or (cur_lang != command[1:]):
            command = command[1:]
            lang_data, punc = load_lang_data(command)
            cur_lang = command

        sendmsg(channel, user+": "+generate_sentences(lang_data, punc))
        continue

    # Print hello if someone says hi to the bot
    if ircmsg.find(":Hello "+ botnick) != -1:
        hello()
        continue

### Canned responses ###

    # Capitalizes on the lols
    if ircmsg.find(":LOL") != -1:
        sendmsg(channel, user+" capitalizes on the lols")
        continue

    # THE BEST THE BEST
    if re.search("t+h+e+ b+e+s+t+",ircmsg,re.IGNORECASE) and ircmsg.find(botnick) == -1:
        thebest = "THE BEST"
        for k in range(random.randint(5,19)):
            thebest += " THE BEST"
        sendmsg(channel, thebest)

    # What? Can't hear you
    if re.search(":(lol)?w+h*[auo]+t+\?*$",ircmsg,re.IGNORECASE) and ircmsg.find(botnick) == -1:
        try:
            sendmsg(channel, lastmsg.upper())
        except UnicodeDecodeError:
            sendmsg(channel, random.choice(["WHAT AIN'T NO COUNTRY I NEVER HEARD OF","DO THEY SPEAK ENGLISH IN WHAT?","SAY 'WHAT' ONE MORE GODDAMN TIME"]))

### Connection Functions ###

    # Pong back the server
    if ircmsg.find("PING :") != -1:
        ping(ircmsg)
        continue
    
    # In case of a disconnect
    if "ERROR :Closing Link: ArbitraryCode" in ircmsg:
        ircsock = ssl.wrap_socket(socket.socket())
        ircsock.connect((server, 16697))
        ircsock.send("PASS %s\r\n" % password)
        ircsock.send("NICK %s\r\n" % botnick)
        ircsock.send("USER %s %s %s :ArbitraryCode Markov Bot\r\n" % (botnick, botnick, botnick)) # user authentication
        continue

### Message tracking and cleanup ###
    lastmsg = " ".join(ircmsg.split()[3:])[1:]
