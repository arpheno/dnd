import glob
import json

import os
from collections import ChainMap
from itertools import chain
from pprint import pprint


def _load_armors():
    paths = [path for path in glob.glob(f'{os.path.dirname(__file__)}/raws/json/5e-SRD-Equipment.json')]
    monsters = list(chain.from_iterable([json.load(open(path)) for path in paths]))
    return monsters

def _load_weapon_properties():
    paths = [path for path in glob.glob(f'{os.path.dirname(__file__)}/raws/json/5e-SRD-Weapon-Properties.json')]
    monsters = list(chain.from_iterable([json.load(open(path)) for path in paths]))
    return monsters
