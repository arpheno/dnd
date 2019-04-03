from equipment.models import Armor, WeaponProperty, Weapon, Damage, AdventuringGear
from equipment_raw.generate import _load_armors, _load_weapon_properties

cost_map = {
    'gp': 100,
    'ep': 50,
    'sp': 10,
    'cp': 1
}
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        self.hangle_armors()
        self.handle_weapon_properties()
        self.handle_weapons()
        self.handle_adventuring_gear()

    def handle_weapons(self):
        l = _load_armors()
        Entity = Weapon
        all_objects = set(o.name for o in Entity.objects.all())
        for e in l:
            if e['equipment_category'] == 'Weapon':
                print(e)
                name = e['name']
                description = e.get('Special','')
                category = e.get('weapon_category',e.get('weapon_category:'))
                ability = 0 if e['weapon_range'] == 'Melee' else 1
                cost = e['cost']['quantity'] * cost_map[e['cost']['unit']]
                weight = e['weight']
                a = Entity(
                    name=name,
                    description=description,
                    category=category,
                    ability=ability,
                    cost=cost,
                    weight=weight
                )
                if name not in all_objects:
                    a.save()
                    for prop in e['properties']:
                        a.properties.add(WeaponProperty.objects.get(name=prop['name']))
                        a.save()
                    dice_count = e['damage']['dice_count']
                    dice_value = e['damage']['dice_value']
                    damage_type = e['damage']['damage_type']['name']
                    obj,created = Damage.objects.get_or_create(dice_count=dice_count, dice_value=dice_value, type=damage_type)
                    print(obj)
                    a.damages.add(obj)

                    a.save()

    def handle_adventuring_gear(self):
        l = _load_armors()
        all_objects = set(o.name for o in AdventuringGear.objects.all())
        for e in l:
            if e['equipment_category'] == 'Adventuring Gear' and not e['gear_category'] == 'Equipment Pack':
                name = e['name']
                description = e.get("desc",'')
                if isinstance(description,list):
                    description='\n'.join(description)
                cost = e['cost']['quantity'] * cost_map[e['cost']['unit']]
                category=e['gear_category']
                weight = e['weight']
                a = AdventuringGear(
                    name=name,
                    description=description,
                    weight=weight,
                    cost=cost,
                    category=category
                )
                if name not in all_objects:
                    a.save()
    def handle_weapon_properties(self):
        l = _load_weapon_properties()
        all_objects = set(o.name for o in WeaponProperty.objects.all())
        for e in l:
            name = e['name']
            description = e["desc"]
            a = WeaponProperty(
                name=name,
                description=description,
            )
            if name not in all_objects:
                a.save()

    def hangle_armors(self):
        l = _load_armors()
        all_armors = set(armor.name for armor in Armor.objects.all())
        for e in l:
            if e['equipment_category'] == 'Armor':
                name = e['name']
                description = ""
                category = e['armor_category']
                base_ac = e['armor_class']['base']
                stealth_disadvantage = e['stealth_disadvantage']
                str_minimum = e['str_minimum']
                cost = e['cost']['quantity'] * cost_map[e['cost']['unit']]
                weight = e['weight']
                a = Armor(
                    name=name,
                    description=description,
                    category=category,
                    base_ac=base_ac,
                    cost=cost,
                    stealth_disadvantage=stealth_disadvantage,
                    str_minimum=str_minimum,
                    weight=weight
                )
                if name not in all_armors:
                    a.save()
