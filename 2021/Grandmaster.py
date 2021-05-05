class GrandMaster:
    def __init__(self, name):
        self.name = name
        self.scores = list()
        self.sorted_scores = None
        self.luck = 0

    def receive(self, score):
        self.scores.append(score)

    def result(self):
        if self.sorted_scores is None:
            self.sorted_scores = sorted(self.scores)
        return self.sorted_scores

    def score(self):
        return sum(self.scores)

    def print(self):
        print(self.name, self.scores)

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        if self.score() < other.score():
            return True
        if self.score() > other.score():
            return False
        if self.result() < other.result():
            return True
        if self.result() > other.result():
            return False
        return self.luck > other.luck


if __name__ == '__main__':
    surrender = GrandMaster("surrender", [1, 3])
    hi3 = GrandMaster("hi3", [2, 2])
    print(surrender > hi3)
