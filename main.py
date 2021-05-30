"""
Websocket API
"""
from threading import Lock
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit, disconnect

from database_client import sqlite


ASYNC_MODE = None
app = Flask(__name__)
socket_ = SocketIO(app, async_mode=ASYNC_MODE)
THREAD = None
thread_lock = Lock()


@app.route('/')
def index():
    """ Rendering index """
    return render_template('index.html', async_mode=socket_.async_mode)


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
    conn = sqlite.create_connection()
    sqlite.save(conn, message)
    disconnect()


if __name__ == '__main__':
    socket_.run(app, debug=True)
