# converts a youtube timeline to a series of event table records

import re


filename = ''
with open(filename) as f:
    timeline = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
timeline = [x.strip() for x in timeline] 


def time_to_sec(time: str):
    split_time = time.split(':')

    hour, minute, second = (0, 0, 0)

    if len(split_time) == 2:
        minute, second = tuple(map(lambda x: int(x), split_time))
    elif len(split_time) == 3:
        hour, minute, second = tuple(map(lambda x: int(x), split_time))
    else:
        print(f'Invalid time: {time}')

    return (hour * 60 * 60) + (minute * 60) + second


LINE_RE = re.compile(r'^((\d+)?:\d+:\d+)\s*(.*)$')

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
