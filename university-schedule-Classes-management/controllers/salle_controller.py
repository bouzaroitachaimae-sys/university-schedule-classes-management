from flask import Blueprint, render_template, request, redirect, url_for, session
from models.salle import Salle

salle_bp = Blueprint("salle", __name__)

def admin_requis(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("user_role") != "admin":
            return redirect(url_for("auth.dashboard"))
        return f(*args, **kwargs)
    return wrapper

@salle_bp.route("/salles")
def liste_salles():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    salles = Salle.get_all()
    return render_template("salles.html", salles=salles, role=session["user_role"])

@salle_bp.route("/salles/ajouter", methods=["GET", "POST"])
@admin_requis
def ajouter_salle():
    if request.method == "POST":
        Salle.creer(
            request.form["nomSalle"],
            request.form["type"],
            int(request.form["capacite"]),
            request.form["batiment"]
        )
        return redirect(url_for("salle.liste_salles"))
    return render_template("salle_form.html", salle=None)

@salle_bp.route("/salles/modifier/<int:id>", methods=["GET", "POST"])
@admin_requis
def modifier_salle(id):
    salle = Salle.get_by_id(id)
    if request.method == "POST":
        Salle.modifier(
            id,
            request.form["nomSalle"],
            request.form["type"],
            int(request.form["capacite"]),
            int(request.form.get("disponible", 1)),
            request.form["batiment"]
        )
        return redirect(url_for("salle.liste_salles"))
    return render_template("salle_form.html", salle=salle)

@salle_bp.route("/salles/supprimer/<int:id>")
@admin_requis
def supprimer_salle(id):
    Salle.supprimer(id)
    return redirect(url_for("salle.liste_salles"))
