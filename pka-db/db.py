'''DB interaction'''
import sqlite3
from typing import Tuple, List, Dict
from . import utils

#TODO figure out how to add 136.5



#===============================================================================
# Episode related
#===============================================================================

def all_episode_events(cur: sqlite3.Cursor, show: str, ep_num: int) -> List[Tuple[int, str]]:
    '''Get all events for a given episode

    Args:
        cur (Cursor): DB cursor.
        show (str): Show name.
        ep_num (int): Episode number.

    Returns:
        List[Tuple[int,str]]: List of events (tuples) in the format: (timestamp, event_description).
    '''
    show_id = utils.get_show_id(show)

    return cur.execute('''
    select timestamp, description from events
    where show = ? and episode = ?
    ''', (show_id, ep_num)).fetchall()

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
    wildcard_name = f'%{search_str}%'
    all_results = cur.execute('''
    select guest_id, name from guests
    where name like ?
    ''', (wildcard_name,)).fetchall()

    return [{'id': res[0], 'name': res[1]} for res in all_results]

#===============================================================================
# Event related
#===============================================================================
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
    wildcard_name = f'%{search_str}%'
    all_results = cur.execute('''
    select event_id, show, episode, timestamp, description from events
    where description like ?
    ''', (wildcard_name,)).fetchall()

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
        'timestamp': event[3],
        'description': event[4], 
    }

def add_event(conn: sqlite3.Connection, show: str, episode: int, timestamp: int, description: str):
    '''Adds an event to the database, in a pending state

    Args:
        conn (Connection): DB connection
        show (str): Show name ('PKA' or 'PKN')
        episode (int): Episode number
        timestamp (int): Timestamp at which the event occurs (in seconds)
        description (str): Description of the event
    '''
    # create a db cursor
    cur = conn.cursor()

    # add the event to the pending table
    cur.execute('''
    insert into pending_events
    (show, episode, timestamp, description)
    values (?,?,?,?)
    ''', (utils.get_show_id(show), episode, timestamp, description))

    # commit changes and close cursor
    conn.commit()
    cur.close()
    

#===============================================================================
# Admin related
#===============================================================================
def all_pending_events(cur: sqlite3.Cursor) -> List[Dict]:
    '''Gets all events pending admin approval

    Args:
        cur (Cursor): DB cursor
    '''
    # fetch pending events from the database
    all_events = cur.execute('select event_id, show, episode, timestamp, description from pending_events').fetchall()

    #TODO clean this up, this is gross
    return [{
        'id': e[0],
        'show': 'PKA' if e[1] == 1 else 'PKN',
        'episode': e[2],
        'timestamp': e[3],
        'description': e[4],
        'link': f'http://www.youtube.com/watch?v={get_yt_link(cur, "PKA" if e[1] == 1 else "PKN",e[2])}&t={e[3]}'
    } for e in all_events]

def approve_pending_event(conn: sqlite3.Connection, pending_id: int):
    '''Approve a pending event by moving it to the regular events table

    Args:
        conn (Connection): DB connection
        pending_id (int): Id of event in pending_events table to be moved
    '''
    cur = conn.cursor()

    # insert pending event into the events table
    cur.execute('''
    insert into events
    (show, episode, timestamp, description)
    select show, episode, timestamp, description from pending_events
    where event_id = ?''', (pending_id,))

    # remove the pending event from the pending_events table
    cur.execute('delete from pending_events where event_id = ?', (pending_id,))

    # commit to the database to make changes live
    conn.commit()
    cur.close()