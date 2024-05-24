from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite pour cet exemple, mais vous pouvez utiliser n'importe quelle base de données supportée par SQLAlchemy
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    creation_item_table(app)
    # Import des routes
    from . import routes
    app.register_blueprint(routes.bp)

    return app


def creation_item_table(app):
    from app import db
    from app.models import Item
    with app.app_context():
        db.create_all()
    