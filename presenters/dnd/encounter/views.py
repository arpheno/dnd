# Create your views here.
import json
from pprint import pprint

from django.http import JsonResponse
from django.utils.http import urlunquote
from django.views.generic import TemplateView
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from encounter.models import Character, Encounter
from monsters.browser import load_monsters, stat_to_mod, ability_to_stat
from party.browser import load_party
from region import build_random_encounter


class EncounterView(TemplateView):
    template_name = "encounter/encounter_detail.html"

    def get_context_data(self, **kwargs):
        context = super(EncounterView, self).get_context_data(**kwargs)
        party = load_party()
        encounter = build_random_encounter('Arctic', [2, 2, 2])
        pprint(encounter)
        context['encounter'] = json.dumps(encounter)
        context['party'] = json.dumps(list(x for x in party.values()))

        return context


class RandomEncounterView(TemplateView):
    template_name = "encounter/encounter_detail.html"

    def get_context_data(self, **kwargs):
        levels = [player.level for player in Character.objects.all()]
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
    # armor = serializers.StringRelatedField()

    class Meta:
        model = Character
        fields = ['id', 'name', 'scores', 'hitpoints', 'speed', 'alignment',
                  'monster_type', 'level', 'gold', 'experience', 'race', 'category']

    def create(self, validated_data):
        print(validated_data)
        return super(CharacterSerializer, self).create(validated_data)

    def modifiers(self):
        return {att: stat_to_mod[stat] for att, stat in zip(ability_to_stat, self.scores)}

    scores = serializers.DictField()


class CharacterDetailSerializer(ModelSerializer):
    armor = serializers.StringRelatedField()

    class Meta:
        model = Character
        fields = '__all__'


class CharacterViewSet(ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

class LevelView(TemplateView):
    template_name = "encounter/encounter_detail.html"

    def get_context_data(self, **kwargs):
        print(kwargs['cls'], kwargs['level'])
        levels = json.load(open('../../levels/5e-SRD-Levels.json'))
        for level in levels:
            if level['class']['name'].lower() == kwargs['cls'] and level['level'] == kwargs['level']:
                print(level)
                return level

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(
            context, safe=False,
            **response_kwargs
        )


class FeatureView(TemplateView):
    template_name = "encounter/encounter_detail.html"

    def get_context_data(self, **kwargs):
        features = json.load(open('../../levels/5e-SRD-Features.json'))
        for feature in features:
            if feature['index'] == kwargs['index']:
                print(feature)
                return feature

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(
            context, safe=False,
            **response_kwargs
        )


class naivejson(serializers.JSONField):
    def to_representation(self, value):
        try:
            res = json.dumps(eval(value))
            print(res)
            return res
        except:
            print(value)
            return json.dumps(value)


class EncounterSerializer(ModelSerializer):
    members = naivejson()
    map = naivejson()

    class Meta:
        model = Encounter
        fields = '__all__'


class EncounterViewSet(ModelViewSet):
    queryset = Encounter.objects.all()
    serializer_class = EncounterSerializer
