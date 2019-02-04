from django.db import models

# Create your models here.
from django.db.models import Model


class Armor(Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    type = models.CharField(max_length=30)
    ac = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name} ({self.type} {self.ac})'


class Character(Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)

    size = models.CharField(max_length=30)
    monster_type = models.CharField(max_length=30)
    alignment = models.CharField(max_length=30)
    speed = models.CharField(max_length=30)
    hitpoints = models.IntegerField()

    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    charisma = models.IntegerField()
    armor = models.ForeignKey(Armor, on_delete='NULL', null=True)


class Attack(Model):
    owners = models.ManyToManyField(Character)

    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    ability = models.IntegerField()
    dice_count = models.IntegerField()
    dice_type = models.IntegerField()
    damage_type = models.IntegerField()
