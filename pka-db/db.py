"""DB interaction"""

import sqlite3
from typing import Tuple, List

#TODO figure out how to add 136.5

def _get_conn() -> sqlite3.Connection:
    return sqlite3.connect('main.db')

def all_episode_events(show: str, ep_num: int):

    conn = sqlite3.connect('main.db')

    show = show.lower()
    show_id = 0
    if show == 'pka':
        show_id = 1
    elif show == 'pkn':
        show_id = 2
    else:
        #TODO specify exception
        raise Exception()


    return conn.execute('''select timestamp, description from events where show = ? and episode = ?;''', (show_id, ep_num))

def all_episode_guests(cur: sqlite3.Cursor, show: str, ep_num: int) -> Tuple[int, str]:
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
    select person_id, name from people
    where person_id in (
        select person_id from appearance
        where appearance.show = ? and appearance.episode = ?
    );
    ''', (show_id, ep_num)).fetchall()


def all_guest_appearances_by_id(guest_id: int) -> List[Tuple[int, int]]:
    conn = sqlite3.connect('main.db')

    return conn.execute('''select show, episode from appearance
    where appearance.person_id in (
	    select person_id from people
	    where people.person_id = ?
    )''', (guest_id,))

def all_guest_appearance_by_name(cur: sqlite3.Cursor, guest_name: str) -> List[Tuple[int, int]]:
    guest_name = f'%{guest_name}%'

    return cur.execute('''select show, episode from appearance
    where appearance.person_id in (
	    select person_id from people
	    where people.name like ?
    )
    order by episode asc''', (guest_name,)).fetchall()

#print(2 + 2)
#print(all_guest_appearance_by_name(sqlite3.connect('main.db').cursor(), 'Awz'))