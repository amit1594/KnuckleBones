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
