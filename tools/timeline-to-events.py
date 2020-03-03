# converts a youtube timeline to a series of event table records
#NOTE: this script isn't ready to run, it's kind of a mess. if you're going to use it
# look at it and make the necessary adjustments beforehand


import re
import sys
import requests
import sqlite3
import json

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

LINE_RE = re.compile(r'^((\d+):\d+:\d+)\s*(-\s*)?(.*)$')

API_KEY = sys.argv[1]

conn = sqlite3.connect('main.db')
cur = conn.cursor()

for i in range(226,480 + 1):
    print(f'EPISODE: {i}')
    print(f'EPISODE: {i}', file=sys.stderr)
    try:
        video_id = cur.execute('select yt_link from episodes where show = 1 and episode = ?', (i,)).fetchone()[0]
        #print(video_id)
        j = requests.get(f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={API_KEY}&part=snippet').json()
        #print(j)
        description = j['items'][0]['snippet']['description']

        for line in description.split('\n'):
            m = LINE_RE.search(line)
            if m is not None:
                print(f'{time_to_sec(m.group(1))} - {m.group(4)}')
                #print(f'event name: {m.group(4)}')
    except:
        continue


    
'''
timeline = [x.strip() for x in timeline] 






for line in timeline.split('\n'):
    if line.strip() == '':
        continue

    m = LINE_RE.search(line)

    if m is None:
        continue

    time = m.group(1)
    description = m.group(3).split()

    print(time_to_sec(time))
    print(description)

    #TODO manual review or auto add to db?
'''