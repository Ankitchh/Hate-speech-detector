from flask import Flask , render_template, request


def create_app():
    app = Flask(__name__)
    app.secret_key = 'TEST'


    from .views import views
    from .auth import auth
    from .models import models

    app.register_blueprint( views,url_prefix = '/')
    app.register_blueprint( auth,url_prefix ='/')
    app.register_blueprint( models,url_prefix ='/')

    def index():
     return render_template('index.html')

    return app