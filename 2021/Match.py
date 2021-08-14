import random
import typing
from abc import abstractmethod, ABCMeta

from GrandmasterPool import GrandmasterPool
from Grandmaster import GrandMaster


class Serializable(metaclass=ABCMeta):
    @abstractmethod
    def init_from_json(self, json_value: dict, pool: GrandmasterPool):
        pass

    @abstractmethod
    def export(self) -> dict:
        pass


class Match(Serializable):
    participants: typing.List[GrandMaster]
    is_first_player_won: typing.Optional[bool] = None

    def __init__(self, participants: typing.List[typing.Optional[GrandMaster]],
                 is_first_player_won: typing.Optional[bool] = None):
        assert(len(participants) == 2)
        self.participants = participants
        self.is_first_player_won = is_first_player_won

    @classmethod
    def init_from_json(cls, json_value: dict, pool: GrandmasterPool):
        if json_value is None:
            return None
        participants = [pool.get_master_by_name(participant) for participant in json_value['participants']]
        is_first_player_won = json_value['is_first_player_won']
        return cls(participants, is_first_player_won)

    def export(self) -> dict:
        result = dict()
        result['participants'] = [participant.name if participant is not None else ''
                                  for participant in self.participants]
        result['is_first_player_won'] = self.is_first_player_won
        return result

    def finish(self):
        assert(self.participants[0] is not None and self.participants[1] is not None)
        if self.is_first_player_won is None:
            self.is_first_player_won = bool(random.getrandbits(1))

    def get_winner(self):
        winner_idx = 0 if self.is_first_player_won else 1
        return self.participants[winner_idx]

    def get_loser(self):
        loser_idx = 1 if self.is_first_player_won else 0
        return self.participants[loser_idx]
