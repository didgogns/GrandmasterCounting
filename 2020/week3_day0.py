from Grandmaster import GrandMaster
from random import shuffle
import time

num_simulation = 10_000_000

if __name__ == '__main__':
    g1 = GrandMaster('Surrender', 4, 1)
    g2 = GrandMaster('Bankyugi', 1, 10)
    g3 = GrandMaster('Tyler', 3, 3)
    g4 = GrandMaster('tom60229', 12, 2)
    g5 = GrandMaster('posesi', 5, 6)
    g6 = GrandMaster('Che0nsu', 2, 13)
    g7 = GrandMaster('TIZS', 15, 4)
    g8 = GrandMaster('glory', 6, 11)
    g9 = GrandMaster('Flurry', 7, 8)
    g10 = GrandMaster('Shaxy', 14, 5)
    g11 = GrandMaster('kin0531', 16, 7)
    g12 = GrandMaster('blitzchung', 8, 16)
    g13 = GrandMaster('Alan870806', 9, 12)
    g14 = GrandMaster('Ryvius', 13, 9)
    g15 = GrandMaster('Alutemu', 10, 15)
    g16 = GrandMaster('DawN', 11, 14)
    gm_list = [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14, g15, g16]
    gm_group_a_count = {}
    for gm in gm_list:
        gm_group_a_count[gm.name] = 0

    for sim_count in range(num_simulation):
        shuffle(gm_list)
        for i, gm in enumerate(gm_list):
            gm.week3 = i + 1
        a_prob_sum = 0.0
        for gm in gm_list:
            lost = 0
            equal = 0
            won = 0
            a_prob = 0
            for other_gm in gm_list:
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
            for gm in gm_list:
                gm.print()
            print(sim_count, a_prob_sum)
            print(gm_group_a_count)
            print(time.process_time())
            exit(0)

    print(gm_group_a_count)
    print(time.process_time())
