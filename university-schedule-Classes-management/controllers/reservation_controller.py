from flask import Blueprint, render_template, request, redirect, url_for, session
from models.reservation import Reservation
from models.salle import Salle
from datetime import datetime

reservation_bp = Blueprint("reservation", __name__)

@reservation_bp.route("/reservations")
def liste_reservations():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    role = session["user_role"]
    if role == "admin":
        reservations = Reservation.get_all()
    else:
        reservations = Reservation.get_by_utilisateur(session["user_id"])
    return render_template("reservations.html", reservations=reservations, role=role)

@reservation_bp.route("/reservations/creer", methods=["GET","POST"])
def creer_reservation():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        Reservation.creer(
            request.form["dateHeure"],
            int(request.form["duree"]),
            request.form["motif"],
            session["user_id"],
            int(request.form["idSalle"])
        )
        return redirect(url_for("reservation.liste_reservations"))
    salles = Salle.get_disponibles()
    return render_template("reservation_form.html", salles=salles)

@reservation_bp.route("/reservations/valider/<int:id>")
def valider_reservation(id):
    if session.get("user_role") != "admin":
        return redirect(url_for("auth.dashboard"))
    Reservation.changer_statut(id, "validee")
    return redirect(url_for("reservation.liste_reservations"))

@reservation_bp.route("/reservations/refuser/<int:id>")
def refuser_reservation(id):
    if session.get("user_role") != "admin":
        return redirect(url_for("auth.dashboard"))
    Reservation.changer_statut(id, "refusee")
    return redirect(url_for("reservation.liste_reservations"))
