from flask import render_template

from . import terrain



@terrain.route("/mountain/<mountain_id>")
def mountainterrain(mountain_id):
    return render_template("mountain.html", mountain_id=mountain_id)
