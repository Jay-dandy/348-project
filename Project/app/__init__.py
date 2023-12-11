from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

# initialize the database instance
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # attach models to the app instance (DEBUG: this is how we overcame circular imports)
    # this ensures that after initialization the models have access to the db instance
    from app.models import models
    app.models = models

    from app.routes.views import views as views_blueprint  # import blueprint
    app.register_blueprint(views_blueprint)  # register blueprint
    
    migrate = Migrate(app, db)

    return app
