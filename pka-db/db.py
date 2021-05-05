'''DB interaction'''
import sqlite3
from typing import Tuple, List, Dict
import random
from . import utils

#TODO figure out how to add 136.5
#solution: episode numbers stored as strings instead. do this at some point



#===============================================================================
# Episode related
#===============================================================================
def get_yt_link(cur: sqlite3.Cursor, show: str, ep_num: int) -> str:
    '''Get YouTube link for a given episode

    Args:
        cur (Cursor): DB cursor.
        show (str): Show name.
        ep_num (int): Episode number.

    Returns:
        str: YouTube link following the `v` query param (e.g.`www.youtube.com/watch?v=`).
    '''
    show_id = utils.get_show_id(show)

    return cur.execute('''
    select yt_link from episodes
    where show = ? and episode = ?
    ''', (show_id, ep_num)).fetchone()[0]

#===============================================================================
# Guest related
#===============================================================================
def all_episode_guests(cur: sqlite3.Cursor, show: str, ep_num: int) -> List[Tuple[int, str]]:
    '''Gets all guests that were on a given episode

    Args:
        cur (Cursor): DB cursor.
        show (str): Show name.
        ep_num (int): Episode number.

    Returns:
        List[Tuple[int, str]]: List of appearances (tuples) in the format: (show_id, episode_num)
    '''
    show_id = utils.get_show_id(show)
    
    return cur.execute('''
    select guest_id, name from guests
    where guest_id in (
        select guest_id from appearances
        where appearances.show = ? and appearances.episode = ?
    )
    ''', (show_id, ep_num)).fetchall()

def all_guest_appearances_by_id(cur: sqlite3.Cursor, guest_id: int) -> List[Tuple[int, int]]:
    '''Finds all apperances of a given guest id

    Args:
        cur (Cursor): DB cursor
        guest_id (int): Guest id in the DB

    Returns:
        List[Tuple[int, int]]: List of appearances (tuples) in the format: (show_id, episode_num)
    '''
    return cur.execute('''
    select show, episode from appearances
    where appearances.guest_id in (
	    select guest_id from guests
	    where guests.guest_id = ?
    )
    order by episode desc
    ''', (guest_id,))

def guest_name_by_id(cur: sqlite3.Cursor, guest_id: int) -> str:
    '''Get the name of a guest based on their id

    Args:
        cur (Cursor): DB cursor
        guest_id (int): Id of the guest
    
    Returns:
        str: Guest name
    '''
    return cur.execute('''
    select name from guests
    where guest_id = ?
    ''', (guest_id,)).fetchone()[0]

def total_guest_runtime(cur: sqlite3.Cursor, guest_id: int) -> int:
    '''Gets the total runtime (in seconds) for the given guest id

    Args:
        cur (Cursor): DB cursor
        guest_id (int): Id of the guest to check runtime for

    Returns:
        int: Total runtime in seconds
    '''
    pka_runtime = cur.execute('''
    select sum(runtime) from episodes
    where episode in (
        select episode from appearances
        where guest_id = ?
    )
    and show = 1
    ''', (guest_id,)).fetchone()[0]

    pkn_runtime = cur.execute('''
    select sum(runtime) from episodes
    where episode in (
        select episode from appearances
        where guest_id = ?
    )
    and show = 2
    ''', (guest_id,)).fetchone()[0]

    if pka_runtime is None:
        pka_runtime = 0

    if pkn_runtime is None:
        pkn_runtime = 0

    return pka_runtime + pkn_runtime

def guest_name_search(cur: sqlite3.Cursor, search_str: str) -> List[Dict]:
    '''Querys the database for guests who have a name contianing the given string

    Args:
        cur (Cursor): DB cursor
        search_str (str): Search query

    Returns:
        List of dicts with the format:
        {
            id: guest_id
            name: guest_name
        }
    '''

    # add a prefix fts wildcard
    if search_str[-1] != '*':
        search_str = search_str + '*'
    #wildcard_name = f'%{search_str}%'
    #all_results = cur.execute('''
    #select guest_id, name from guests
    #where name like ?
    #''', (wildcard_name,)).fetchall()
    #
    all_results = cur.execute('''
    select guest_id, name from guests_fts
    where name match ? order by rank;
    ''', (search_str,)).fetchall()
    
    return [{'id': res[0], 'name': res[1]} for res in all_results]

#===============================================================================
# Event related
#===============================================================================
def all_episode_events(cur: sqlite3.Cursor, show: str, ep_num: int) -> List[dict]:
    '''Gets all events from a given episode

    Args:
        cur (Cursor): DB cursor.
        show (str): Show name.
        ep_num (int): Episode number.

    Returns:
        List[dict]: List of events
    '''
    show_id = utils.get_show_id(show)
    
    events = cur.execute('''
    select event_id, show, episode, timestamp, description from events
    where show = ? and episode = ?
    ''', (show_id, ep_num)).fetchall()

    return [{
        'id': event[0],
        'show': 'PKA' if event[1] == 1 else 'PKN',
        'episode': event[2],
        'timestamp': utils.sec_to_timestr(event[3]),
        'description': event[4], 
    } for event in events]

def event_search(cur: sqlite3.Cursor, search_str: str) -> List[Dict]:
    '''Querys the database for events that match given string

    Args:
        cur (Cursor): DB cursor
        search_str (str): Search query

    Returns:
        List of dicts with the format:
        {
            id: event_id,
            show: show,
            episode: episode,
            timestamp: timestamp,
            description: description,
        }
    '''

    # perform a prefix fts query
    if search_str[-1] != '*':
        search_str = search_str + '*'

    # it looks like the order of the FTS query is perserved. If that isn't the case for some reason in the future, use something like
    #select event_id, e.description, e.timestamp from events_fts INNER JOIN events e USING (event_id) WHERE events_fts MATCH 'prison' ORDER BY rank;
    all_results = cur.execute('''
    select event_id, show, episode, timestamp, description
    from events
    inner join (
        select event_id
        from events_fts
        where events_fts match ?
        order by rank
    ) using (event_id);
    ''', (search_str,)).fetchall()

    return [{
        'id': res[0],
        'show': 'PKA' if res[1] == 1 else 'PKN',
        'episode': res[2],
        'timestamp': utils.sec_to_timestr(res[3]),
        'description': res[4],
    } for res in all_results]

def get_event_by_id(cur: sqlite3.Cursor, event_id: int) -> Dict:
    '''Get an event based on its id

    Args:
        cur (Cursor): Database cursor
        event_id: Id of event

    Returns:
        dict: Dict representing an event
    '''
    event = cur.execute('''
    select event_id, show, episode, timestamp, description from events
    where event_id = ?
    ''', (event_id,)).fetchone()

    return {
        'id': event[0],
        'show': 'PKA' if event[1] == 1 else 'PKN',
        'episode': event[2],
        'timestamp': utils.sec_to_timestr(event[3]),
        'description': event[4], 
    }

def random_events(cur: sqlite3.Cursor, num_events: int) -> List[dict]:
    '''Get `num_events` events randomly from the database

    Args:
        cur (Cursor): Database cursor
        event_id: Number of events to select randomly

    Returns:
        dict: List of dicts representing an event
    '''
    max_event = cur.execute('select count(*) from events').fetchone()[0]

    # get a series of random events
    event_ids = []
    for _ in range(num_events):
        eid = random.randint(0, max_event)
        while eid in event_ids:
            eid = random.randint(0, max_event)

        event_ids.append(eid)

    # construct a select statement with an arbitrary amount of '?' placeholders
    # to allow us search for a sequence. This doesn't allow SQL injection because
    # still use placeholders
    events = cur.execute(f'''
    select event_id, show, episode, timestamp, description from events
    where event_id in ({','.join(['?' for _ in range(num_events)])})
    ''', event_ids).fetchall()

    return [{
        'id': event[0],
        'show': 'PKA' if event[1] == 1 else 'PKN',
        'episode': event[2],
        'timestamp': utils.sec_to_timestr(event[3]),
        'description': event[4], 
    } for event in events]
    
#===============================================================================
# Admin related
#===============================================================================
