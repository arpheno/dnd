from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Spell, AdventuringGear, Armor, Trait

admin.site.register(Spell)
admin.site.register(AdventuringGear)
admin.site.register(Armor)
admin.site.register(Trait)
