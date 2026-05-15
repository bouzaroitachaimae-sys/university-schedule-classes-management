from flask import Blueprint, render_template, request, redirect, url_for, session
from models.utilisateur import Utilisateur
from models.planning import Creneau
from models.session import Notification

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    return redirect(url_for("auth.dashboard") if "user_id" in session else url_for("auth.login"))

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    erreur = None
    if request.method == "POST":
        user = Utilisateur.get_by_email(request.form["email"])
        if user and user["motDePasse"] == request.form["motDePasse"]:
            session["user_id"]   = user["idUtilisateur"]
            session["user_nom"]  = user["prenom"] + " " + user["nom"]
            session["user_role"] = user["role"]
            return redirect(url_for("auth.dashboard"))
        erreur = "Email ou mot de passe incorrect."
    return render_template("login.html", erreur=erreur)

@auth_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    role = session["user_role"]
    if role == "etudiant":
        profil  = Utilisateur.get_etudiant_profil(session["user_id"])
        notifs  = Notification.get_by_user(session["user_id"])
        return render_template("dashboard_etudiant.html", profil=profil, notifs=notifs)
    return render_template("dashboard.html", nom=session["user_nom"], role=role)

@auth_bp.route("/emploi_du_temps")
def emploi_du_temps():
    if "user_id" not in session or session["user_role"] != "etudiant":
        return redirect(url_for("auth.login"))
    profil   = Utilisateur.get_etudiant_profil(session["user_id"])
    creneaux = Creneau.get_by_filiere(profil["filiere"])
    jours    = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi"]
    edt      = {j: [] for j in jours}
    for cr in creneaux:
        if cr["jour"] in edt:
            edt[cr["jour"]].append(cr)
    return render_template("emploi_du_temps.html", edt=edt, jours=jours, profil=profil)

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
