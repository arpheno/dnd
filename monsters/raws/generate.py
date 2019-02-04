import json

if __name__ == '__main__':
    name=input('name?')
    size,type,alignment= input("basic").split()
    ac = [int(input("ac")), "", False],
    hp = input("hp")
    hd = [int(x) for x in input("hd").split('d')]
    speed = input("speed")
    scores = [int(x) for x in input("scores").split(',')]
    damage_immunities=input('damage immunities?')
    damage_resistances=input('damage resistances?')
    damage_vulnerabilities=input('damage vulnerabilities?')
    condition_immunities=input('condition immunities?')
    senses=input('senses')
    languages=input('languages')
    challenge_rating=input('challenge rating?')
    a = input("more traits?")
    traits = []
    while a:
        aname = input("    name?")
        adescription = input("    description?")
        traits.append(dict(aname=aname, description=adescription))
        a = input("more traits?")

    attacks = []
    a = input("more attacks?")
    while a:
        aname = input("    aname?")
        ability = int(input("    ability?"))
        range = input("    range?")
        damage = [int(x) for x in input("    damage?").split('d')]
        damage_type = input("    damage type?")
        damage.append(damage_type)
        adescription = input("    description?")
        attacks.append(dict(name=aname, ability=ability, damage=damage, range=range, description=adescription))
        a = input("more attacks?")

    actions = []
    a = input("more actions?")
    while a:
        aname = input("    name?")
        adescription = input("    description?")
        actions.append(dict(aname=aname, description=adescription))
        a = input("more actions?")
    description = input('description?')

    monster = {
        name: dict(languages=languages,challenge_rating=challenge_rating,senses=senses,damage_immunities=damage_immunities,name=name, attacks=attacks, description=description, traits=traits, actions=actions, size=size,
                   type=type, alignment=alignment, speed=speed, ac=ac, hp=hp, hd=hd, scores=scores)}
    with open(f'{name}.json', 'w') as f:
        json.dump(monster, f, sort_keys=True, indent=4)
