import json

from flask import render_template, make_response, url_for, request
from healthcheck import HealthCheck, EnvironmentDump

from tabletopscanner import app
from tabletopscanner.boardgamegeekapi.api import BggApi
from tabletopscanner.boardgamegeekapi.game import GameParser

api = BggApi('ramseyboy')
game_parser = GameParser()


@app.route('/')
def index():
    """
    Home page
    """
    return render_template('index.html'), 200


@app.errorhandler(404)
def not_found(error):
    """
    404 - Not Found route
    """
    return render_template('error.html'), 404


@app.route('/api', methods=['GET'])
def api_root():
    """
    Api root dir
    """
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if url.startswith('/api'):
                links.append({'url': url, 'method': rule.endpoint})

    return make_response(json.dumps(links, indent=4), 200, {'Content-Type': 'application/json'})


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route('/api/search', methods=['GET'])
def search():
    """
    Return search results from board game geek
    """
    q = request.args.get('q')
    if q is None or len(q) < 1:
        return make_response({'msg': 'must supply search query as \'q\' parameter'})

    games = api.search(q)

    return make_response(game_parser.serialize(games), 200, {'Content-Type': 'application/json'})


@app.route('/api/game/<path:geekid>', methods=['GET'])
def game_by_id(geekid):
    """
    Return board game geek game data
    """

    game = api.request_game(geekid)

    return make_response(game_parser.serialize(game), 200, {'Content-Type': 'application/json'})


@app.route('/api/buy', methods=['GET'])
def buy_list():
    """
    Return user's wanttobuy list
    """

    buy_list = api.request_buy_list()

    return make_response(game_parser.serialize(buy_list), 200, {'Content-Type': 'application/json'})


@app.route('/api/play', methods=['GET'])
def play_list():
    """
    Return user's wanttoplay list
    """

    play_list = api.request_play_list()

    return make_response(game_parser.serialize(play_list), 200, {'Content-Type': 'application/json'})


# health and environment endpoints
health = HealthCheck(app, "/api/health")
envdump = EnvironmentDump(app, "/api/environment")


def application_data():
    return {"maintainer": "Walker Hannan",
            "git_repo": "https://github.com/ramseyboy/tabletop-scanner"}


envdump.add_section("application", application_data)
