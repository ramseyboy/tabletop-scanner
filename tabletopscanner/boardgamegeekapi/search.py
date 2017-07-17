import xml.etree.cElementTree as et
from collections import OrderedDict

from tabletopscanner.boardgamegeekapi.parsers import Deserializer


class SearchParser(Deserializer):
    def deserialize(self, xml):
        tree = et.fromstring(xml)
        return [SearchParser.__make_search_result(el) for el in tree.findall('item')]

    @staticmethod
    def __make_search_result(el):
        geekid = geekid = el.attrib['id']
        name = el.find('name').attrib['value']
        yearpublished = el.find('yearpublished').attrib['value']

        return OrderedDict({
            'geekid': geekid,
            'name': name,
            'yearpublished': yearpublished
        })
