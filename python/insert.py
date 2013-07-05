import sys
import sqlite3
__author__ = 'henkec'

def main():
    id = sys.argv[1]
    text = sys.argv[2]
    sender_id = sys.argv[3]

    conn = sqlite3.connect("group.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages(id, text, sender_id) VALUES (?,?,?)", (id, text, sender_id))
    c.close()
    conn.close()
    print(text)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
