from flask import Blueprint , render_template

auth = Blueprint("auth",__name__)

@auth.route('/About')
def about():
    return "<p>About-us</p>"

@auth.route('/contact')
def contact():
    return "<p>contact-us</p>"