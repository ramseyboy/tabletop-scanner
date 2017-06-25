import xml.etree.cElementTree as et
import json


class Game():

    def __init__(self, gameid, collectionid, name, yearpublished, image, thumbnail):
        self.gameid = gameid
        self.collectionid = collectionid
        self.name = name
        self.yearpublished = yearpublished
        self.image = image
        self.thumbnail = thumbnail


class GameEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Game):
            return o.__dict__
        else:
            return json.JSONEncoder.default(self, o)


def serialize(games):
    return json.dumps(games, cls=GameEncoder, indent=4)


def deserialize(xml):
    tree = et.fromstring(xml)
    return [__make_game(el) for el in tree.findall('item')]


def __make_game(el):
    return Game(
        gameid=el.attrib['objectid'],
        collectionid=el.attrib['collid'],
        name=el.find('name').text,
        yearpublished=el.find('yearpublished').text,
        image=el.find('image').text,
        thumbnail=el.find('thumbnail').text)


if __name__ == '__main__':
    xml = open('resources/buylist.xml', 'r').read()
    games = deserialize(xml)
    print(games)
    print(serialize(games))
