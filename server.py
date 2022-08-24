from datetime import timedelta
from flask import Flask, render_template, request, redirect, session, url_for
import random
from flask_socketio import SocketIO, join_room, leave_room, disconnect
import logging
from classes.game import Game
# from engineio.payload import Payload

# configs
# Payload.max_decode_packets = 50
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vlkjnflajhbfl1232#'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
# logging.getLogger('werkzeug').disabled = True  # disabling logs
# app.logger.disabled = True
socketio = SocketIO(app, cors_allowed_origins='*')
my_game = None
next_guest_num = 100
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)


def send_number(column, num):
    socketio.emit('new_command', {'column': column, 'number': num}, namespace='/game')


@app.before_request
def before_request():
    """ Sets up the session for a guest """
    global next_guest_num
    print(session)
    print('username' not in session)
    if 'username' not in session:
        session['username'] = "Guest" + str(next_guest_num)
        session.permanent = True
        next_guest_num += 1


@app.route('/', methods=['POST', 'GET'])
def index():
    print("from index: " + session['username'])
    return render_template('index.html')


@socketio.on('request_current_username', namespace='/index')
def print_current_username():
    print(session['username'])


@socketio.on('change_username', namespace='/index')
def change_username(json):
    username = json.get('username', session['username'])
    print(f"got username change request: {session['username']} to {username}")
    session.pop('username', None)
    session['username'] = username
    socketio.emit('username_changed', {'username': username}, namespace='/index')
    print(session['username'])
    print(session)


@app.route('/game', methods=['POST', 'GET'])
def game():
    print("from game: " + session['username'])
    return render_template('game.html')


@socketio.on('connect_to_game', namespace='/game')
def connect_to_game():
    global my_game
    my_game = Game(request.sid, request.sid, socketio)


@socketio.on('request_reset', namespace='/game')
def game_reset():
    global my_game
    my_game.reset()
    my_game = Game(request.sid, request.sid, socketio)


@socketio.on('become_a_player', namespace='/game')
def become_a_player(json):
    global my_game
    player = json.get('player', 1)
    if my_game:
        my_game.add_player(player, request.sid)


@socketio.on('chose_column', namespace='/game')
def got_number(json):
    global my_game
    col = json.get('column', 1)
    board = json.get('board', 1)
    print(f"got: {col}")
    if my_game:
        my_game.add_dice(board, col, request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)
