from flask import Blueprint, render_template, request, redirect, url_for, session
from models.planning import Planning, Creneau
from models.salle import Salle

planning_bp = Blueprint("planning", __name__)

@planning_bp.route("/plannings")
def liste_plannings():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    plannings = Planning.get_all()
    return render_template("plannings.html", plannings=plannings, role=session["user_role"])

@planning_bp.route("/plannings/<int:id>")
def detail_planning(id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    planning  = Planning.get_by_id(id)
    creneaux  = Creneau.get_by_planning(id)
    salles    = Salle.get_disponibles()
    return render_template("planning_detail.html",
                           planning=planning,
                           creneaux=creneaux,
                           salles=salles,
                           role=session["user_role"])

@planning_bp.route("/plannings/creer", methods=["GET", "POST"])
def creer_planning():
    if session.get("user_role") not in ("chef_dept", "admin"):
        return redirect(url_for("auth.dashboard"))
    if request.method == "POST":
        Planning.creer(
            request.form["semestre"],
            request.form["filiere"],
            request.form["anneeUniv"],
            session["user_id"]
        )
        return redirect(url_for("planning.liste_plannings"))
    return render_template("planning_form.html")

@planning_bp.route("/plannings/<int:id>/creneau/ajouter", methods=["POST"])
def ajouter_creneau(id):
    if session.get("user_role") not in ("chef_dept", "admin"):
        return redirect(url_for("auth.dashboard"))
    ok, msg = Creneau.creer(
        request.form["jour"],
        request.form["heureDebut"],
        request.form["heureFin"],
        request.form["matiere"],
        id,
        int(request.form["idSalle"])
    )
    return redirect(url_for("planning.detail_planning", id=id))

@planning_bp.route("/plannings/creneau/supprimer/<int:idCreneau>/<int:idPlanning>")
def supprimer_creneau(idCreneau, idPlanning):
    if session.get("user_role") not in ("chef_dept", "admin"):
        return redirect(url_for("auth.dashboard"))
    Creneau.supprimer(idCreneau)
    return redirect(url_for("planning.detail_planning", id=idPlanning))
