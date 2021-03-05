import GrandmasterLeagueParser
import copy
import time
from Util import html_table, round_per

group_a, group_b = GrandmasterLeagueParser.from_file('status.txt')

group_a_probability_top = {name: 0 for name in group_a.names}
group_a_probability_middle = {name: 0 for name in group_a.names}
group_a_probability_bottom = {name: 0 for name in group_a.names}

group_b_probability_top = {name: 0 for name in group_b.names}
group_b_probability_rank_5 = {name: 0 for name in group_b.names}
group_b_probability_rank_6 = {name: 0 for name in group_b.names}
group_b_probability_bottom = {name: 0 for name in group_b.names}

N = 100000

for i in range(N):
    group_a_possibility = copy.deepcopy(group_a)
    group_b_possibility = copy.deepcopy(group_b)
    group_a_possibility.finish_randomly()
    group_b_possibility.finish_randomly()
    group_a_ranks = group_a_possibility.get_ranks()

    group_a_probability_top[group_a_ranks[0]] += 1
    group_a_probability_top[group_a_ranks[1]] += 1
    group_a_probability_middle[group_a_ranks[2]] += 1
    group_a_probability_middle[group_a_ranks[3]] += 1
    group_a_probability_middle[group_a_ranks[4]] += 1
    group_a_probability_middle[group_a_ranks[5]] += 1
    group_a_probability_bottom[group_a_ranks[6]] += 1
    group_a_probability_bottom[group_a_ranks[7]] += 1

    group_b_ranks = group_b_possibility.get_ranks()
    group_b_probability_top[group_b_ranks[0]] += 1
    group_b_probability_top[group_b_ranks[1]] += 1
    group_b_probability_top[group_b_ranks[2]] += 1
    group_b_probability_top[group_b_ranks[3]] += 1
    group_b_probability_rank_5[group_b_ranks[4]] += 1
    group_b_probability_rank_6[group_b_ranks[5]] += 1
    group_b_probability_bottom[group_b_ranks[6]] += 1
    group_b_probability_bottom[group_b_ranks[7]] += 1

group_a_names = sorted(group_a.names, key=lambda x: (
    group_a_probability_bottom[x],
    -group_a_probability_top[x],
    -group_a.wins[x],
    x
))
table_a = list()
table_a.append([round_per(group_a_probability_top[name], N) for name in group_a_names])
table_a.append([round_per(group_a_probability_middle[name], N) for name in group_a_names])
table_a.append([round_per(group_a_probability_bottom[name], N) for name in group_a_names])
print(html_table(table_a, ['이름', '1-2위', '3-6위', '강등전'], group_a_names))
print()

group_b_names = sorted(group_b.names, key=lambda x: (
    group_b_probability_rank_5[x] / 4 + group_b_probability_rank_6[x] / 2 + group_b_probability_bottom[x],
    -group_b_probability_top[x],
    -group_b.wins[x],
    x
))
table_b = list()
table_b.append([round_per(group_b_probability_top[name], N) for name in group_b_names])
table_b.append([round_per(group_b_probability_rank_5[name], N) for name in group_b_names])
table_b.append([round_per(group_b_probability_rank_6[name], N) for name in group_b_names])
table_b.append([round_per(group_b_probability_bottom[name], N) for name in group_b_names])
print(html_table(table_b, ['이름', '플옵', '5위', '6위', '강등'], group_b_names))
print()


print(time.process_time())
print(N)
print(group_a_probability_top)
print(group_a_probability_middle)
print(group_a_probability_bottom)
print(group_b_probability_top)
print(group_b_probability_rank_5)
print(group_b_probability_rank_6)
print(group_b_probability_bottom)
