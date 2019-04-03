import json


def parse(thing, prefix=''):
    for key, value in thing.items():
        print(f'{prefix}{key}:{type(value)}')
        if isinstance(value, list):
            parse(value[0], prefix=prefix + '  ')
        if isinstance(value,dict):
            parse(value,prefix=prefix + '  ')


if __name__ == '__main__':
    content = json.load(open('5e-SRD-Classes.json'))
    parse(content[0])
