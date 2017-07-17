import json
import xml.etree.cElementTree as et
from collections import OrderedDict

from tabletopscanner.boardgamegeekapi.parsers import Deserializer, Serializer


class GameParser(Serializer, Deserializer):
    def serialize(self, games):
        return json.dumps(games, indent=4)

    def deserialize(self, xml):
        tree = et.fromstring(xml)
        return [GameParser.__make_game(el) for el in tree.findall('item')]

    @staticmethod
    def __make_game(el):

        geekid = None
        try:
            geekid = el.attrib['objectid']
        except KeyError:
            geekid = el.attrib['id']

        name = None
        try:
            name = el.find('name').text
        except KeyError:
            name = el.find('name').attrib['value']

        yearpublished = None
        try:
            yearpublished = el.find('yearpublished').text
        except KeyError:
            yearpublished = el.find('yearpublished').attrib['value']

        description = None
        try:
            description = el.find('description').text
        except KeyError:
            # no description
            pass

        return OrderedDict({
            'geekid': geekid,
            'name': name,
            'yearpublished': yearpublished,
            'image': el.find('image').text,
            'thumbnail': el.find('thumbnail').text,
            'description': description,
            'prices': None
        })
