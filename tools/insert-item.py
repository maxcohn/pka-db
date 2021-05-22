# Insert a new episode, guest, or event into the database
#
# Usage: insert-item.py insert_type db_path

import sqlite3
import sys
import os

insert_type = sys.argv[1].lower()
db_path = sys.argv[2]

conn = None
try:
    conn = sqlite3.connect(db_path)
except:
    print('Failed to connect to databse. Check given path.')
    os.exit(1)

cur = conn.cursor()

PKA_ID = 1
PKN_ID = 2

if insert_type == 'episode':
    show = PKA_ID if input('Show (PKA or PKN): ').lower().strip() == 'pka' else PKN_ID
    ep_num = int(input('Episode number: '))
    yt_link = input('YouTube link (after v=): ').strip()
    runtime = int(input('Runtime (in seconds): '))
    airdate = input('Airdate (YYYY-MM-DD): ').strip()

    # insert episode into the database
    cur.execute('''
    insert into episodes (show, episode, airdate, runtime, yt_link)
    values (?, ?, ?, ?, ?)
    ''', (show, ep_num, airdate, runtime, yt_link))

    if show == PKA_ID:
        guest_ids = []
        if input('Were all hosts on?').strip().lower()[0] == 'y':
            guest_ids += [1,2,4]
        
        guest_ids += list(map(int, input('Enter space separated guest IDs: ').strip().split()))

        # insert the guests into the database
        for id in guest_ids:
            cur.execute('''
            insert into appearances (guest_id, show, episode)
            values (?, 1, ?)
            ''', (id, ep_num))
    
elif insert_type == 'guest':
    name = input('What is the guest\'s name? ').strip()
    cur.execute('insert into guests (name) values (?)', (name,))
    cur.execute('select max(guest_id) from guests')
    new_id = cur.fetchone()
    print(f'New guest id = {new_id}')
else:
    print('Invalid insert type, check arguments.')
    os.exit(1)

conn.commit()