from flask import Flask, render_template, request, g
from . import db
import sqlite3
import os
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "main.db")
#DATABASE_PATH = 'main.db'

# get database from context
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
    return db

# destroy database
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/pka/<episode>')
def get_pka_epsiode(episode):
    '''Page consisting of list of guests present on the episode and a list of
    events from that episode.

    :param episode: Episode number
    '''
    cur = get_db()
    guest_list = db.all_episode_guests(cur, 'pka', episode)
    cur.close()

    return '\n'.join(map(lambda x: f'<li>{x[1]}</li>', guest_list))


@app.route('/guests/id/<guest_id>')
def guest(guest_id: int):

    cur = get_db().cursur()
    
    #TODO finish this page
    render_template('guests.html')

#TODO change this to a search
@app.route('/guest/name/<guest_name>')
def get_guest_by_name(guest_name):
    cur = get_db().cursor()
    guest_list = db.all_guest_appearances_by_name(cur, guest_name)
    cur.close()
    return '\n'.join(map(lambda x: f'<li>{x[1]}</li>', guest_list))


if __name__ == '__main__':
    app.run()