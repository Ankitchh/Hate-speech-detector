from flask import Flask , render_template , request, url_for , redirect , session
from flask import Blueprint 

models = Blueprint("models",__name__)

@models.route('/result', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        link = request.form.get("link")
        session["link"] = link
        return redirect(url_for("link"))
    
    elif request.method == "POST":
        audio = request.form.get("audio")
        session["audio"] = audio
        return redirect(url_for("audio"))
    
    elif request.method == "POST":
        video = request.form.get("video")
        session["audio"] = audio
        return redirect(url_for("audio"))
    
    else:
        if user in session:
            return redirect(url_for("user"))
        return render_template("result.html")

@models.route('/usr')
def user():
    if link in session:
        link = session["link"]
        return f"<h1>{user}</h1>"

    else:
        return render_template(url_for("result.html"))

@models.route('/home')
def home():
    session.pop ("user", None)
    return redirect(url_for("/home"))