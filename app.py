#!/usr/bin/env python3 

from bgg_api import BggApi
from flask import Flask, render_template, make_response
app = Flask(__name__)

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
    api = BggApi('ramseyboy')
    xml = api.requestBuyList()
    return make_response(xml, 200, {'Content-Type': 'application/xml'})

@app.errorhandler(404)
def not_found(error):
    """
    404 - Not Found route
    """
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run()
