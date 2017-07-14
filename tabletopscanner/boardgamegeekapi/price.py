import json
import re

from tabletopscanner.boardgamegeekapi.parsers import Deserializer


class Price:
    def __init__(self, gameid, collectionid, name, yearpublished, image, thumbnail):
        self.gameid = gameid
        self.collectionid = collectionid
        self.name = name
        self.yearpublished = yearpublished
        self.image = image
        self.thumbnail = thumbnail


class PriceParser(Deserializer):
    def deserialize(self, html):
        pattern = re.compile(r'<script>var prices = (.*?)</script>', re.MULTILINE | re.DOTALL)
        matches = re.findall(pattern, string=html)
        if len(matches) > 0:
            prices = PriceParser.__combine_prices(matches)
            return prices
        else:
            raise RuntimeError()

    @staticmethod
    def __combine_prices(json_lists):
        combined = []
        for lists in json_lists:
            prices = json.loads(lists)
            if len(prices) > 0:
                for price in prices:
                    combined.append(price)
        return combined
