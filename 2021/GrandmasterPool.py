from Grandmaster import GrandMaster


class GrandmasterPool:
    def __init__(self):
        self.pool = dict()

    def get_master_by_name(self, name):
        if name in self.pool:
            return self.pool[name]
        else:
            grandmaster = GrandMaster(name)
            self.pool[name] = grandmaster
            return grandmaster

    def get_masters(self):
        return list(self.pool.values())
