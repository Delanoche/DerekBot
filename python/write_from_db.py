import json
import sqlite3
import codecs
import time
import re
import urllib2

if __name__ == "__main__":

    f = codecs.open("eric.txt", 'w+', 'utf-8')
    conn = sqlite3.connect("group.db")
    c = conn.cursor()
    size = 0
    members = []
    for row in c.execute("SELECT * FROM people"):
        members.append((row[0], row[1]))

    for member in members:
        id = member[0]
        name = member[1].replace(":", "")
        f = codecs.open(name + ".txt", 'w+', 'utf-8')

        for row in c.execute("SELECT * FROM messages WHERE sender_id = " + str(id)):
            size += 1
            if row[1] is not None:
                if not row[1].endswith("!") and not row[1].endswith("?") and not row[1].endswith("."):
                    text = row[1] + ".\n"
                    f.write(text)
            print(size)

