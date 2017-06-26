from tabletopscanner import db


class WantToBuy(db.Document):
    title = db.StringField()
    xml = db.StringField()
    created = db.CreatedField()
    modified = db.ModifiedField()
