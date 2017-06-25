import urllib.request
import urllib.parse

class BggApi:

    def __init__(self, username):
        base_url = "https://www.boardgamegeek.com/xmlapi2/collection?{0}"
        query_params = {'username': username, 'wanttobuy': 1}
        self.url = base_url.format(urllib.parse.urlencode(query_params))

    def requestBuyList(self):
        print(self.url)
        return urllib.request.urlopen(self.url).read()
