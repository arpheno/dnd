# Create your models here.
from django.db import models
from django.db.models import Model

from encounter.models import Character


class Inventory(Model):
    character = models.OneToOneField('encounter.Character',on_delete='DELETE')
    weapons = models.ManyToManyField('equipment.Weapon')
    armors = models.ManyToManyField('equipment.Armor')
    gear = models.ManyToManyField('equipment.AdventuringGear')

    def __str__(self):
        return f'{self.name} ({self.category} {self.base_ac})'


