import json
import xml.etree.cElementTree as et

from tabletopscanner.boardgamegeekapi.parsers import Deserializer, Serializer


class Game:
    def __init__(self, gameid, collectionid, name, yearpublished, image, thumbnail, prices=None):
        self.gameid = gameid
        self.collectionid = collectionid
        self.name = name
        self.yearpublished = yearpublished
        self.image = image
        self.thumbnail = thumbnail
        self.prices = prices


class GameParser(Serializer, Deserializer):
    def serialize(self, games):
        return json.dumps(games, cls=GameEncoder, indent=4)

    def deserialize(self, xml):
        tree = et.fromstring(xml)
        return [GameParser.__make_game(el) for el in tree.findall('item')]

    @staticmethod
    def __make_game(el):
        return Game(
            gameid=el.attrib['objectid'],
            collectionid=el.attrib['collid'],
            name=el.find('name').text,
            yearpublished=el.find('yearpublished').text,
            image=el.find('image').text,
            thumbnail=el.find('thumbnail').text)


class GameEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Game):
            return o.__dict__
        else:
            return json.JSONEncoder.default(self, o)
