from Grandmaster import GrandMaster
import copy
from day2_util import get_day2_possibility
import time

if __name__ == '__main__':
    g1 = GrandMaster('Surrender', 4, 1, 14)
    g2 = GrandMaster('Bankyugi', 1, 10, 3)
    g3 = GrandMaster('Tyler', 3, 3, 13)
    g4 = GrandMaster('tom60229', 12, 2, 8)
    g5 = GrandMaster('posesi', 5, 6, 10)
    g6 = GrandMaster('Che0nsu', 2, 13, 4)
    g7 = GrandMaster('TIZS', 15, 4, 9)
    g8 = GrandMaster('glory', 6, 11, 5)
    g9 = GrandMaster('Flurry', 7, 8, 12)
    g10 = GrandMaster('Shaxy', 14, 5, 11)
    g11 = GrandMaster('kin0531', 16, 7, 15)
    g12 = GrandMaster('blitzchung', 8, 16, 7)
    g13 = GrandMaster('Alan870806', 9, 12, 2)
    g14 = GrandMaster('Ryvius', 13, 9, 1)
    g15 = GrandMaster('Alutemu', 10, 15, 16)
    g16 = GrandMaster('DawN', 11, 14, 6)
    gm_list = [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14, g15, g16]
    gm_group_a_count = {}
    for gm in gm_list:
        gm_group_a_count[gm.name] = 0

    possibilities = get_day2_possibility()
    possibilities = list(filter(lambda x : x[0] in [7, 8] and x[7] in [5, 6], possibilities))
    for possibility in possibilities:
        new_gm_list = copy.deepcopy(gm_list)
        for gm in new_gm_list:
            if gm.week3 <= 8:
                gm.week3 = possibility[gm.week3 - 1]
        a_prob_sum = 0.0
        for gm in new_gm_list:
            lost = 0
            equal = 0
            won = 0
            a_prob = 0
            for other_gm in new_gm_list:
                if gm < other_gm:
                    lost += 1
                elif gm == other_gm:
                    equal += 1
                else:
                    won += 1

            if won >= 8:
                a_prob = 1
            elif lost >= 8:
                a_prob = 0
            else:
                a_prob = (8 - lost) / equal
            gm_group_a_count[gm.name] += a_prob
            a_prob_sum += a_prob
        if a_prob_sum != 8:
            for gm in new_gm_list:
                gm.print()
            print(gm_group_a_count)
            print(time.process_time())
            exit(0)

    for name, value in gm_group_a_count.items():
        print(name, str(round(value / len(possibilities) * 100, 2)) + '%', str(value // 2) + '/' + str(len(possibilities) // 2))
    print(time.process_time())
