import Util
import GrandmasterWeek


class GrandMasterLeague:
    def __init__(self, grandmasters, weeks):
        self.grandmasters = grandmasters
        self.weeks = weeks

    def finish(self):
        for week in self.weeks:
            week.finish()

    def get_ranks(self):
        result = [None] * len(self.grandmasters)
        Util.shuffle(self.grandmasters)
        for idx in range(len(self.grandmasters)):
            self.grandmasters[idx].luck = idx
        for grandmaster in self.grandmasters:
            count_better = 0
            for other_grandmaster in self.grandmasters:
                if other_grandmaster > grandmaster:
                    count_better += 1
            result[count_better] = grandmaster.name
        return result

    @staticmethod
    def to_dict(league):
        result = dict()
        result['grandmasters'] = [master.name for master in league.grandmasters]
        result['weeks'] = [GrandmasterWeek.to_dict(week) for week in league.weeks]
        return result

    @staticmethod
    def from_dict(league_dict, pool):
        grandmasters_json = league_dict['grandmasters']
        for grandmaster_json in grandmasters_json:
            pool.get_master_by_name(grandmaster_json)
        grandmasters = pool.get_masters()
        weeks = [GrandmasterWeek.from_dict(week, pool) for week in league_dict['weeks']]
        return GrandMasterLeague(grandmasters, weeks)
