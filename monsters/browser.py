import glob
import json
import os
from collections import ChainMap

from cr_to_xp import cr_to_xp

stat_to_mod = [-5, -5, -4, -4, -3, -3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10,
               10,
               10, 10]


def cr_to_proficiency(cr):
    try:
        if  int(cr) < 5:
            return 2
        if 5 <= int(cr) < 9:
            return 3
        elif 9 <= int(cr) < 13:
            return 4
        elif 9 <= int(cr) < 13:
            return 4
        elif 13 <= int(cr) < 17:
            return 5
        elif 17 <= int(cr) < 21:
            return 6
        elif 21 <= int(cr) < 25:
            return 7
        else:
            return 2
    except:
        return 2


def _load_monsters():
    paths = [path for path in glob.glob(f'{os.path.dirname(__file__)}/raws/json/**/*.json')]
    paths = paths + [path for path in glob.glob(f'{os.path.dirname(__file__)}/raws/json/*.json')]
    monsters = dict(ChainMap(*[json.load(open(path)) for path in paths]))
    return monsters


def load_monsters():
    with open(f'{os.path.dirname(__file__)}/monsters.json') as f:
        print('loading monsters')
        return json.load(f)


ability_to_stat = ['str', 'dex', 'con', 'int', 'wis', 'cha', ]

if __name__ == '__main__':
    monsters = _load_monsters()
    for monster in monsters.values():
        try:
            print('.', end='')
            monster['proficiency_bonus'] = cr_to_proficiency(monster['challenge_rating'])
            monster['modifiers'] = {att: stat_to_mod[stat] for att, stat in zip(ability_to_stat, monster['scores'])}
            monster['xp'] = cr_to_xp.get(monster['challenge_rating'],0)
            try:
                monster['saves'] = [True if save else False for save in monster['saves']]
            except:
                monster['saves']= [False]*6
            for attack in monster['attacks']:
                stat = ability_to_stat[attack['ability'] - 1]
                attack['to_hit'] = monster['proficiency_bonus'] + monster['modifiers'][stat]
        except:
            print(monster['name'])
            raise
    with open(f'{os.path.dirname(__file__)}/monsters.json', 'w') as f:
        json.dump(monsters, f)
