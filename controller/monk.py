"""
Websocket API
"""
import json
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
from flask_restful import Api

from database import sqlite

async_mode = None
app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
api = Api(app)


@app.route('/')
def index():
    return render_template("index.html", async_mode=socket_.async_mode)


@app.route('/monk/<monk>')
def get(monk):
    """ Return the monk data"""
    r = sqlite.get(monk)
    monks = {
        "key": r[0],
        "value": r[1],
    }
    return render_template("monk.html", data=monks, async_mode=socket_.async_mode)


@socket_.on('connection', namespace='/websocket')
def test_message(message):
    """ test message receive"""
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socket_.on('save', namespace='/websocket')
def save_message(message):
    """
    save message received
    """
    sqlite.save(message)
    return render_template('success.html', async_mode=socket_.async_mode)


