from equipment.models import Spell


def transform(spell):
    spell['description'] = '\n'.join(spell['description'])
    spell['higher_level'] = '\n'.join(spell.get('higher_level', []))
    spell['components'] = '\n'.join(spell['components'])
    spell['school'] = spell['school']['name']
    spell['concentration'] = True if spell['concentration'] == 'yes' else False
    spell['ritual'] = True if spell['ritual'] == 'yes' else False
    del spell['index']
    del spell['url']
    del spell['classes']
    del spell['subclasses']
    del spell['page']
    return spell


import json

spells = json.load(open('/users/swozny/Downloads/5e-database-master/5e-SRD-Spells.json'))
transformed = [transform(spell) for spell in spells]
for spell in transformed:
    Spell(**spell).save()
