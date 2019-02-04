import glob
import json
import os
from collections import ChainMap

stat_to_mod = [-5, -5, -4, -4, -3, -3, -2, -2, -1, -1, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10,
               10, 10]


def cr_to_proficiency(cr):
    try:
        if 5 <= int(cr) < 9:
            return 3
        elif 9 <= int(cr) < 13:
            return 4
        else:
            return 2
    except:
        return 2


def _load_party():
    paths = [path for path in glob.glob(f'{os.path.dirname(__file__)}/raws/json/*.json')]
    monsters = dict(ChainMap(*[json.load(open(path)) for path in paths]))
    return monsters


def load_party():
    with open(f'{os.path.dirname(__file__)}/party.json') as f:
        print('loading party')
        return json.load(f)


ability_to_stat = ['str', 'dex', 'con', 'int', 'wis', 'cha',]

if __name__ == '__main__':
    party = _load_party()
    for member in party.values():
        print('.', end='')
        member['proficiency_bonus'] = cr_to_proficiency(member['challenge_rating'])
        member['modifiers'] = {att: stat_to_mod[stat] for att, stat in zip(ability_to_stat, member['scores'])}
        for attack in member['attacks']:
            stat = ability_to_stat[attack['ability']-1]
            attack['to_hit'] = member['proficiency_bonus'] + member['modifiers'][stat]
    with open(f'{os.path.dirname(__file__)}/party.json', 'w') as f:
        json.dump(party, f)
