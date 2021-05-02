from pandas import DataFrame


class GrandmasterRanks:
    def __init__(self, name):
        self.name = name
        self.playoff = 0
        self.nothing = 0
        self.relegation = 0


class RankCollection:
    def __init__(self):
        self.masters = dict()

    def add_result(self, rank_list):
        if not self.masters:
            for ranked_player in rank_list:
                self.masters[ranked_player] = GrandmasterRanks(ranked_player)

        for i in range(8):
            self.masters[rank_list[i]].playoff += 1

        for i in range(8, 12):
            self.masters[rank_list[i]].nothing += 1

        for i in range(12, 16):
            self.masters[rank_list[i]].relegation += 1

    def export_to_df(self):
        gm_data_frame = DataFrame(
            data=[[gm.playoff, gm.nothing, gm.relegation] for gm in self.masters.values()],
            index=self.masters.keys(),
            columns=['playoff', 'rank 9-12', 'relegation']
        )
        gm_data_frame = gm_data_frame.sort_values(['playoff', 'rank 9-12'])
        gm_data_frame = gm_data_frame.drop('-', errors='ignore')
        return gm_data_frame
