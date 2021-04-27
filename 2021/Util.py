import os
import random


def is_aws():
    return os.environ['API_KEY'].startswith('AQI')


def coin_flip(player1, player2):
    # hard coding for 15-people NA grandmaster
    if player1.name == '-':
        return player2, player1
    elif player2.name == '-':
        return player1, player2
    if bool(random.getrandbits(1)):
        return player1, player2
    else:
        return player2, player1


def shuffle(participants):
    random.shuffle(participants)
    minus_idx = -1
    for idx in range(len(participants)):
        if participants[idx].name == '-':
            minus_idx = idx
    if minus_idx != -1:
        participants[-1], participants[minus_idx] = participants[minus_idx], participants[-1]
