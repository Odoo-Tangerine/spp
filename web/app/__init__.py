from .config import ProductionConfig
from flask import Flask
from flask_session import Session


def create_app():
    app = Flask(__name__)
    app.config.from_object(ProductionConfig)
    Session(app)

    ctx = app.app_context()
    ctx.push()

    from .routes.index_bp import index
    from .routes.users_bp import users
    from .routes.services_bp import services

    app.register_blueprint(index)
    app.register_blueprint(users)
    app.register_blueprint(services)

    return app
