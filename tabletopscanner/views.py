from flask import render_template, make_response
from healthcheck import HealthCheck, EnvironmentDump

from tabletopscanner import app
from tabletopscanner.boardgamegeekapi.api import BggApi

api = BggApi('ramseyboy')


@app.route('/')
def root():
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


@app.route('/api')
def buy_list():
    """
    Return user's buy list
    """
    # wanttobuy = WantToBuy.query.filter(WantToBuy.title == 'buy').first()

    # if wanttobuy is None:
    #     xml = api.requestBuyList()
    #     rec = WantToBuy(title='buy', xml=xml.decode("utf-8"))
    #     rec.save()
    # else:
    #     xml = wanttobuy.xml

    buy = api.requestBuyList()

    return make_response(buy[1], 200, {'Content-Type': 'application/json'})


# health and environment endpoints
health = HealthCheck(app, "/api/health")
envdump = EnvironmentDump(app, "/api/environment")


def application_data():
    return {"maintainer": "Walker Hannan",
            "git_repo": "https://github.com/ramseyboy/tabletop-scanner"}


envdump.add_section("application", application_data)
