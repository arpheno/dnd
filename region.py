import random
from pprint import pprint

import pandas as pd

from cr_to_xp import _cr, cr_to_xp
from monsters.browser import load_monsters

encounter_budget = '''\
    25  50  75  100
    50  100 150 200
    75  150 225 400
    125 250 375 500
    250 500 750 1100
 300 600 900 1400
350 750 1100 1700
 450 900 1400 2100
 550 1100 1600 2400
 600 1200 1900 2800
 800 1600 2400 3600
1000 2000 3000 4500
 1100 2200 3400 5100
 1250 2500 3800 5700 
 1400 2800 4300 6400
  1600 3200 4800 7200
 2000 3900 5900 8800
 2100 4200 6300 9500
 2400 4900 7300 10900
 2800 5700 8500 12700
'''
a = [line.strip() for line in encounter_budget.splitlines()]
b = zip(*[line.split() for line in a])
easy, medium, hard, deadly = (list(b))
difficulties = {}
difficulties[0] = dict(enumerate([int(x) for x in easy], start=1))
difficulties[1] = dict(enumerate([int(x) for x in medium], start=1))
difficulties[2] = dict(enumerate([int(x) for x in hard], start=1))
difficulties[3] = dict(enumerate([int(x) for x in deadly], start=1))
pprint(difficulties)

monsters = load_monsters()


def build_encounter_tokens(levels, difficulty=1):
    print(f'Party of {len(levels)}')
    xp_budget = sum(difficulties[difficulty][level] for level in levels)
    print(f'Experience budget: {xp_budget}')
    encounter = []
    horde_modifier = [0, 1, 1.5, 2, 2, 2, 2, 2.5, 2.5, 2.5, 2.5]
    while sum(encounter) * horde_modifier[len(encounter)] < xp_budget:
        encounter.append(random.choice([x for x in cr_to_xp.values() if x <= xp_budget]))
    print(encounter)
    return encounter


import os


def build_random_encounter(biome, levels, difficulty=1):
    biomes = pd.read_csv(f'{os.path.dirname(__file__)}/monsters/raws/biomes.csv')
    biomes['CR'] = biomes['CR'].str.strip()
    biomes['XP'] = biomes['CR'].map(cr_to_xp)
    encounter = build_encounter_tokens(levels, difficulty)
    mon = pd.concat([biomes[biomes.XP == mob][biomes[biome] == 'YES'].sample(1) for mob in encounter])['Name'].tolist()
    return mon


def monster_details(mon):
    return monsters[mon]


if __name__ == '__main__':
    biome = 'Arctic'
    biome = 'Underdark'
    pprint(build_random_encounter('Arctic', [1, 1, 1]))
    pprint(build_encounter_tokens([2, 2, 2], 1))
''''''
