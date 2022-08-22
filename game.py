from column import Column
from board import Board
import random


def generate_dice():
    return random.randint(1, 6)


class Game:
    def __init__(self, p1_sid, p2_sid, socket):
        self.p1_board = Board()
        self.p2_board = Board()
        self.curr_player = 1
        self.curr_dice = generate_dice()
        self.socket = socket
        self.p1_sid = p1_sid
        self.p2_sid = p2_sid
        self.socket.emit('update_turn', {"player": self.curr_player, "dice": self.curr_dice}, namespace="/game")

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

    def add_dice(self, board_index, col, sid):
        if sid != self.get_curr_player_sid() or board_index != self.curr_player:
            return
        curr_board = self.get_curr_board()
        if not curr_board.add_dice(col, self.curr_dice):
            return
        updated_col = curr_board.get_col(col)
        my_json = {"board_index": self.curr_player, "column_index": col,
                   "dices": updated_col.get_dices(), "sum": updated_col.get_sum()}
        self.socket.emit('update_column', my_json, namespace="/game")
        # swap turn
        if self.curr_player == 1:
            self.curr_player = 2
        else:
            self.curr_player = 1
        curr_board = self.get_curr_board()
        # remove matching dice from enemy's col
        curr_board.remove_dice(col, self.curr_dice)
        updated_col = curr_board.get_col(col)
        my_json = {"board_index": self.curr_player, "column_index": col,
                   "dices": updated_col.get_dices(), "sum": updated_col.get_sum()}
        self.socket.emit('update_column', my_json, namespace="/game")
        # generate new dice
        self.curr_dice = generate_dice()
        self.socket.emit('update_turn', {"player": self.curr_player, "dice": self.curr_dice}, namespace="/game")
        self.check_win()


