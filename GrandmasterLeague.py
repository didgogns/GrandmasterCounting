import itertools
import random


class GrandMasterLeague:
    def __init__(self, names_sorted_by_t3):
        cnt = 0
        names = list()
        self.tb2 = dict()
        for t3, names_with_same_t3 in enumerate(names_sorted_by_t3):
            cnt += len(names_with_same_t3)
            names.extend(names_with_same_t3)
            for name in names_with_same_t3:
                self.tb2[name] = -0.01 * t3
        assert(cnt == 8)
        self.names = names
        self.results = {tuple(sorted(match)): None for match in itertools.combinations(names, 2)}
        self.wins = {name: 0 for name in names}

    def match(self, winner, loser):
        assert(winner in self.names)
        assert(loser in self.names)
        self.results[tuple(sorted([winner, loser]))] = winner
        self.wins[winner] += 1

    def is_ended(self):
        for entry in self.results.values():
            if entry is None:
                return False
        return True

    def finish_randomly(self):
        for entry, result in self.results.items():
            if result is None:
                player_a, player_b = entry
                if bool(random.getrandbits(1)):
                    self.match(player_a, player_b)
                else:
                    self.match(player_b, player_a)
        assert(self.is_ended())

    def finish_with_result(self, remaining_result):
        cur_idx = 0
        for entry, result in self.results.items():
            if result is None:
                player_a, player_b = entry
                if remaining_result[cur_idx]:
                    self.match(player_a, player_b)
                else:
                    self.match(player_b, player_a)
                cur_idx += 1
        assert(self.is_ended())

    def get_tb2(self):
        for entry, result in self.results.items():
            winner, loser = entry
            if result == loser:
                winner, loser = loser, winner
            self.tb2[winner] += self.wins[loser]

    def get_ranks(self):
        assert(self.is_ended())
        self.get_tb2()
        result = list()
        for i in range(7, -1, -1):
            players_with_i_wins = list()
            for player in self.names:
                if self.wins[player] == i:
                    players_with_i_wins.append(player)
            if len(players_with_i_wins) < 2:
                result.extend(players_with_i_wins)
            elif len(players_with_i_wins) == 2:
                winner = players_with_i_wins[0]
                loser = players_with_i_wins[1]
                if self.results[tuple(sorted([winner, loser]))] == loser:
                    winner, loser = loser, winner
                result.append(winner)
                result.append(loser)
            else:
                random.shuffle(players_with_i_wins)
                players_with_i_wins = sorted(players_with_i_wins, key=lambda x: -self.tb2[x])
                result.extend(players_with_i_wins)
        return result

    def get_ranks_no_random(self):
        result = {x: [0] * len(self.names) for x in self.names}
        assert(self.is_ended())
        self.get_tb2()
        cur_rank = 0
        for i in range(7, -1, -1):
            players_with_i_wins = list()
            for player in self.names:
                if self.wins[player] == i:
                    players_with_i_wins.append(player)
            if len(players_with_i_wins) < 2:
                for player in players_with_i_wins:
                    result[player][cur_rank] = 1
                    cur_rank += 1
            elif len(players_with_i_wins) == 2:
                winner = players_with_i_wins[0]
                loser = players_with_i_wins[1]
                if self.results[tuple(sorted([winner, loser]))] == loser:
                    winner, loser = loser, winner
                result[winner][cur_rank] = 1
                cur_rank += 1
                result[loser][cur_rank] = 1
                cur_rank += 1
            else:
                num_player_tie = len(players_with_i_wins)
                for player in players_with_i_wins:
                    num_won = 0
                    num_tie = 0
                    num_lost = 0
                    for other_player in players_with_i_wins:
                        if self.tb2[player] > self.tb2[other_player]:
                            num_won += 1
                        elif self.tb2[player] == self.tb2[other_player]:
                            num_tie += 1
                        else:
                            num_lost += 1
                    for j in range(num_tie):
                        result[player][cur_rank + num_lost + j] += 1 / num_tie
                cur_rank += num_player_tie
        return result


if __name__ == '__main__':
    group_a = GrandMasterLeague(['surrender', 'bankyugi', 'tom', 'cheonsu', 'dawn', 'glory', 'blitzchung', 'Tyler'])
    print(group_a.wins)
    print(group_a.results)
    group_a.match("bankyugi", "surrender")
    group_a.finish_randomly()
    print(group_a.get_ranks())
    print(group_a.wins)
    print(group_a.tb2)
    print(group_a.results)
