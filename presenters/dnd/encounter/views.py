# Create your views here.
import json
from pprint import pprint

from django.http import JsonResponse
from django.utils.http import urlunquote
from django.views.generic import TemplateView
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from encounter.models import Character, Armor, Attack
from monsters.browser import load_monsters
from party.browser import load_party
from region import build_random_encounter


class EncounterView(TemplateView):
    template_name = "encounter/encounter_detail.html"

    def get_context_data(self, **kwargs):
        context = super(EncounterView, self).get_context_data(**kwargs)
        party = load_party()
        encounter = build_random_encounter('Arctic', [1, 1, 1])
        pprint(encounter)
        context['encounter'] = json.dumps(encounter)
        context['party'] = json.dumps(list(x for x in party.values()))

        return context


class RandomEncounterView(TemplateView):
    template_name = "encounter/encounter_detail.html"

    def get_context_data(self, **kwargs):
        levels = [player['challenge_rating'] for player in load_party().values()]
        encounter = build_random_encounter(self.kwargs['biome'], levels, self.kwargs['difficulty'])
        pprint(encounter)
        context = encounter

        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(
            context, safe=False,
            **response_kwargs
        )


class PartyDetailView(TemplateView):
    template_name = "encounter/encounter_detail.html"

    def get_context_data(self, **kwargs):
        return list(x for x in load_party().values())

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(
            context, safe=False,
            **response_kwargs
        )


class MonsterDetailView(TemplateView):
    template_name = "encounter/encounter_detail.html"

    def get_context_data(self, **kwargs):
        m = load_monsters()[urlunquote(self.kwargs['slug'])]
        print(m)
        return m

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(
            context, safe=False,
            **response_kwargs
        )


class CharacterSerializer(ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'


class CharacterViewSet(ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class ArmorSerializer(ModelSerializer):
    class Meta:
        model = Armor
        fields = '__all__'


class ArmorViewSet(ModelViewSet):
    queryset = Armor.objects.all()
    serializer_class = ArmorSerializer


class AttackSerializer(ModelSerializer):
    class Meta:
        model = Attack
        fields = '__all__'


class AttackViewSet(ModelViewSet):
    queryset = Attack.objects.all()
    serializer_class = AttackSerializer
