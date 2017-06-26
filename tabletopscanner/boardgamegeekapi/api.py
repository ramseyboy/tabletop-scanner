import time
import urllib.parse
import urllib.request

from tabletopscanner.boardgamegeekapi.parser import deserialize


class BggApi:
    DEFAULT_202_RETRY_TIMES = 5
    DEFAULT_RETRY_DELAY = 5

    def __init__(self, username):
        self.base_url = "https://www.boardgamegeek.com/xmlapi2/collection?{0}"
        self.username = username

    def request_buy_list(self):
        """
        :return:
        :raises: BggException if request or retry after processing failed
        """
        query_params = {'username': self.username, 'wanttobuy': 1}
        url = self.base_url.format(urllib.parse.urlencode(query_params))

        xml = BggApi.__request_collection(url)

        games = deserialize(xml)
        return games

    def request_play_list(self):
        """

        :return:
        :raises: BggException if request or retry after processing failed
        """
        query_params = {'username': self.username, 'wanttoplay': 1}
        url = self.base_url.format(urllib.parse.urlencode(query_params))

        xml = BggApi.__request_collection(url)
        games = deserialize(xml)
        return games

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
    def __make_request(url):
        return urllib.request.urlopen(url)

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
