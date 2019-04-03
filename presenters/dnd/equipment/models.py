# Create your models here.
from django.db import models
from django.db.models import Model

from encounter.models import Character


class Armor(Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    category = models.CharField(max_length=30)
    base_ac = models.IntegerField(max_length=30)
    cost = models.IntegerField()
    stealth_disadvantage = models.BooleanField()
    str_minimum = models.IntegerField()
    weight = models.IntegerField()
    magical_bonus = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} ({self.category} {self.base_ac})'


class Weapon(Model):
    owners = models.ManyToManyField('encounter.Character')

    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    ability = models.IntegerField()
    category = models.CharField(max_length=30)
    cost = models.IntegerField()
    weight = models.IntegerField()
    magical_bonus = models.IntegerField(default=0)


class WeaponProperty(Model):
    owners = models.ManyToManyField('equipment.Weapon', related_name='properties')
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)


class Damage(Model):
    owners = models.ManyToManyField('equipment.Weapon', related_name='damages')
    dice_count = models.IntegerField()
    dice_value = models.IntegerField()
    type = models.CharField(max_length=30)


class AdventuringGear(Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    category = models.CharField(max_length=30)
    cost = models.IntegerField()
    weight = models.IntegerField()
