#!/usr/bin/python

import re
import random
import sqlite3
import sys
import requests
import os

# These mappings can get fairly large -- they're stored globally to
# save copying time.

# (tuple of words) -> {dict: word -> number of times the word appears following the tuple}
# Example entry:
#    ('eyes', 'turned') => {'to': 2.0, 'from': 1.0}
# Used briefly while first constructing the normalized mapping
tempMapping = {}

# (tuple of words) -> {dict: word -> *normalized* number of times the word appears following the tuple}
# Example entry:
#    ('eyes', 'turned') => {'to': 0.66666666, 'from': 0.33333333}
mapping = {}

# Contains the set of words that can start sentences
starts = []

# We want to be able to compare words independent of their capitalization.
def fixCaps(word):
    # Ex: "FOO" -> "foo"
    if word.isupper() and word != "I":
        word = word.lower()
        # Ex: "LaTeX" => "Latex"
    elif word [0].isupper():
        word = word.lower().capitalize()
        # Ex: "wOOt" -> "woot"
    else:
        word = word.lower()
    return word

# Tuples can be hashed; lists can't.  We need hashable values for dict keys.
# This looks like a hack (and it is, a little) but in practice it doesn't
# affect processing time too negatively.
def toHashKey(lst):
    return tuple(lst)

def wordlistFromDB(id):
    wordlist = []
    conn = sqlite3.connect("group.db")
    c = conn.cursor()
    for row in c.execute("SELECT * FROM messages WHERE sender_id = " + str(id)):
        if row[1] is not None:
            tokens = row[1].split(" ")
            size = 0
            for token in tokens:
                size += 1
                if token.endswith(("!", "?", ".")):
                    punct = token[len(token) - 1]
                    token = token[:-1]
                    wordlist.append(token)
                    wordlist.append(punct)
                else:
                    wordlist.append(token)
                    if size == len(tokens):
                        wordlist.append(".")

            # if row[1] is not None:
            #     if not row[1].endswith("!") and not row[1].endswith("?") and not row[1].endswith("."):
            #         text = row[1] + ".\n"
            #         string += text
    return wordlist


# Returns the contents of the file, split into a list of words and
# (some) punctuation.
def wordlist(filename):
    # wordlist = []
    f = open(filename, 'r')
    wordlist = [fixCaps(w) for w in re.findall(r"[\w']+|[.,!?;]", f.read())]
    f.close()
    return wordlist

# Self-explanatory -- adds "word" to the "tempMapping" dict under "history".
# tempMapping (and mapping) both match each word to a list of possible next
# words.
# Given history = ["the", "rain", "in"] and word = "Spain", we add "Spain" to
# the entries for ["the", "rain", "in"], ["rain", "in"], and ["in"].
def addItemToTempMapping(history, word):
    global tempMapping
    while len(history) > 0:
        first = toHashKey(history)
        if first in tempMapping:
            if word in tempMapping[first]:
                tempMapping[first][word] += 1.0
            else:
                tempMapping[first][word] = 1.0
        else:
            tempMapping[first] = {}
            tempMapping[first][word] = 1.0
        history = history[1:]

# Building and normalizing the mapping.
def buildMapping(wordlist, markovLength):
    global tempMapping
    starts.append(wordlist [0])
    for i in range(1, len(wordlist) - 1):
        if i <= markovLength:
            history = wordlist[: i + 1]
        else:
            history = wordlist[i - markovLength + 1 : i + 1]
        follow = wordlist[i + 1]
        # if the last elt was a period, add the next word to the start list
        if history[-1] == "." and follow not in ".,!?;":
            starts.append(follow)
        addItemToTempMapping(history, follow)
    # Normalize the values in tempMapping, put them into mapping
    for first, followset in tempMapping.iteritems():
        total = sum(followset.values())
        # Normalizing here:
        mapping[first] = dict([(k, v / total) for k, v in followset.iteritems()])

# Returns the next word in the sentence (chosen randomly),
# given the previous ones.
def next(prevList):
    sum = 0.0
    retval = ""
    index = random.random()
    # Shorten prevList until it's in mapping
    while toHashKey(prevList) not in mapping:
        prevList.pop(0)
    # Get a random word from the mapping, given prevList
    for k, v in mapping[toHashKey(prevList)].iteritems():
        sum += v
        if sum >= index and retval == "":
            retval = k
    return retval

def genSentence(markovLength):
    # Start with a random "starting word"
    curr = random.choice(starts)
    sent = curr.capitalize()
    prevList = [curr]
    # Keep adding words until we hit a period
    while (curr not in "."):
        curr = next(prevList)
        prevList.append(curr)
        # if the prevList has gotten too long, trim it
        if len(prevList) > markovLength:
            prevList.pop(0)
        if (curr not in ".,!?;"):
            sent += " " # Add spaces between words (but not punctuation)
        sent += curr
    return sent

def main():

    id = sys.argv[1]
    markovLength = 2

		print(os.listdir())
		print(str(id))

    buildMapping(wordlistFromDB(id), markovLength)

    # buildMapping(wordlist(filename), markovLength)
    first = genSentence(markovLength)
    second = ""
    if len(first) < 20:
        second = genSentence(markovLength)
    text =  first + " " + second
		print(text)
    payload = {'bot_id':'', 'text':text}
    r = requests.post('https://api.groupme.com/v3/bots/post', params=payload)
		print(r.text)
		sys.stdout.flush()

if __name__ == "__main__":
    main()
