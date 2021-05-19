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
        Util.shuffle(self.grandmasters)
        return [grandmaster.name for grandmaster in sorted(self.grandmasters)]

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
