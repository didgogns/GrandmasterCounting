import typing
from abc import abstractmethod, ABCMeta

import Util
from GrandmasterPool import GrandmasterPool
from Grandmaster import GrandMaster
from Match import Match, Serializable


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

    @abstractmethod
    def finish_matches_intelligently(self):
        pass


class DualTournament(TournamentBase):
    participants: typing.List[GrandMaster]
    initials: typing.List[Match]
    winners: typing.Optional[Match]
    elimination: typing.Optional[Match]
    decider: typing.Optional[Match]
    first_place = typing.Optional[GrandMaster]
    second_place = typing.Optional[GrandMaster]

    def __init__(self, participants, results):
        self.participants = participants
        self.initials, self.winners, self.elimination, self.decider = results

    @classmethod
    def init_from_json(cls, json_value: dict, pool: GrandmasterPool):
        if json_value is None:
            return None
        participants = [pool.get_master_by_name(participant) for participant in json_value['participants']]
        initials = [Match.init_from_json(initial, pool) for initial in json_value['initials']]
        winners = Match.init_from_json(json_value['winners'], pool)
        elimination = Match.init_from_json(json_value['elimination'], pool)
        decider = Match.init_from_json(json_value['decider'], pool)
        return cls(participants, (initials, winners, elimination, decider))

    def finish(self):
        for idx in range(len(self.initials)):
            self.initials[idx].finish()
        if self.winners.participants[0] is None:
            self.winners.participants = [self.initials[0].get_winner(), self.initials[1].get_winner()]
        self.winners.finish()
        if self.elimination.participants[0] is None:
            self.elimination.participants = [self.initials[0].get_loser(), self.initials[1].get_loser()]
        self.elimination.finish()
        if self.decider.participants[0] is None:
            self.decider.participants = [self.winners.get_loser(), self.elimination.get_winner()]
        self.decider.finish()
        self.elimination.get_loser().receive(0)
        self.decider.get_loser().receive(1)
        self.first_place = self.winners.get_winner()
        self.second_place = self.decider.get_winner()

    def validate(self):
        assert(len(self.participants) == 4)
        assert(len(self.initials) == 2)

    def is_finished(self) -> bool:
        return self.decider.is_first_player_won is not None

    def export(self) -> dict:
        result = dict()
        result['participants'] = [participant.name if participant is not None else ''
                                  for participant in self.participants]
        result['initials'] = [initial.export() for initial in self.initials]
        result['winners'] = self.winners.export()
        result['elimination'] = self.elimination.export()
        result['decider'] = self.decider.export()
        return result

    def finish_matches_intelligently(self):
        winners_loser, elimination_winner = self.decider.participants
        if self.elimination.is_first_player_won is None and elimination_winner is not None:
            self.elimination.is_first_player_won = self.elimination.participants[0].name == elimination_winner.name
        if self.winners.is_first_player_won is None and winners_loser is not None:
            self.winners.is_first_player_won = self.winners.participants[0].name != winners_loser.name
        for idx, initial in enumerate(self.initials):
            if initial.is_first_player_won is None and self.winners.participants[idx] is not None:
                initial.is_first_player_won = initial.participants[0].name == self.winners.participants[idx].name


class Tournament(TournamentBase):
    participants: typing.List[GrandMaster]
    quarterfinals: typing.List[Match]
    semifinals: typing.List[Match]
    final: typing.Optional[Match]

    def __init__(self, participants, results):
        self.participants = participants
        self.quarterfinals, self.semifinals, self.final = results

    @classmethod
    def init_from_json(cls, json_value: dict, pool: GrandmasterPool):
        if json_value is None:
            return None
        participants = [pool.get_master_by_name(participant) for participant in json_value['participants']]
        quarterfinals = [Match.init_from_json(quarterfinal, pool) for quarterfinal in json_value['quarterfinals']]
        semifinals = [Match.init_from_json(semifinal, pool) for semifinal in json_value['semifinals']]
        final = Match.init_from_json(json_value['final'], pool)
        return cls(participants, (quarterfinals, semifinals, final))

    def finish(self):
        for idx in range(len(self.quarterfinals)):
            if self.quarterfinals[idx].participants[0] is None:
                self.quarterfinals[idx].participants = [self.participants[2 * idx], self.participants[2 * idx + 1]]
            self.quarterfinals[idx].finish()
            self.quarterfinals[idx].get_loser().receive(2)
        for idx in range(len(self.semifinals)):
            if self.semifinals[idx].participants[0] is None:
                self.semifinals[idx].participants = [self.quarterfinals[2 * idx].get_winner(),
                                                     self.quarterfinals[2 * idx + 1].get_winner()]
            self.semifinals[idx].finish()
            self.semifinals[idx].get_loser().receive(3)
        if self.final.participants[0] is None:
            self.final.participants = [self.semifinals[0].get_winner(), self.semifinals[1].get_winner()]
        self.final.finish()
        self.final.get_loser().receive(4)
        self.final.get_winner().receive(5)

    def validate(self):
        assert(len(self.participants) == 8)
        assert(len(self.quarterfinals) == 4)
        assert(len(self.semifinals) == 2)

    def is_finished(self):
        return self.final is not None and self.final.is_first_player_won is not None

    def export(self) -> dict:
        result = dict()
        result['participants'] = [participant.name if participant is not None else ''
                                  for participant in self.participants]
        result['quarterfinals'] = [quarterfinal.export() for quarterfinal in self.quarterfinals]
        result['semifinals'] = [semifinal.export() for semifinal in self.semifinals]
        result['final'] = self.final.export()
        return result

    def finish_matches_intelligently(self):
        for idx, semifinal in enumerate(self.semifinals):
            if semifinal.is_first_player_won is None and self.final.participants[idx] is not None:
                semifinal.is_first_player_won = semifinal.participants[0].name == self.final.participants[idx].name

        for idx, quarterfinal in enumerate(self.quarterfinals):
            potential_winner = self.semifinals[idx // 2].participants[idx % 2]
            if quarterfinal.is_first_player_won is None and potential_winner is not None:
                quarterfinal.is_first_player_won = quarterfinal.participants[0].name == potential_winner.name

    @staticmethod
    def empty():
        return Tournament([None] * 8, ([Match.empty(), Match.empty(), Match.empty(), Match.empty()],
                          [Match.empty(), Match.empty()], Match.empty()))


class GrandmasterWeek(TournamentBase):
    dual_tournament_groups = typing.List[DualTournament]
    tournament: typing.Optional[Tournament]

    def __init__(self, dual_tournament_groups, tournament):
        self.dual_tournament_groups = dual_tournament_groups
        self.tournament = tournament

    @classmethod
    def init_from_json(cls, json_value: dict, pool: GrandmasterPool):
        if not json_value:
            return None
        dual_tournament_group = json_value['dual_tournament_groups']
        dual_tournament_groups = [
            DualTournament.init_from_json(dual_tournament_json, pool) for dual_tournament_json in dual_tournament_group
        ]
        tournament = Tournament.init_from_json(json_value['tournament'], pool)
        return cls(dual_tournament_groups, tournament)

    def finish(self):
        dual_tournament_result = list()
        for dual_tournament in self.dual_tournament_groups:
            dual_tournament.finish()
            dual_tournament_result.append([dual_tournament.first_place, dual_tournament.second_place])
        # Tournament is not yet started
        if self.tournament is None:
            self.tournament = Tournament.empty()
        if self.tournament.participants[0] is None:
            self.tournament.participants = [
                dual_tournament_result[0][0], dual_tournament_result[1][1],
                dual_tournament_result[2][0], dual_tournament_result[3][1],
                dual_tournament_result[1][0], dual_tournament_result[0][1],
                dual_tournament_result[3][0], dual_tournament_result[2][1]]
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
        return self.tournament is not None and self.tournament.is_finished()

    def export(self) -> dict:
        result = dict()
        result['dual_tournament_groups'] = [dual_tournament.export() for dual_tournament in self.dual_tournament_groups]
        result['tournament'] = self.tournament.export() if self.tournament is not None else {}
        return result

    def is_end_of_day(self) -> bool:
        dual_tournament_not_started = True
        dual_tournament_finished_except_decider = True
        dual_tournament_finished = True
        for dual_tournament in self.dual_tournament_groups:
            for initial in dual_tournament.initials:
                if initial.is_first_player_won is not None:
                    dual_tournament_not_started = False
            if not dual_tournament.is_finished():
                dual_tournament_finished = False
            if dual_tournament.winners.is_first_player_won is None or\
                    dual_tournament.elimination.is_first_player_won is None or\
                    dual_tournament.is_finished():
                dual_tournament_finished_except_decider = False
        if dual_tournament_not_started or dual_tournament_finished_except_decider:
            return True
        if not dual_tournament_finished:
            return False
        if self.tournament is None:
            return False
        tournament_not_started = True
        quarterfinal_finished = True
        semifinal_not_started = True
        final_finished = self.tournament.is_finished()
        if final_finished:
            return True
        for quarterfinal in self.tournament.quarterfinals:
            if quarterfinal.is_first_player_won is not None:
                tournament_not_started = False
            else:
                quarterfinal_finished = False
        for semifinal in self.tournament.semifinals:
            if semifinal.is_first_player_won is not None:
                semifinal_not_started = False
        if tournament_not_started:
            return True
        if not quarterfinal_finished:
            return False
        if semifinal_not_started:
            return True
        return False

    def finish_matches_intelligently(self):
        if self.tournament is not None:
            self.tournament.finish_matches_intelligently()
            place_of_decide_winner_in_tournament = [5, 1, 7, 3]
            for idx, dual_tournament in enumerate(self.dual_tournament_groups):
                potential_winner = self.tournament.participants[place_of_decide_winner_in_tournament[idx]]
                if dual_tournament.decider.is_first_player_won is None and potential_winner is not None:
                    dual_tournament.decider.is_first_player_won =\
                    (dual_tournament.decider.participant[0].name == potential_winner.name)
        for dual_tournament in self.dual_tournament_groups:
            dual_tournament.finish_matches_intelligently()


# For week not yet started, no need to actually play all games
class EmptyGrandmasterWeek(TournamentBase):
    def __init__(self, participants):
        self.participants = participants

    @classmethod
    def init_from_json(cls, json_value: dict, pool: GrandmasterPool):
        return cls(participants=pool.get_masters())

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

    def is_end_of_day(self):
        return True

    def finish_matches_intelligently(self):
        pass
