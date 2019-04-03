from django.db import models

# Create your models here.
from django.db.models import Model


class Adventure(Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Quest(Model):
    adventure = models.ForeignKey('quests.Adventure', on_delete='cascade',related_name='quests')
    name = models.CharField(max_length=100, default='')
    description = models.TextField(null=True, blank=True)
    loot = models.TextField(null=True, blank=True)
    bluetext = models.TextField(null=True, blank=True)
    traps = models.TextField(null=True, blank=True)
    combat = models.TextField(null=True, blank=True)
    gold_reward = models.IntegerField(default=0)
    exp_reward = models.IntegerField(default=0)

    def __str__(self):
        return self.name
