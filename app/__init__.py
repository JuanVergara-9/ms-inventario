from flask import Flask
from app.extension import db, cache, migrate
from app.routes import inventario_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configurar el modo de depuración
    app.debug = True

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)

    app.register_blueprint(inventario_bp, url_prefix='/inventario')

    return app