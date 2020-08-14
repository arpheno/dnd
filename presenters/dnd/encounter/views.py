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
from equipment.models import Trait, Spell, AdventuringGear, Weapon, Armor
from equipment.views import TraitSerializer, SpellSerializer, AdventuringGearSerializer
from monsters.browser import load_monsters
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
    class Meta:
        model = Character
        fields = ['id', 'name', 'scores', 'modifiers', 'hitpoints', 'speed', 'alignment',
                  'monster_type', 'level', 'gold', 'experience', 'race', 'category', 'ac', 'armor','traits','known_spells'
                  ,'adventuringgear_set','weapon_set']

    def create(self, validated_data):
        print(validated_data)
        return super(CharacterSerializer, self).create(validated_data)

    scores = serializers.DictField()
    modifiers = serializers.DictField()
    traits = TraitSerializer(many=True,read_only=True)
    known_spells = SpellSerializer(many=True,read_only=True)
    adventuringgear_set = AdventuringGearSerializer(many=True,read_only=True)

class CharacterCreateSerializer(ModelSerializer):
    class Meta:
        model = Character
        fields = ['name', 'scores', 'alignment', 'race', 'category', 'traits','max_hitpoints','speed']

    traits = TraitSerializer(many=True, validators=[], required=False)
    scores = serializers.DictField()

    def validate_traits(self):
        print("ASH")
        return True

    def run_validation(self, data):
        traits = data.pop('traits')
        known_spells = data.get('known_spells') and data.pop('known_spells')
        data = super(CharacterCreateSerializer, self).run_validation(data)
        data['traits'] = traits
        data['known_spells'] = known_spells
        return data

    def create(self, validated_data):
        traits = validated_data.pop('traits')
        spells = validated_data.pop('known_spells')
        validated_data['hitpoints']=validated_data['max_hitpoints']
        character = Character(**validated_data)
        character.save()
        for trait in traits:
            if trait['type']=='spell':
                try:
                    spell = Spell.objects.get(name__iexact=trait['name'])
                    spell.save()
                    spell.known_by.add(character)
                except Spell.DoesNotExist:
                    print(f"Can't find spell {trait['name']}")
            elif trait['type']=='gear':
                for kls in [AdventuringGear,Weapon,Armor]:
                    try:
                        o=kls.objects.get(name__iexact=trait['name'])
                        o.owners.add(character)
                        break
                    except kls.DoesNotExist:
                        pass
                    except Exception as e:
                        print(e)
                        print(trait)
                        break
                else:
                    # a=AdventuringGear(name=trait['name'],description='none',cost=0,weight=0,category='stuff')
                    # a.save()
                    # a.owners.add(character)
                    print(f"Couldnt find a class for {trait}")
            else:
                try:
                    t= Trait.objects.get(name=trait['name'])
                except Trait.DoesNotExist:
                    t= Trait(name=trait['name'], type=trait['type'], description=trait.get('description', ''))
                    t.save()
                character.traits.add(t)
        return character


class CharacterViewSet(ModelViewSet):
    queryset = Character.objects.all()
    def partial_update(self, request, *args, **kwargs):
        return super(CharacterViewSet, self).partial_update(request,*args,**kwargs)
    def get_serializer_class(self):
        if self.action == 'create':
            return CharacterCreateSerializer
        else:
            return CharacterSerializer


class LevelView(TemplateView):
    template_name = "encounter/encounter_detail.html"

    def get_context_data(self, **kwargs):
        levels = json.load(open(f'{os.path.dirname(__file__)}/levels/5e-SRD-Levels.json'))
        for level in levels:
            if level['class']['name'].lower() == kwargs['cls'].lower() and level['level'] == kwargs['level']:
                print(level)
                return level

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(
            context, safe=False,
            **response_kwargs
        )


class LevelView(TemplateView):
    template_name = "encounter/encounter_detail.html"

    def get_context_data(self, **kwargs):
        print(kwargs['cls'], kwargs['level'])
        levels = json.load(open(f'{os.path.dirname(__file__)}/levels/5e-SRD-Levels.json'))
        for level in levels:
            if level['class']['name'].lower() == kwargs['cls'].lower() and level['level'] == kwargs['level']:
                print(level)
                return level

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(
            context, safe=False,
            **response_kwargs
        )


import os


class FeatureView(TemplateView):
    template_name = "encounter/encounter_detail.html"

    def get_context_data(self, **kwargs):
        features = json.load(open(f'{os.path.dirname(__file__)}/levels/5e-SRD-Features.json'))
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
    players = naivejson()

    class Meta:
        model = Encounter
        fields = '__all__'


class EncounterViewSet(ModelViewSet):
    queryset = Encounter.objects.all()
    serializer_class = EncounterSerializer
