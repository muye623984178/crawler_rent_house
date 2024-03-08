import json

person = {
    'basic': {
        'name': 'jx',
        'age': 22,
        'sex': '男',
        'merry': False
    },
    'work': {
        'position': 'engineer',
        'department': None
    }
}

person_json = json.dumps(person)
print(person_json)
print(type(person_json))
person_dict = json.loads(person_json)
print(person_dict)
print(type(person_dict))
print(person_dict['basic']['name'])