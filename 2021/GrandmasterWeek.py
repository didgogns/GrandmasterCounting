import Util
from abc import abstractmethod, ABCMeta
from GrandmasterPool import GrandmasterPool


class Serializable(metaclass=ABCMeta):
    @abstractmethod
    def init_from_json(self, json_value: dict, pool: GrandmasterPool):
        pass

    @abstractmethod
    def export(self) -> dict:
        pass


class TournamentBase(Serializable):
    @abstractmethod
    def finish(self):
        pass

    @abstractmethod
    def is_finished(self) -> bool:
        pass

    @abstractmethod
    def validate(self):
        pass


class DualTournament(TournamentBase):
    def __init__(self, participants, results):
        self.participants = participants
        self.initials, self.winners, self.elimination, self.decider = results

    @classmethod
    def init_from_json(cls, json_value: dict, pool: GrandmasterPool):
        assert json_value
        initials = [match_from_dict(initials, pool) for initials in json_value['initials']]
        winners = match_from_dict(json_value['winners'], pool)
        elimination = match_from_dict(json_value['elimination'], pool)
        decider = match_from_dict(json_value['decider'], pool)
        return cls(None, (initials, winners, elimination, decider))

    def finish(self):
        for idx in range(len(self.initials)):
            if self.initials[idx] is None:
                self.initials[idx] = Util.coin_flip(self.participants[2 * idx], self.participants[2 * idx + 1])
        if self.winners is None:
            self.winners = Util.coin_flip(self.initials[0][0], self.initials[1][0])
        if self.elimination is None:
            self.elimination = Util.coin_flip(self.initials[0][1], self.initials[1][1])
        if self.decider is None:
            self.decider = Util.coin_flip(self.winners[1], self.elimination[0])
        self.decider[1].receive(1)
        self.elimination[1].receive(0)
        return self.winners[0], self.decider[0]

    def validate(self):
        assert(len(self.participants) == 4)
        assert(len(self.initials) == 2)

    def is_finished(self) -> bool:
        # TODO cache tournament result
        return False

    def export(self) -> dict:
        result = dict()
        result['initials'] = [match_to_dict(initial) for initial in self.initials]
        result['winners'] = match_to_dict(self.winners)
        result['elimination'] = match_to_dict(self.elimination)
        result['decider'] = match_to_dict(self.decider)
        return result


class Tournament(TournamentBase):
    def __init__(self, participants, results):
        self.participants = participants
        self.quarterfinals, self.semifinals, self.final = results

    @classmethod
    def init_from_json(cls, json_value: dict, pool: GrandmasterPool):
        assert json_value
        quarterfinals = [match_from_dict(quarterfinal, pool) for quarterfinal in json_value['quarterfinals']]
        semifinals = [match_from_dict(semifinal, pool) for semifinal in json_value['semifinals']]
        final = match_from_dict(json_value['final'], pool)
        return cls(None, (quarterfinals, semifinals, final))

    def finish(self):
        for idx in range(len(self.quarterfinals)):
            if self.quarterfinals[idx] is None:
                self.quarterfinals[idx] = Util.coin_flip(self.participants[2 * idx], self.participants[2 * idx + 1])
            self.quarterfinals[idx][1].receive(2)
        for idx in range(len(self.semifinals)):
            if self.semifinals[idx] is None:
                self.semifinals[idx] = \
                    Util.coin_flip(self.quarterfinals[2 * idx][0], self.quarterfinals[2 * idx + 1][0])
            self.semifinals[idx][1].receive(3)
        if self.final is None:
            self.final = Util.coin_flip(self.semifinals[0][0], self.semifinals[1][0])
        self.final[1].receive(4)
        self.final[0].receive(5)

    def validate(self):
        assert(len(self.participants) == 8)
        assert(len(self.quarterfinals) == 4)
        assert(len(self.semifinals) == 2)

    def is_finished(self):
        # TODO cache tournament result
        return False

    def export(self) -> dict:
        result = dict()
        result['quarterfinals'] = [match_to_dict(quarterfinal) for quarterfinal in self.quarterfinals]
        result['semifinals'] = [match_to_dict(semifinal) for semifinal in self.semifinals]
        result['final'] = match_to_dict(self.final)
        return result


class GrandmasterWeek(TournamentBase):
    def __init__(self, dual_tournament_groups, tournament):
        self.dual_tournament_groups = dual_tournament_groups
        self.tournament = tournament

    @classmethod
    def init_from_json(cls, json_value: dict, pool: GrandmasterPool):
        dual_tournament_group = json_value['dual_tournament_groups']
        dual_tournament_groups = [
            DualTournament.init_from_json(dual_tournament_json, pool) for dual_tournament_json in dual_tournament_group
        ]
        tournament = Tournament.init_from_json(json_value['tournament'], pool)
        return cls(dual_tournament_groups, tournament)

    def finish(self):
        dual_tournament_result = list()
        for dual_tournament in self.dual_tournament_groups:
            dual_tournament_result.append(dual_tournament.finish())
        if self.tournament is None:
            self.tournament = Tournament([
                dual_tournament_result[0][0], dual_tournament_result[1][1],
                dual_tournament_result[2][0], dual_tournament_result[3][1],
                dual_tournament_result[1][0], dual_tournament_result[0][1],
                dual_tournament_result[3][0], dual_tournament_result[2][1]
            ], ([None, None, None, None], [None, None], None))
        self.tournament.finish()

    def validate(self):
        assert(len(self.dual_tournament_groups) == 4)
        for dual_tournament in self.dual_tournament_groups:
            if dual_tournament is not None:
                dual_tournament.validate()
            else:
                print('empty dual_tournament?')
        if self.tournament is not None:
            self.tournament.validate()

    def is_finished(self):
        return self.tournament.is_finished()

    def export(self) -> dict:
        result = dict()
        result['dual_tournament_groups'] = [dual_tournament.export() for dual_tournament in self.dual_tournament_groups]
        result['tournament'] = self.tournament.export()
        return result


# For week not yet started, no need to actually play all games
class EmptyGrandmasterWeek(TournamentBase):
    def __init__(self, participants):
        self.participants = participants

    @classmethod
    def init_from_json(cls, json_value: dict, pool: GrandmasterPool):
        return cls(participants = pool.get_masters())

    def finish(self):
        Util.shuffle(self.participants)
        score_table = [5, 4, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0]
        for idx in range(len(self.participants)):
            self.participants[idx].receive(score_table[idx])

    def validate(self):
        assert(len(self.participants) == 16)

    def is_finished(self):
        return False

    def export(self) -> dict:
        return dict()


def match_to_dict(match):
    if match is None:
        return None
    return [match[0].name, match[1].name]


def match_from_dict(match, pool):
    if match is None:
        return None
    return pool.get_master_by_name(match[0]), pool.get_master_by_name(match[1])
