from abc import ABC

import Util
import GrandmasterWeek


class GrandMasterLeague(GrandmasterWeek.TournamentBase):
    def __init__(self, grandmasters, weeks):
        self.grandmasters = grandmasters
        self.weeks = weeks

    @classmethod
    def init_from_json(cls, json_value: dict, pool):
        grandmasters_json = json_value['grandmasters']
        for grandmaster_json in grandmasters_json:
            if grandmaster_json:
                pool.get_master_by_name(grandmaster_json)
        cls.grandmasters = pool.get_masters()
        cls.weeks = [
            GrandmasterWeek.GrandmasterWeek.init_from_json(week, pool) if week
            else GrandmasterWeek.EmptyGrandmasterWeek.init_from_json(week, pool)
            for week in json_value['weeks']
        ]

    def finish(self):
        for week in self.weeks:
            week.finish()

    def validate(self):
        pass

    def is_finished(self) -> bool:
        return False

    def get_ranks(self):
        Util.shuffle(self.grandmasters)
        return [grandmaster.name for grandmaster in sorted(self.grandmasters)]

    def export(self) -> dict:
        result = dict()
        result['grandmasters'] = [master.name for master in self.grandmasters]
        result['weeks'] = [week.export() for week in self.weeks]
        return result
