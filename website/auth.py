from flask import Flask , render_template , request, url_for , redirect , session
from flask import Blueprint 

auth = Blueprint("auth",__name__)

@auth.route('/')
def home():
    return render_template("base.html") 
@auth.route('/mission')
def contact():
    return render_template("mission.html")


@auth.route('/Team')
def services():
    return   render_template("team.html")


@auth.route('/result')
def result():
    return render_template("result.html")

