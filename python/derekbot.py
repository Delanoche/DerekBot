import json
import sqlite3
import time
import re
import urllib2

if __name__ == "__main__":

    base_url = "https://api.groupme.com/v3"
    group_id = ""
    token = ""
    limit = "&limit=100"
    before = "&before_id="
    endpoint = "/groups/" + group_id + "/messages"

    group_url = base_url + "/groups/" + group_id + token

    last_id = ""

    url = base_url + endpoint + token + limit + before
    print(url)

    conn = sqlite3.connect("group.db")
    c = conn.cursor()
    c.execute("CREATE TABLE people(id INTEGER PRIMARY KEY, nickname TEXT)")
    c.execute("CREATE TABLE messages(id INTEGER PRIMARY KEY, text TEXT, sender_id INTEGER)")
    conn.commit()

    response = urllib2.urlopen(group_url)
    html = response.read()
    json_response = json.loads(html)
    response = json_response['response']
    members = response['members']
    for member in members:
        user_id = member['user_id']
        nickname = member['nickname']
        c.execute("INSERT INTO people(id, nickname) VALUES (?,?)", (user_id, nickname))

    response = urllib2.urlopen(url)
    html = response.read()
    json_response = json.loads(html)

    response = json_response['response']
    messages = response['messages']

    message_id = ""
    hasMessages = True

    size = 0

    while hasMessages:
        for message in messages:
            message_id = message['id']
            text = message['text']
            sender_id = message['sender_id']
            c.execute("INSERT INTO messages(id, text, sender_id) VALUES (?,?,?)", (message_id, text, sender_id))
            size += 1
        conn.commit()
        before = "&before_id=" + message_id
        print(message_id)
        print("Size: " + str(size))
        url = base_url + endpoint + token + limit + before
        print(url)
        response = urllib2.urlopen(url)
        html = response.read()
        json_response = json.loads(html)
        response = json_response['response']
        messages = response['messages']
        time.sleep(0.5)
        if len(json_response) == 0:
            hasMessages = False
