# website/__init__.py

from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = 'TEST'

    # Set the upload folder in app config
    UPLOAD_FOLDER = 'uploads'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Import blueprints
    from .auth import auth
    from .models import models

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(models, url_prefix='/')

    return app
