#!/usr/bin/env python3

from datetime import datetime

from bgg_api import BggApi
api = BggApi('ramseyboy')

from flask import Flask, render_template, make_response
from flask_mongoalchemy import MongoAlchemy

app = Flask(__name__)

app.config['MONGOALCHEMY_DATABASE'] = 'library'
db = MongoAlchemy(app)

class WantToBuy(db.Document):
    title = db.StringField()
    xml = db.StringField()
    created = db.CreatedField()
    modified = db.ModifiedField()

@app.route('/')
def root():
    """
    Api root listing
    """
    return "/"


@app.route('/buy')
def buy_list():
    """
    Return user's buy list
    """
    wanttobuy = WantToBuy.query.filter(WantToBuy.title == 'buy').first()

    if wanttobuy is None:
        xml = api.requestBuyList()
        rec = WantToBuy(title='buy', xml=xml.decode("utf-8"))
        rec.save()
    else:
        xml = wanttobuy.xml

    return make_response(xml, 200, {'Content-Type': 'application/xml'})


@app.errorhandler(404)
def not_found(error):
    """
    404 - Not Found route
    """
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run()
