"""DB interaction"""

import sqlite3
from typing import Tuple, List

#TODO figure out how to add 136.5


def all_episode_events(cur: sqlite3.Cursor, show: str, ep_num: int) -> List[Tuple[int, str]]:

    show = show.lower()
    show_id = 0
    if show == 'pka':
        show_id = 1
    elif show == 'pkn':
        show_id = 2
    else:
        #TODO specify exception
        raise Exception()


    return cur.execute('''select timestamp, description from events where show = ? and episode = ?;''', (show_id, ep_num)).fetchall()

def all_episode_guests(cur: sqlite3.Cursor, show: str, ep_num: int) -> List[Tuple[int, str]]:
    show = show.lower()
    show_id = 0
    if show == 'pka':
        show_id = 1
    elif show == 'pkn':
        show_id = 2
    else:
        #TODO specify exception
        raise Exception()
    
    return cur.execute('''
    select guest_id, name from guests
    where guest_id in (
        select guest_id from appearances
        where appearances.show = ? and appearances.episode = ?
    );
    ''', (show_id, ep_num)).fetchall()


#TODO use cur
def all_guest_appearances_by_id(guest_id: int) -> List[Tuple[int, int]]:
    conn = sqlite3.connect('main.db')

    return conn.execute('''select show, episode from appearances
    where appearances.guest_id in (
	    select guest_id from guests
	    where guests.guest_id = ?
    )''', (guest_id,))

def all_guest_appearances_by_name(cur: sqlite3.Cursor, guest_name: str) -> List[Tuple[int, int]]:
    '''Get each apperance (show_id, episode_num) of all guests that match `guest_name`

    :param cur: Database cursor

    :param guest_name: Guest name to search in the database
    '''
    guest_name = f'%{guest_name}%'

    return cur.execute('''select show, episode from appearances
    where appearances.guest_id in (
	    select guest_id from guests
	    where guests.name like ?
    )
    order by episode asc''', (guest_name,)).fetchall()

#print(2 + 2)
#print(all_guest_appearances_by_name(sqlite3.connect('main.db').cursor(), 'Awz'))
