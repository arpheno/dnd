from django.db import models

# Create your models here.
from django.db.models import Model, TextField

stat_to_modifier = [-5, -5, -4, -4, -3, -3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9,
                    10, 10, 10, 10]


def level_to_proficiency(cr):
    try:
        if int(cr) < 5:
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


class Character(Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    level = models.IntegerField(default=1)
    description = models.TextField(null=True)

    size = models.CharField(max_length=30)
    monster_type = models.CharField(max_length=30)
    race = models.CharField(max_length=30)
    alignment = models.CharField(max_length=30)
    speed = models.CharField(max_length=30)
    hitpoints = models.IntegerField()
    #max_hitpoints = models.IntegerField() TODO!

    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    charisma = models.IntegerField()
    gold = models.IntegerField()
    experience = models.IntegerField()
    armor = models.ForeignKey('equipment.Armor', on_delete='NULL', null=True)

    @property
    def scores(self):
        return dict(str=self.strength, dex=self.dexterity, con=self.constitution, int=self.intelligence,
                    wis=self.wisdom, cha=self.charisma)

    @scores.setter
    def scores(self, value):
        self.strength = value['str']
        self.dexterity = value['dex']
        self.constitution = value['con']
        self.intelligence = value['int']
        self.wisdom = value['wis']
        self.charisma = value['cha']

    @property
    def modifiers(self):
        return {key: stat_to_modifier[value] for key, value in self.scores.items()}

    @property
    def ac(self):
        dex_map = {
            'light': lambda x: x,
            'medium': lambda x: max(x, 2),
            'heavy': lambda x: 0,
        }
        dex_bonus = dex_map[self.armor.category](self.dexterity)
        return self.armor.base_ac + self.armor.magical_bonus + dex_bonus

    @property
    def saves(self):
        return [False] * 6 #TODO

    @property
    def skills(self):
        return []

    @property
    def attacks(self):
        return [] # TODO

    @property
    def languages(self):
        return []

    @property
    def passive_perception(self):
        return self.modifiers['wis'] + 10

    @property
    def proficiency_bonus(self):
        return level_to_proficiency(self.level)


class Encounter(models.Model):
    members = TextField(default='[]')
    map = TextField(default='[]')
