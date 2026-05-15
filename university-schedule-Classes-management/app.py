from flask import Flask
from database.db import init_db

app = Flask(__name__)
app.secret_key = "gestion_salles_secret"

from controllers.auth_controller import auth_bp
from controllers.salle_controller import salle_bp
from controllers.planning_controller import planning_bp
from controllers.reservation_controller import reservation_bp
from controllers.session_controller import session_bp

app.register_blueprint(auth_bp)
app.register_blueprint(salle_bp)
app.register_blueprint(planning_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(session_bp)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
