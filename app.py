from bgg_api import BggApi

from flask import Flask, render_template, make_response
app = Flask(__name__)

@app.route('/')
def root():
    api = BggApi()
    xml = api.requestBuyList()
    return make_response(xml, 200, {'Content-Type': 'application/xml'})


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run()
