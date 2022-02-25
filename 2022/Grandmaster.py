from functools import total_ordering


@total_ordering
class GrandMaster:
    def __init__(self, name):
        self.name = name
        self.scores = list()
        self.score_sum = -1
        self.match_result = dict()
        self.win_rate = -1.0

    def receive_score(self, score):
        self.scores.append(score)

    def receive_match_result(self, opponent: str, won: bool):
        if opponent not in self.match_result:
            self.match_result[opponent] = [0, 0] # lose, win
        self.match_result[opponent][won] += 1

    def receive_players_with_same_points(self, opponents):
        score_against_same_points = [0, 0]
        for opponent in opponents:
            if opponent.name not in self.match_result:
                continue
            opponent_result = self.match_result[opponent.name]
            score_against_same_points = [score_against_same_points[idx] + opponent_result[idx] for idx in range(2)]
        if sum(score_against_same_points) > 0:
            self.win_rate = score_against_same_points[1] / sum(score_against_same_points)

    def score(self):
        if self.score_sum == -1:
            self.score_sum = sum(self.scores)
        return self.score_sum

    def print(self):
        print(self.name, self.score_sum, self.match_result)

    def __eq__(self, other):
        return self.score() == other.score() and self.win_rate == other.winrate

    def __lt__(self, other):
        if self.score() > other.score():
            return True
        if self.score() < other.score():
            return False
        return self.win_rate > other.win_rate


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
