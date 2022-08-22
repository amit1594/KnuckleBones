from flask import Flask, render_template, request, redirect, session, url_for
import random
from flask_socketio import SocketIO, join_room, leave_room, disconnect
import logging
from game import Game
from column import Column
# from engineio.payload import Payload

# configs
# Payload.max_decode_packets = 50
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
logging.getLogger('werkzeug').disabled = True  # disabling logs
# app.logger.disabled = True
socketio = SocketIO(app)
my_game = None


def send_number(column, num):
    socketio.emit('new_command', {'column': column, 'number': num}, namespace='/game')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game', methods=['POST', 'GET'])
def game():
    return render_template('game.html')


@socketio.on('connect_to_game', namespace='/game')
def connect_to_game():
    global my_game
    my_game = Game(request.sid, request.sid, socketio)


@socketio.on('chose_column', namespace='/game')
def got_number(json):
    global my_game
    col = json.get('column', 1)
    board = json.get('board', 1)
    print(f"got: {col}")
    if my_game:
        my_game.add_dice(board, col, request.sid)


@socketio.on('disconnect')
def lobby_disconnect():
    pass


if __name__ == '__main__':
    socketio.run(app, debug=True)
