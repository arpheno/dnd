"""dnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dnd import settings
from encounter.views import EncounterView, RandomEncounterView, MonsterDetailView, PartyDetailView, CharacterViewSet, \
    LevelView, FeatureView, EncounterViewSet
from equipment.views import WeaponViewSet, ArmorViewSet, AdventuringGearViewSet
# Create a router and register our viewsets with it.
from quests.views import AdventureViewSet, QuestViewSet

router = DefaultRouter()
router.register(r'characters', CharacterViewSet)
router.register(r'encounters', EncounterViewSet)
router.register(r'armors', ArmorViewSet)
router.register(r'weapons', WeaponViewSet)
router.register(r'adventuring_gear', AdventuringGearViewSet)
router.register(r'quests', QuestViewSet)
router.register(r'adventures', AdventureViewSet)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('encounter/', EncounterView.as_view()),
                  path('random_encounter/<str:biome>/<int:difficulty>', RandomEncounterView.as_view()),
                  path(r'monster/<str:slug>/', MonsterDetailView.as_view()),
                  path(r'api/classes/<str:cls>/level/<int:level>', LevelView.as_view()),
                  path(r'api/features/<int:index>', FeatureView.as_view()),
                  path(r'party/', PartyDetailView.as_view()),
                  path('', EncounterView.as_view()),
                  url(r'^api/', include(router.urls))

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
