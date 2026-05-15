from flask import Blueprint, render_template, request, redirect, url_for, session
from models.session import SessionExamen, Convocation, Notification
from models.salle import Salle

session_bp = Blueprint("session", __name__)

@session_bp.route("/sessions")
def liste_sessions():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    sessions = SessionExamen.get_all()
    role = session["user_role"]
    convocations = []
    if role == "etudiant":
        convocations = Convocation.get_by_etudiant(session["user_id"])
    return render_template("sessions.html", sessions=sessions, role=role, convocations=convocations)

@session_bp.route("/sessions/creer", methods=["GET","POST"])
def creer_session():
    if session.get("user_role") not in ("chef_dept","admin"):
        return redirect(url_for("auth.dashboard"))
    if request.method == "POST":
        SessionExamen.creer(
            request.form["dateHeure"],
            int(request.form["duree"]),
            request.form["matiere"],
            int(request.form["idSalle"]),
            session["user_id"]
        )
        return redirect(url_for("session.liste_sessions"))
    salles = Salle.get_all()
    return render_template("session_form.html", salles=salles)

@session_bp.route("/sessions/<int:id>/publier")
def publier_convocations(id):
    if session.get("user_role") not in ("chef_dept","admin"):
        return redirect(url_for("auth.dashboard"))
    Convocation.publier(id)
    return redirect(url_for("session.liste_sessions"))

@session_bp.route("/sessions/<int:id>/supprimer")
def supprimer_session(id):
    if session.get("user_role") not in ("chef_dept","admin"):
        return redirect(url_for("auth.dashboard"))
    SessionExamen.supprimer(id)
    return redirect(url_for("session.liste_sessions"))

@session_bp.route("/notifications")
def notifications():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    if session["user_role"] == "admin":
        notifs = Notification.get_all()
    else:
        notifs = Notification.get_by_user(session["user_id"])
    return render_template("notifications.html", notifs=notifs, role=session["user_role"])
