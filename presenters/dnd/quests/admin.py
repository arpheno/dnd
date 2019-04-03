from django.contrib import admin
# Register your models here.
from django.contrib.admin import TabularInline

from quests.models import Adventure, Quest


class QuestsAdmin(TabularInline):
    model = Quest


@admin.register(Adventure)
class AdventureAdmin(admin.ModelAdmin):
    inlines = [QuestsAdmin]
