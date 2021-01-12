import re
from os import path
from typing import Tuple, Set

# regex for matching timestring with hours, minutes, and seconds being in capture groups
_TIME_RE = re.compile(r'(\d+):(\d+):(\d+)')

def sec_to_timestr(total_seconds: int) -> str:
    '''Convert a number of seconds to a string of format HH:MM:SS

    Args:
        total_seconds (int): Total seconds

    Returns:
        str: Time string of format HH:MM:SS
    '''
    hours, minutes, seconds = sec_to_parts(total_seconds)    

    return f'{hours:02}:{minutes:02}:{seconds:02}'

def sec_to_parts(total_seconds: int) -> Tuple[int, int, int]:
    '''Convert a number of seconds to a tuple of its parts (hours, minutes, seconds)

    Args:
        total_seconds (int): Total seconds

    Returns:
        Tuple[int, int, int]: Tuple of format (hours, minutes, seconds)
    '''
    seconds = total_seconds % 60
    total_seconds = total_seconds // 60
    minutes = total_seconds % 60
    hours = total_seconds // 60

    return (hours, minutes, seconds)

def timestr_to_sec(time: str) -> int:
    '''Convert a time string to the total number of seconds for the time it represents

    Args:
        time (str): Time string of format HH:MM:SS

    Return:
        int: Total seconds

    '''
    match = _TIME_RE.match(time.strip())
    
    if match is None:
        return ''
    
    hours, minutes, seconds = map(int, match.groups())

    return (hours * 60 * 60) + (minutes * 60) + seconds

def get_show_id(show_name: str) -> int:
    '''Get show id from a string representation

    Args:
        show_name (str): String representation of show name (e.g. 'pka' or 'pkn')

    Returns:
        int: Show id in the database
    '''
    show_name = show_name.strip().lower()
    if show_name == 'pka':
        return 1
    elif show_name == 'pkn':
        return 2
    else:
        raise Exception(f'Invalid show identifier: "{show_name}"')

def load_blacklist(blacklist_path: str) -> Set[str]:
    '''Load the blacklist as a set of strings

    Args:
        blacklist_path (str): Path to the blacklist
    Returns:
        Set[str]: Set of blacklisted words. Is empty if the blacklist didn't exist
    '''
    if not path.exists(blacklist_path):
        return set()

    with open(blacklist_path) as f:
        return set(f.read().split('\n'))
