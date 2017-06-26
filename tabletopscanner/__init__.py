from flask import Flask

app = Flask(__name__)

from flask_mongoalchemy import MongoAlchemy

app.config['MONGOALCHEMY_DATABASE'] = 'library'
db = MongoAlchemy(app)

import tabletopscanner.views
