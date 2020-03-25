'''
Gets the most recent episode of PKA via the YouTube API and adds it to the database

Note: This script does not add guests to the page (due to inconsistent naming of episodes)
To add a guest, use the query:
    insert into appearances (show, episode, guest_id) values (?,?,?)
or use the admin page that I hopefully build at this point


Usage:
    python <this-script> DB_PATH YT_API_KEY SENDGRID_API_KEY USER_EMAIL

Cron Job to run this with:
    0 17 * * 6 docker exec >/dev/null 2>&1

    (every saturday at 5pm, no output)
'''


import requests
import json
import re
from datetime import datetime
import sys
import sqlite3

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

DB_PATH = sys.argv[1]
YT_API_KEY = sys.argv[2]
SENDGRID_API_KEY = sys.argv[3]
USER_EMAIL = sys.argv[4]

LINE_RE = re.compile(r'^((\d+):\d+:\d+)\s*(-\s*)?(.*)$')
WOODYS_CHANNEL_ID = 'UCIPVJoHb_A5S3kcv3TJlyEg'


def time_to_sec(time: str):
    '''Convert a string of format hh:mm:ss to a number of seconds'''
    split_time = time.split(':')

    hour, minute, second = (0, 0, 0)

    if len(split_time) == 2:
        minute, second = tuple(map(lambda x: int(x), split_time))
    elif len(split_time) == 3:
        hour, minute, second = tuple(map(lambda x: int(x), split_time))
    else:
        raise Exception()

    return (hour * 60 * 60) + (minute * 60) + second

# get id of newest PKA
resp_json = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={WOODYS_CHANNEL_ID}&maxResults=1&order=date&key={YT_API_KEY}').json()

title = resp_json['items'][0]['snippet']['title']
yt_link = resp_json['items'][0]['id']['videoId']

# get video details
resp_json = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails&id={yt_link}&key={YT_API_KEY}').json()

description = resp_json['items'][0]['snippet']['description']
runtime = resp_json['items'][0]['contentDetails']['duration']

# parse episode
episode = int(re.search(r'^PKA (\d+)', title).group(1))

# get total runtime for the episode
hours, mins, secs = map(int, re.search(r'PT(\d+)H(\d+)M(\d+)S', runtime).groups())
total_secs = hours * 60 * 60 + mins * 60 + secs


conn = sqlite3.connect(DB_PATH)

# insert episode into database
conn.execute('''
insert into episodes (show, episode, airdate, runtime, yt_link)
values (1, ?, ?, ?, ?)
''', (episode, datetime.today().strftime('%Y-%m-%d'), total_secs, yt_link))

conn.commit()

# enter guests into episode

# assume woody, kyle, and taylor are there
guests = [1,2,4]

for g in guests:
    conn.execute('''
    insert into appearances (guest_id, show, episode)
    values (?, 1, ?)
    ''', (g, episode))

conn.commit()

# enter timeline events into database
for line in description.split('\n'):
    m = LINE_RE.search(line)
    if m is not None:
        secs = time_to_sec(m.group(1))
        event_desc = m.group(4)
        if secs == 0:
            continue
        elif 'calls it a show' in event_desc.lower():
            continue

        conn.execute('''
        insert into events (show, episode, timestamp, description) values (?,?,?,?)
        ''', (1, episode, secs, event_desc))
        conn.commit()

# close db connection
conn.close()

print(description)
print((episode, datetime.today().strftime('%Y-%m-%d'), total_secs, yt_link))

# send an email to me
sg = SendGridAPIClient(SENDGRID_API_KEY)
resp=sg.send(Mail(
    from_email='automation-alerts@pka-db.com',
    to_emails=USER_EMAIL,
    subject=f'PKA {episode} added to pka-db.com',
    plain_text_content=f'''PKA {episode}

        Airtime: {total_secs}
        Video Id: {yt_link}

        Added to database
    '''
))
