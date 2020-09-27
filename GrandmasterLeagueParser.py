from GrandmasterLeague import GrandMasterLeague


def from_file(file_name):
    with open(file_name) as f:
        group_a = GrandMasterLeague(f.readline().split())
        group_b = GrandMasterLeague(f.readline().split())
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
