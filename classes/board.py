from classes.column import Column


class Board:
    def __init__(self):
        self.left_col = Column()
        self.mid_col = Column()
        self.right_col = Column()

    def get_col(self, col_index):
        if col_index == "1" or col_index == 1:
            col = self.left_col
        elif col_index == "2" or col_index == 2:
            col = self.mid_col
        elif col_index == "3" or col_index == 3:
            col = self.right_col
        else:
            col = None
        return col

    def add_dice(self, my_column, value):
        col = self.get_col(my_column)
        if not col:
            return False
        if col.get_count() < 3:
            col.add_dice(value)
            print("here2")
            return True
        print("here3")
        return False

    def remove_dice(self, my_column, value):
        col = self.get_col(my_column)
        if not col:
            return False
        col.remove_dice(value)

    def get_count(self):
        return self.left_col.get_count() + self.mid_col.get_count() + self.right_col.get_count()

    def get_sum(self):
        return self.left_col.get_sum() + self.mid_col.get_sum() + self.right_col.get_sum()

    def get_columns(self):
        return [self.left_col, self.mid_col, self.right_col]

    def send_current_state(self, board_index, socketio, sid):
        cols = [self.left_col, self.mid_col, self.right_col]
        count = 0
        for col in cols:
            count += 1
            my_json = {"board_index": board_index, "column_index": count,
                       "dices": col.get_dices(), "sum": col.get_sum()}
            socketio.emit('update_column', my_json, room=sid, namespace="/game")
