import Util


class DualTournament:
    def __init__(self, participants, results):
        self.participants = participants
        self.initials, self.winners, self.elimination, self.decider = results

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


class Tournament:
    def __init__(self, participants, results):
        self.participants = participants
        self.quarterfinals, self.semifinals, self.final = results

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


class GrandmasterWeek:
    def __init__(self, dual_tournament_groups, tournament):
        self.dual_tournament_groups = dual_tournament_groups
        self.tournament = tournament

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


# For week not yet started, no need to actually play all games
class EmptyGrandmasterWeek:
    def __init__(self, participants):
        self.participants = participants

    def finish(self):
        Util.shuffle(self.participants)
        score_table = [5, 4, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0]
        for idx in range(len(self.participants)):
            self.participants[idx].receive(score_table[idx])

    def validate(self):
        assert(len(self.participants) == 16)


def to_dict(week):
    if isinstance(week, EmptyGrandmasterWeek):
        return dict()
    result = dict()
    result['dual_tournament_groups'] = [dual_tournament_to_dict(dt) for dt in week.dual_tournament_groups]
    result['tournament'] = tournament_to_dict(week.tournament)
    return result


def from_dict(week_json, pool):
    if not week_json:
        return None
    groups_json = week_json['dual_tournament_groups']
    dual_tournament_groups = [dual_tournament_from_dict(group_json, pool) for group_json in groups_json]
    tournament = tournament_from_dict(week_json['tournament'], pool)
    return GrandmasterWeek(dual_tournament_groups, tournament)


def dual_tournament_to_dict(dual_tournament):
    if dual_tournament is None:
        return None
    result = dict()
    result['initials'] = [match_to_dict(initial) for initial in dual_tournament.initials]
    result['winners'] = match_to_dict(dual_tournament.winners)
    result['elimination'] = match_to_dict(dual_tournament.elimination)
    result['decider'] = match_to_dict(dual_tournament.decider)
    return result


def dual_tournament_from_dict(group_json, pool):
    if group_json is None:
        return None
    initials = [match_from_dict(initials, pool) for initials in group_json['initials']]
    winners = match_from_dict(group_json['winners'], pool)
    elimination = match_from_dict(group_json['elimination'], pool)
    decider = match_from_dict(group_json['decider'], pool)
    return DualTournament(None, (initials, winners, elimination, decider))


def tournament_to_dict(tournament):
    if tournament is None:
        return None
    result = dict()
    result['quarterfinals'] = [match_to_dict(quarterfinal) for quarterfinal in tournament.quarterfinals]
    result['semifinals'] = [match_to_dict(semifinal) for semifinal in tournament.semifinals]
    result['final'] = match_to_dict(tournament.final)
    return result


def tournament_from_dict(tournament, pool):
    if tournament is None:
        return None
    quarterfinals = [match_from_dict(quarterfinal, pool) for quarterfinal in tournament['quarterfinals']]
    semifinals = [match_from_dict(semifinal, pool) for semifinal in tournament['semifinals']]
    final = match_from_dict(tournament['final'], pool)
    return Tournament(None, (quarterfinals, semifinals, final))


def match_to_dict(match):
    if match is None:
        return None
    return [match[0].name, match[1].name]


def match_from_dict(match, pool):
    if match is None:
        return None
    return pool.get_master_by_name(match[0]), pool.get_master_by_name(match[1])
