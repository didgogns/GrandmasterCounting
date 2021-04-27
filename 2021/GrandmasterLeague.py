import Util


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
