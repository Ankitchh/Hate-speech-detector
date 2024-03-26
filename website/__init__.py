from flask import Flask , render_template, request


def create_app():
    app = Flask(__name__)
    app.secret_key = 'TEST'


    
    from .auth import auth
    from .models import models
    
    app.register_blueprint( auth,url_prefix ='/')
    app.register_blueprint( models,url_prefix ='/')

    def index():
     return render_template('base.html')

    return app