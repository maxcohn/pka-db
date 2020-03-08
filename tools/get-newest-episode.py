'''
This script is mean to be called on a schedule, probably saturday afternoons, to
ensure the episode is uploaded. This will handled automatically updating the
database with the most recent episodes
'''


import requests
import json
import re
from datetime import datetime
import sys
import sqlite3

DB_PATH = sys.argv[1]
LINE_RE = re.compile(r'^((\d+):\d+:\d+)\s*(-\s*)?(.*)$')
API_KEY = sys.argv[2]
WOODYS_CHANNEL_ID = 'UCIPVJoHb_A5S3kcv3TJlyEg'


def time_to_sec(time: str):
    split_time = time.split(':')

    hour, minute, second = (0, 0, 0)

    if len(split_time) == 2:
        minute, second = tuple(map(lambda x: int(x), split_time))
    elif len(split_time) == 3:
        hour, minute, second = tuple(map(lambda x: int(x), split_time))
    else:
        #print(f'Invalid time: {time}')
        raise Exception()

    return (hour * 60 * 60) + (minute * 60) + second


resp_json = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={WOODYS_CHANNEL_ID}&maxResults=1&order=date&key={API_KEY}').json()

title = resp_json['items'][0]['snippet']['title']
yt_link = resp_json['items'][0]['id']['videoId']

resp_json = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails&id={yt_link}&key={API_KEY}').json()

description = resp_json['items'][0]['snippet']['description']
runtime = resp_json['items'][0]['contentDetails']['duration']

# parse episode
episode = int(re.search(r'^PKA (\d+)', title).group(1))

# get total runtime for the episode
hours, mins, secs = map(int, re.search(r'PT(\d+)H(\d+)M(\d+)S', runtime).groups())
total_secs = hours * 60 * 60 + mins * 60 + secs


# insert episode into database
'''
insert into episodes (show, episode, airdate, runtime, yt_link)
values (1, ?, ?, ?, ?)
''', (episode, datetime.today().strftime('%Y-%m-%d'), total_secs, yt_link)

# enter guests into episode

# assume woody, kyle, and taylor are there
guests = [1,2,4]

for g in guests:
    '''
    insert into appearances (guest_id, show, episode)
    values (?, 1, ?)
    ''', (g, episode)

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

print(description)
print((episode, datetime.today().strftime('%Y-%m-%d'), total_secs, yt_link))