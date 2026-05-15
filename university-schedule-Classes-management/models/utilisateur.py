from database.db import get_connection

class Utilisateur:
    @staticmethod
    def get_by_email(email):
        conn = get_connection()
        user = conn.execute("SELECT * FROM Utilisateur WHERE email=?", (email,)).fetchone()
        conn.close()
        return user

    @staticmethod
    def get_by_id(id):
        conn = get_connection()
        user = conn.execute("SELECT * FROM Utilisateur WHERE idUtilisateur=?", (id,)).fetchone()
        conn.close()
        return user

    @staticmethod
    def get_etudiant_profil(id):
        conn = get_connection()
        row = conn.execute("""
            SELECT u.nom, u.prenom, u.email, u.role,
                   e.filiere, e.niveau, e.groupe,
                   e.dateNaissance, e.cne, e.anneeInscription
            FROM Utilisateur u
            JOIN Etudiant e ON e.idEtudiant = u.idUtilisateur
            WHERE u.idUtilisateur = ?
        """, (id,)).fetchone()
        conn.close()
        return row
