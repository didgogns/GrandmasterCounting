from GrandmasterLeague import GrandMasterLeague


def from_file(file_name):
    with open(file_name) as f:
        players = list()
        cnt = 0
        while cnt != 8:
            players_with_same_t3 = f.readline().split()
            players.append(players_with_same_t3)
            cnt += len(players_with_same_t3)
        group_a = GrandMasterLeague(players)
        players.clear()
        cnt = 0
        while cnt != 8:
            players_with_same_t3 = f.readline().split()
            players.append(players_with_same_t3)
            cnt += len(players_with_same_t3)
        group_b = GrandMasterLeague(players)
        matches = f.readlines()
        for raw_match in matches:
            match = raw_match.split()
            if match[0] in group_a.names:
                group_a.match(match[0], match[1])
            else:
                group_b.match(match[0], match[1])
    return group_a, group_b


if __name__ == '__main__':
    from_file('status.txt')
