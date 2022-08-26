from classes.board import Board
import random


def generate_dice():
    return random.randint(1, 6)


class Game:
    def __init__(self, p1_sid, p2_sid, socket):
        self.p1_board = Board()
        self.p2_board = Board()
        self.curr_player = random.randint(1, 2)
        self.curr_dice = generate_dice()
        self.socket = socket
        self.p1_sid = p1_sid
        self.p2_sid = p2_sid
        self.socket.emit('update_turn', {"player": self.curr_player, "dice": self.curr_dice,
                                         "p1sum": self.p1_board.get_sum(), "p2sum": self.p2_board.get_sum()},
                         namespace="/game")

    def get_other_player(self):
        if self.curr_player == 1:
            return 2
        return 1

    def get_curr_player_sid(self):
        if self.curr_player == 1:
            return self.p1_sid
        return self.p2_sid

    def get_other_player_sid(self):
        if self.curr_player == 1:
            return self.p2_sid
        return self.p1_sid

    def get_curr_board(self):
        if self.curr_player == 1:
            return self.p1_board
        else:
            return self.p2_board

    def get_other_board(self):
        if self.curr_player == 1:
            return self.p2_board
        else:
            return self.p1_board

    def check_win(self):
        if self.p1_board.get_count() == 9 or self.p2_board.get_count() == 9:
            p1_sum = self.p1_board.get_sum()
            p2_sum = self.p2_board.get_sum()
            if p1_sum > p2_sum:
                winning_text = f"Player 1 won with {p1_sum}:{p2_sum}"
            else:
                winning_text = f"Player 2 won with {p2_sum}:{p1_sum}"
            self.socket.emit('winning_message', {'text': winning_text}, namespace="/game")
            self.send_chat_message('win', winning_text)

    def send_update_turn(self):
        self.socket.emit('update_turn', {"player": self.curr_player, "dice": self.curr_dice,
                                         "p1sum": self.p1_board.get_sum(), "p2sum": self.p2_board.get_sum()},
                         namespace="/game")

    def add_dice(self, board_index, col, sid):
        if sid != self.get_curr_player_sid() or board_index != self.curr_player:
            return
        curr_board = self.get_curr_board()
        if not curr_board.add_dice(col, self.curr_dice):
            return
        my_json = {"column_index": col, "play": True}
        updated_col = curr_board.get_col(col)
        my_json["index1"] = self.curr_player
        my_json["column1"] = updated_col.get_dices()
        my_json["sum1"] = updated_col.get_sum()
        # swap turn
        if self.curr_player == 1:
            self.curr_player = 2
        else:
            self.curr_player = 1
        curr_board = self.get_curr_board()
        # remove matching dice from enemy's col
        curr_board.remove_dice(col, self.curr_dice)
        updated_col = curr_board.get_col(col)
        my_json["index2"] = self.curr_player
        my_json["column2"] = updated_col.get_dices()
        my_json["sum2"] = updated_col.get_sum()
        self.socket.emit('update_column', my_json, namespace="/game")
        # generate new dice
        self.curr_dice = generate_dice()
        self.send_update_turn()
        self.check_win()

    def send_chat_message(self, msg_type, msg):
        self.socket.emit('new_chat_message', {"type": msg_type, "msg":  msg}, namespace="/game")

    def reset(self):
        self.socket.emit('reset_game', namespace="/game")

    def add_player(self, player, sid):
        print(player, type(player))
        if player == 1 and sid != self.p1_sid:
            self.p1_sid = sid
            self.send_current_boards(sid)
            self.send_chat_message('player_join', "player1 joined")
        elif player == 2 and sid != self.p2_sid:
            self.send_current_boards(sid)
            self.p2_sid = sid
            self.send_chat_message('player_join', "player2 joined")

    def send_current_boards(self, sid):
        self.send_update_turn()
        p1cols = self.p1_board.get_columns()
        p2cols = self.p2_board.get_columns()
        for i in range(3):
            my_json = {"column_index": i + 1, "index1": 1, "index2": 2, "column1": p1cols[i].get_dices(), "play": False,
                       "sum1": p1cols[i].get_sum(), "column2": p2cols[i].get_dices(), "sum2": p2cols[i].get_sum()}
            self.socket.emit('update_column', my_json, room=sid, namespace="/game")

    def process_chat_message(self, sid, msg):
        if sid == self.p1_sid:
            sender = "Player 1: "
        elif sid == self.p2_sid:
            sender = "Player 2: "
        else:
            sender = "Spectator: "
        self.send_chat_message('regular', sender + msg)
