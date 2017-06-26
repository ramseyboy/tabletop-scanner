import xml.etree.cElementTree as et

from tabletopscanner.boardgamegeekapi.game import Game


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
