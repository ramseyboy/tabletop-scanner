import json


class Game:
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
