from flask import Flask, render_template, request, g, redirect, url_for
from . import db
from . import utils
import sqlite3
import os
app = Flask(__name__)

#TODO have full db path laoded from .env
# get current path and then up one to the database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(os.path.join(BASE_DIR, '..'), "main.db")

#===============================================================================
# Routes
#===============================================================================

@app.route('/', methods=['GET'])
def home():
    return render_template('base.html')

@app.route('/about', methods=['GET'])
def about():
    #TODO add doc comment
    return render_template('about.html')

@app.route('/new-event', methods=['GET', 'POST'])
def new_event():
    #TODO add doc comment
    if request.method == 'GET':
        return render_template('new-event.html')

    
    show = request.json['show']
    episode = request.json['episode']
    timestamp = request.json['timestamp']
    description = request.json['description']

    #TODO abstract this
    cur = get_db().cursor()
    cur.execute('''
    insert into pending_events
    (show, episode, timestamp, description)
    values (?,?,?,?)
    ''', (utils.get_show_id(show), episode, timestamp, description))
    cur.close()
    get_db().commit()
    return ('', 201)

@app.route('/admin', methods=['GET','POST'])
def admin():
    #TODO have this loaded from .env
    #TODO clean this entire thing
    username = request.args.get('username')
    password = request.args.get('password')

    if username != 'test_user' or password != 'test_pass':
        return ('', 401)
    
    if request.method == 'GET':
        cur = get_db().cursor()
        pending_events = db.all_pending_events(cur)
        cur.close()
        return render_template('admin.html', pending_events=pending_events)

    
    event_id = request.json['id']
    cur = get_db().cursor()
    cur.execute('''
    insert into events
    (show, episode, timestamp, description)
    select show, episode, timestamp, description from pending_events
    where event_id = ?
    ''', (event_id,))
    cur.execute('delete from pending_events where event_id = ?', (event_id,))
    get_db().commit()
    cur.close()
    
    return ('RAD', 401)

@app.route('/guest/id/<guest_id>', methods=['GET'])
def get_guest(guest_id: int):
    cur = get_db().cursor()
    
    # get list of dicts of episode appearances
    tmp_appearances = db.all_guest_appearances_by_id(cur, guest_id)
    appearance_list = [{'show_name': 'PKA' if x[0] == 1 else 'PKN','episode': x[1]} for x in tmp_appearances]
    
    # get total runtime and convert to a nicer format
    total_runtime = db.total_guest_runtime(cur, guest_id)

    hours, minutes, seconds = utils.sec_to_parts(total_runtime)

    runtime_str = f'{hours} hours, {minutes} minutes, and {seconds} seconds'

    # get the guest's name    
    guest_name = db.guest_name_by_id(cur, guest_id)

    cur.close()

    return render_template(
        'guest.html', 
        appearance_list=appearance_list, 
        runtime=runtime_str,
        guest_name=guest_name    
    )

@app.route('/event/id/<event_id>', methods=['GET'])
def get_event(event_id: int):
    cur = get_db().cursor()
    event = db.get_event_by_id(cur, event_id)
    yt_link = db.get_yt_link(cur, event['show'], event['episode'])
    cur.close()

    return render_template('event.html', event=event, yt_link=yt_link)

@app.route('/guest/search/<search_str>', methods=['GET'])
def guest_search(search_str: str):
    cur = get_db().cursor()
    all_results = db.guest_name_search(cur, search_str)
    cur.close()

    if len(all_results) == 1:
        return redirect(url_for('get_guest', guest_id=all_results[0]['id']))
    
    return render_template('guest-search.html', search_str=search_str, guest_list=all_results)

@app.route('/event/search/<search_str>', methods=['GET'])
def event_search(search_str: str):
    cur = get_db().cursor()
    all_results = db.event_search(cur, search_str)
    cur.close()

    #if len(all_results) == 1:
    #    return redirect(url_for('get_event', event_id=all_results[0]['id']))

    return render_template('event-search.html', search_str=search_str, event_list=all_results)

@app.route('/<show>/<int:episode>', methods=['GET'])
def get_pka_epsiode(show: str, episode):
    '''Page consisting of list of guests present on the episode and a list of
    events from that episode.

    Args:
        episode (int): Episode number
    '''
    show = show.lower()
    if show not in ('pka', 'pkn'):
        return 'BAD' #TODO change this

    cur = get_db().cursor()

    # get the list of quests on this episode
    guest_list = db.all_episode_guests(cur, show, episode)
    guest_list = [{'id': x[0], 'name': x[1]} for x in guest_list]

    # get the youtube link if applicable
    yt_link = db.get_yt_link(cur, show, episode)
    
    cur.close()

    return render_template(
        'episode.html',
        show_name=show.upper(),
        episode=episode,
        guest_list=guest_list,
        yt_link=yt_link
    )

#===============================================================================
# Misc functions related to routes
#===============================================================================

def get_db():
    '''Get current open database connection'''
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
    return db

@app.teardown_appcontext
def close_connection(exception):
    '''Close the database on a closed connection'''
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':

    app.run()
