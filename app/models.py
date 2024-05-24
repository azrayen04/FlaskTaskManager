
from . import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255))
    project = db.Column(db.String(100))
    status = db.Column(db.String(50))
    date_livraison = db.Column(db.String(50))
    importance = db.Column(db.String(50))
    risque = db.Column(db.String(50))
    commentaire = db.Column(db.Text)



class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    ip = db.Column(db.String(50))
    user = db.Column(db.String(50))
    password = db.Column(db.String(255))
    key = db.Column(db.String(255))
    