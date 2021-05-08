import numpy as np


class GrandmasterRanks:
    def __init__(self, name):
        self.name = name
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

        for i in range(8):
            self.masters[rank_list[i]].first_result += 1

        for i in range(8, 12):
            self.masters[rank_list[i]].second_result += 1

        for i in range(12, 16):
            self.masters[rank_list[i]].third_result += 1

    def export_to_array(self):
        gm_array = np.array([[gm.name, gm.first_result, gm.second_result, gm.third_result] for gm in self.masters.values()
                             if gm.name != '-'])
        ind = np.lexsort([gm_array[:, 0], gm_array[:, 2].astype(int), gm_array[:, 1].astype(int)])
        gm_array = gm_array[ind]
        return gm_array, ['playoff', 'rank 9-12', 'relegation']


class RankCollectionForPlayoff:
    def __init__(self):
        self.masters = dict()

    def add_result(self, rank_list):
        if not self.masters:
            for ranked_player in rank_list:
                self.masters[ranked_player] = GrandmasterRanks(ranked_player)

        for i in range(2):
            self.masters[rank_list[i]].first_result += 1

        for i in range(2, 6):
            self.masters[rank_list[i]].second_result += 1

        for i in range(6, 8):
            self.masters[rank_list[i]].third_result += 1

    def export_to_array(self):
        gm_array = np.array([[gm.name, gm.first_result, gm.second_result, gm.third_result] for gm in self.masters.values()
                             if gm.name != '-'])
        ind = np.lexsort([gm_array[:, 0], gm_array[:, 2].astype(int), gm_array[:, 1].astype(int)])
        gm_array = gm_array[ind]
        return gm_array, ['rank 1-2', 'rank 3-6', 'rank 7-8']
