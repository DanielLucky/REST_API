# Создаем свои сериалайзеры
import pprint


def serializer_find(data: dict):
    dreams = {}

    for dr in data:
        dream = [{
            '_id': str(dr['_id']),
            'title': dr['title'],
            'done': dr['done'],
            'date': dr['date']
        }]

        dreams.setdefault([dr['author']][0], [])
        dreams[[dr['author']][0]] += dream

    return dreams


def serializer_find_one(data: dict):
    dream = {
        data['author']: {
            '_id': str(data['_id']),
            'title': data['title'],
            'done': data['done'],
            'date': data['date']
        }
    }

    return dream


def serializer_find_all(data: dict):
    dreams = []
    for dream in data:
        l = [{
            '_id': str(dream['_id']),
            'title': dream['title'],
            'done': dream['done'],
            'date': dream['date'],
            'author': dream['author']
        }]
        dreams += l

    return dreams
