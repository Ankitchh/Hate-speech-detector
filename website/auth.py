from flask import Flask , render_template , request, url_for , redirect , session
from flask import Blueprint 

auth = Blueprint("auth",__name__)


@auth.route('/contactUs')
def contact():
    return render_template("base.html")


@auth.route('/services')
def services():
    return   render_template("base.html")


@auth.route('/blog')
def blog():
    return   render_template("blog.html")


@auth.route('/about')
def about():
    return   render_template("about.html")

@auth.route('/result')
def result():
    return render_template("result.html")

