# Create your models here.
from django.db import models
from django.db.models import Model

from encounter.models import Character


class Armor(Model):
    owners = models.ManyToManyField("encounter.Character", related_name="armors")
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
        return f"{self.name} ({self.category} {self.base_ac})"


class Weapon(Model):
    owners = models.ManyToManyField("encounter.Character")

    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    ability = models.IntegerField()
    category = models.CharField(max_length=30)
    cost = models.IntegerField()
    weight = models.IntegerField()
    magical_bonus = models.IntegerField(default=0)


class WeaponProperty(Model):
    owners = models.ManyToManyField("equipment.Weapon", related_name="properties")
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)


class Damage(Model):
    owners = models.ManyToManyField("equipment.Weapon", related_name="damages")
    dice_count = models.IntegerField()
    dice_value = models.IntegerField()
    type = models.CharField(max_length=30)


class AdventuringGear(Model):
    owners = models.ManyToManyField("encounter.Character", null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    category = models.CharField(max_length=30)
    cost = models.IntegerField()
    weight = models.IntegerField()

    def __str__(self):
        return self.name


class Trait(Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(default="")
    type = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Spell(Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(default="")
    level = models.IntegerField()
    higher_level = models.TextField(default="")
    range = models.TextField(default="")
    ritual = models.BooleanField(default=False)
    duration = models.TextField(default="")
    casting_time = models.TextField(default="", null=True)
    components = models.CharField(max_length=20)
    school = models.CharField(max_length=20)
    material = models.TextField(default="")
    concentration = models.BooleanField(default=False)

    def __str__(self):
        return self.name
