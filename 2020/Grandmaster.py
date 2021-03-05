score_table = [-1234567, 8, 6, 5, 5, 4, 4, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1]


class GrandMaster:
    def __init__(self, name, week1, week2, week3=0):
        self.name = name
        self.week1 = week1
        self.week2 = week2
        self.week3 = week3

    def result(self):
        return sorted([self.week1, self.week2, self.week3])

    def score(self):
        return score_table[self.week1] + score_table[self.week2] + score_table[self.week3]

    def print(self):
        print(self.name, self.week1, self.week2, self.week3, self.score())

    def __eq__(self, other):
        return self.result() == other.result()

    def __lt__(self, other):
        if self.score() < other.score():
            return True
        if self.score() > other.score():
            return False
        return self.result() > other.result()


if __name__ == '__main__':
    surrender = GrandMaster("surrender", 1, 3, 4)
    ryvius = GrandMaster("ryvius", 1, 3, 3)
    surrender.week3 = 14
    ryvius.week3 = 6
    print(surrender > ryvius)
