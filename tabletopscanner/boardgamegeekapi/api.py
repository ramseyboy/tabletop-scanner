import time
import urllib.parse
import urllib.request

from tabletopscanner.boardgamegeekapi.game import GameParser
from tabletopscanner.boardgamegeekapi.price import PriceParser


class BggApi:
    DEFAULT_202_RETRY_TIMES = 5
    DEFAULT_RETRY_DELAY = 5

    def __init__(self, username):
        self.bgg_thing_url = "https://www.boardgamegeek.com/xmlapi2/thing?{0}"
        self.bgg_collection_url = "https://www.boardgamegeek.com/xmlapi2/collection?{0}"
        self.board_game_prices_url = "https://www.boardgameprices.com/api/public/bggRedirect/{0}"
        self.username = username

        self.game_parser = GameParser()
        self.price_parser = PriceParser()

    def request_game(self, geekid):
        """
        :return:
        :raises: BggException if request failed
        """
        query_params = {'id': geekid}
        url = self.bgg_thing_url.format(urllib.parse.urlencode(query_params))

        xml = BggApi.__make_request(url)

        game = self.game_parser.deserialize(xml.read())
        games = self.add_price_to_games(game)

        return games

    def request_buy_list(self):
        """
        :return:
        :raises: BggException if request or retry after processing failed
        """
        query_params = {'username': self.username, 'wanttobuy': 1}
        url = self.bgg_collection_url.format(urllib.parse.urlencode(query_params))

        xml = BggApi.__request_collection(url)

        games = self.game_parser.deserialize(xml)
        games = self.add_price_to_games(games)

        return games

    def request_play_list(self):
        """

        :return:
        :raises: BggException if request or retry after processing failed
        """
        query_params = {'username': self.username, 'wanttoplay': 1}
        url = self.bgg_collection_url.format(urllib.parse.urlencode(query_params))

        xml = BggApi.__request_collection(url)

        games = self.game_parser.deserialize(xml)
        games = self.add_price_to_games(games)

        return games

    def add_price_to_games(self, games):
        for game in games:
            prices = self.request_price(game['geekid'])
            game['prices'] = prices
        return games

    def request_price(self, bgg_id):
        url = self.board_game_prices_url.format(bgg_id)
        headers = {'Content-Type': 'application/json',
                   'application/json': 'application/json',
                   'X-Requested-With': 'XMLHttpRequest'}

        html = BggApi.__make_request(url).read().decode("utf-8")
        prices = self.price_parser.deserialize(html)
        return prices

    @staticmethod
    def __request_collection(url):
        """
        :param url: url for http request
        :return: xml body of http response
        :raises: BggException
        """
        res = BggApi.__make_request(url)

        if res.status >= 400:
            BggApi.__process_error(res)

        res = BggApi.__process_response(url, res)

        # return xml response body
        return res.read()

    @staticmethod
    def __process_response(url, response):
        """

        :param response: HttpResponse object
        :return: response or response after retry
        :raises: BggException
        """
        if response.status == 202:
            try:
                return BggApi.__retry(url, times=BggApi.DEFAULT_RETRY_DELAY)
            except RetryException as e:
                msg = "Error occurred when processing BoardGameGeek data, could not wait for processing, retry"
                raise BggException(msg, 500)
            except BggException as be:
                raise be
        else:
            return response

    @staticmethod
    def __retry(url, times):
        """
        :param url: the url for the request
        :param times: times to retry after receiving an HTTP 202
        :raises: RetryException if calls still are processing after n retries
        :raises: BggException if response contains an HTTP error
        :return: response after retry
        """
        if times == 0:
            raise RetryException("Retry failed, unable to process collection")

        res = BggApi.__make_request(url)
        if res.status >= 400:
            BggApi.__process_error(res)
        elif res.status == 202:
            time.sleep(BggApi.DEFAULT_RETRY_DELAY)
            return BggApi.__retry(url, times=times - 1)
        else:
            return res

    @staticmethod
    def __make_request(url, headers=None):
        req = urllib.request.Request(url)

        if headers is not None:
            for key, value in headers.items():
                req.add_header(key, value)

        resp = urllib.request.urlopen(req)
        return resp

    @staticmethod
    def __process_error(response):
        """
        raises a BggException based on http error type
        :param response: {@link HttpResponse}
        :raises: BggException
        """
        msg = "Error occurred when processing BoardGameGeek data. Request failed with status code: {0}"
        raise BggException(msg.format(response.status), response.status)


class RetryException(Exception):
    pass


class BggException(Exception):
    def __init__(self, message, status_code):
        super(BggException, self).__init__(message)

        self.status_code = status_code
