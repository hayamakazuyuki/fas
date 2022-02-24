from flask import Flask

from .views import cs

def create_app():
    app = Flask(__name__)

    app.register_blueprint(cs)
    
    return app