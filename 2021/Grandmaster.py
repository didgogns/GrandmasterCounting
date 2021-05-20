from functools import total_ordering

@total_ordering
class GrandMaster:
    def __init__(self, name):
        self.name = name
        self.scores = list()
        self.score_sum = -1
        self.sorted_scores = None

    def receive(self, score):
        self.scores.append(score)

    def result(self):
        if self.sorted_scores is None:
            self.sorted_scores = sorted(self.scores, reverse=True)
        return self.sorted_scores

    def score(self):
        if self.score_sum == -1:
            self.score_sum = sum(self.scores)
            if self.name == 'xBlyzes':
                self.score_sum -= 2
        return self.score_sum

    def print(self):
        print(self.name, self.score_sum, self.sorted_scores)

    def __eq__(self, other):
        return self.result() == other.result()

    def __lt__(self, other):
        if self.score() > other.score():
            return True
        if self.score() < other.score():
            return False
        return self.result() > other.result()


if __name__ == '__main__':
    surrender = GrandMaster("surrender")
    hi3 = GrandMaster("hi3")
    surrender.receive(3)
    surrender.receive(3)
    surrender.receive(2)
    hi3.receive(4)
    hi3.receive(3)
    hi3.receive(1)
    Dawn = GrandMaster('Dawn')
    Dawn.receive(4)
    Dawn.receive(4)
    Dawn.receive(4)
    print(surrender > hi3)
    print(hi3 < hi3)
    print(Dawn > surrender)
    surrender.print()
    hi3.print()
    Dawn.print()
