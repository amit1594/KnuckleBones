class Column:
    def __init__(self):
        self.dices = []
        self.count = 0

    def add_dice(self, value):
        if len(self.dices) < 3:
            self.dices.append(value)

    def remove_dice(self, value):
        count = 0
        while value in self.dices:
            count += 1
            self.dices.remove(value)
        print("removed: ", count)

    def get_count(self):
        return len(self.dices)

    def get_sum(self):
        my_sum = 0
        dice_dict = dict()
        for dice in self.dices:
            if dice in dice_dict.keys():
                dice_dict[dice] += 1
            else:
                dice_dict[dice] = 1
        for val, count in dice_dict.items():
            if count == 1:
                my_sum += val
            elif count == 2:
                my_sum += val * 4
            elif count == 3:
                my_sum += val * 9
        return my_sum

    def get_dices(self):
        my_dict = dict()
        for i in range(len(self.dices)):
            my_dict[i + 1] = self.dices[i]
        return my_dict