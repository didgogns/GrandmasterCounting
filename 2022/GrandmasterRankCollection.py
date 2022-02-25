import numpy as np


class GrandmasterRanks:
    def __init__(self, name):
        self.name = name
        self.results = [0] * 5
        self.sum_of_ranks = 0
        self.first_result = 0
        self.second_result = 0
        self.third_result = 0


class RankCollection:
    def __init__(self):
        self.masters = dict()

    def add_result(self, rank_list):
        if not self.masters:
            for ranked_player in rank_list:
                self.masters[ranked_player] = GrandmasterRanks(ranked_player)

        for i in range(2):
            self.masters[rank_list[i]].results[0] += 1

        for i in range(2, 4):
            self.masters[rank_list[i]].results[1] += 1

        for i in range(4, 6):
            self.masters[rank_list[i]].results[2] += 1

        for i in range(6, 8):
            self.masters[rank_list[i]].results[3] += 1

        for i in range(8, 16):
            self.masters[rank_list[i]].results[4] += 1

        for i in range(16):
            self.masters[rank_list[i]].sum_of_ranks += i

    def export_to_array(self):
        gm_array = np.array([[gm.name, gm.results[0], gm.results[1], gm.results[2], gm.results[3], gm.results[4], -gm.sum_of_ranks]
                             for gm in self.masters.values() if gm.name != '-'])
        ind = np.lexsort([gm_array[:, 0],
                          gm_array[:, 6].astype(int)])
        gm_array = gm_array[ind]
        return gm_array, ['rank 1-2', 'rank 3-4', 'rank 5-6', 'rank 7-8', 'rank 9-16']
