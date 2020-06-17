from flask import Flask
from flask_bootstrap import Bootstrap

from .config import Config

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    # Trasladamos nuestra configuracion de app a el archivo config.py
    # entonces ocupamos esto que traera el objeto Config:
    app.config.from_object(Config)
    
    return app