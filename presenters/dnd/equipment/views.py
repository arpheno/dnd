# Create your views here.
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from equipment.models import Weapon, Armor, AdventuringGear, Damage, Trait, Spell


class DamageSerializer(ModelSerializer):
    class Meta:
        model = Damage
        fields = ('dice_count', 'dice_value', 'type')


class WeaponSerializer(ModelSerializer):
    class Meta:
        model = Weapon
        fields = ('id', 'name', 'description', 'damages')
        depth = 3

    damages = DamageSerializer(many=True, read_only=True)


class WeaponViewSet(ModelViewSet):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializer


class ArmorSerializer(ModelSerializer):
    class Meta:
        model = Armor
        fields = '__all__'
        depth = 3


class ArmorViewSet(ModelViewSet):
    queryset = Armor.objects.all()
    serializer_class = ArmorSerializer


class AdventuringGearSerializer(ModelSerializer):
    class Meta:
        model = AdventuringGear
        fields = '__all__'
        depth = 3


class AdventuringGearViewSet(ModelViewSet):
    queryset = AdventuringGear.objects.all()
    serializer_class = AdventuringGearSerializer


class TraitSerializer(ModelSerializer):
    class Meta:
        model = Trait
        fields = ('name', 'type', 'description')
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class TraitViewSet(ModelViewSet):
    queryset = Trait.objects.all()
    serializer_class = TraitSerializer
    lookup_field = 'name'


class SpellSerializer(ModelSerializer):
    class Meta:
        model = Spell
        fields = '__all__'
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class SpellViewSet(ModelViewSet):
    queryset = Spell.objects.all()
    serializer_class = SpellSerializer
    lookup_field = 'name'
