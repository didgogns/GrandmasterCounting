import GrandmasterLeagueParser
import copy
import time
from Util import html_table, round_per
import itertools

group_a, group_b = GrandmasterLeagueParser.from_file('status.txt')

group_a_probability_top = {name: 0 for name in group_a.names}
group_a_probability_middle = {name: 0 for name in group_a.names}
group_a_probability_bottom = {name: 0 for name in group_a.names}

group_b_probability_top = {name: 0 for name in group_b.names}
group_b_probability_rank_5 = {name: 0 for name in group_b.names}
group_b_probability_rank_6 = {name: 0 for name in group_b.names}
group_b_probability_bottom = {name: 0 for name in group_b.names}

remaining_match_a = 28 - sum(group_a.wins.values())
remaining_result_a = list(itertools.product([True, False], repeat=remaining_match_a))
N_a = len(remaining_result_a)
for result in remaining_result_a:
    group_a_possibility = copy.deepcopy(group_a)
    group_a_possibility.finish_with_result(result)
    group_a_ranks = group_a_possibility.get_ranks_no_random()
    for player, array in group_a_ranks.items():
        group_a_probability_top[player] += array[0]
        group_a_probability_top[player] += array[1]
        group_a_probability_middle[player] += array[2]
        group_a_probability_middle[player] += array[3]
        group_a_probability_middle[player] += array[4]
        group_a_probability_middle[player] += array[5]
        group_a_probability_bottom[player] += array[6]
        group_a_probability_bottom[player] += array[7]

remaining_match_b = 28 - sum(group_b.wins.values())
remaining_result_b = list(itertools.product([True, False], repeat=remaining_match_b))
N_b = len(remaining_result_b)
for result in remaining_result_b:
    group_b_possibility = copy.deepcopy(group_b)
    group_b_possibility.finish_with_result(result)
    group_b_ranks = group_b_possibility.get_ranks_no_random()
    for player, array in group_b_ranks.items():
        group_b_probability_top[player] += array[0]
        group_b_probability_top[player] += array[1]
        group_b_probability_top[player] += array[2]
        group_b_probability_top[player] += array[3]
        group_b_probability_rank_5[player] += array[4]
        group_b_probability_rank_6[player] += array[5]
        group_b_probability_bottom[player] += array[6]
        group_b_probability_bottom[player] += array[7]

group_a_names = sorted(group_a.names, key=lambda x: (group_a_probability_bottom[x], x))
table_a = list()
table_a.append([round_per(group_a_probability_top[name], N_a) for name in group_a_names])
table_a.append([round_per(group_a_probability_middle[name], N_a) for name in group_a_names])
table_a.append([round_per(group_a_probability_bottom[name], N_a) for name in group_a_names])
print(html_table(table_a, ['이름', '1-2위', '3-6위', '강등전'], group_a_names))
print()

group_b_names = sorted(
    group_b.names,
    key=lambda x:
    (group_b_probability_rank_5[x] / 4 + group_b_probability_rank_6[x] / 2 + group_b_probability_bottom[x], x))
table_b = list()
table_b.append([round_per(group_b_probability_top[name], N_b) for name in group_b_names])
table_b.append([round_per(group_b_probability_rank_5[name], N_b) for name in group_b_names])
table_b.append([round_per(group_b_probability_rank_6[name], N_b) for name in group_b_names])
table_b.append([round_per(group_b_probability_bottom[name], N_b) for name in group_b_names])
print(html_table(table_b, ['이름', '플옵', '5위', '6위', '강등'], group_b_names))
print()


print(time.process_time())
print(N_a)
print(N_b)
print(group_a_probability_top)
print(group_a_probability_middle)
print(group_a_probability_bottom)
print(group_b_probability_top)
print(group_b_probability_rank_5)
print(group_b_probability_rank_6)
print(group_b_probability_bottom)
