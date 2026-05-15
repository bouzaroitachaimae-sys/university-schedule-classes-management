from database.db import get_connection
from datetime import datetime

class SessionExamen:
    @staticmethod
    def get_all():
        conn = get_connection()
        rows = conn.execute("""
            SELECT s.*, sa.nomSalle, u.nom AS nomChef
            FROM SessionExamen s
            JOIN Salle sa ON s.idSalle = sa.idSalle
            JOIN Utilisateur u ON s.idChef = u.idUtilisateur
            ORDER BY s.dateHeure
        """).fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_by_id(id):
        conn = get_connection()
        row = conn.execute("SELECT * FROM SessionExamen WHERE idSession=?", (id,)).fetchone()
        conn.close()
        return row

    @staticmethod
    def creer(dateHeure, duree, matiere, idSalle, idChef):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO SessionExamen (dateHeure,duree,matiere,idSalle,idChef) VALUES (?,?,?,?,?)",
                       (dateHeure, duree, matiere, idSalle, idChef))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    @staticmethod
    def supprimer(id):
        conn = get_connection()
        conn.execute("DELETE FROM Convocation WHERE idSession=?", (id,))
        conn.execute("DELETE FROM SessionExamen WHERE idSession=?", (id,))
        conn.commit()
        conn.close()


class Convocation:
    @staticmethod
    def get_by_session(idSession):
        conn = get_connection()
        rows = conn.execute("""
            SELECT c.*, u.nom AS nomEtudiant, u.email
            FROM Convocation c
            JOIN Etudiant e ON c.idEtudiant = e.idEtudiant
            JOIN Utilisateur u ON e.idEtudiant = u.idUtilisateur
            WHERE c.idSession=?
        """, (idSession,)).fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_by_etudiant(idEtudiant):
        conn = get_connection()
        rows = conn.execute("""
            SELECT c.*, s.matiere, s.dateHeure, s.duree
            FROM Convocation c
            JOIN SessionExamen s ON c.idSession = s.idSession
            WHERE c.idEtudiant=?
        """, (idEtudiant,)).fetchall()
        conn.close()
        return rows

    @staticmethod
    def publier(idSession):
        conn = get_connection()
        etudiants = conn.execute("SELECT idEtudiant FROM Etudiant").fetchall()
        session = conn.execute("SELECT * FROM SessionExamen WHERE idSession=?", (idSession,)).fetchone()
        salle = conn.execute("SELECT nomSalle FROM Salle WHERE idSalle=?", (session['idSalle'],)).fetchone()
        for i, e in enumerate(etudiants, 1):
            conn.execute("""INSERT INTO Convocation (numPlace,salleAttribuee,envoyee,idEtudiant,idSession)
                           VALUES (?,?,1,?,?)""",
                        (f"P-{i:03d}", salle['nomSalle'], e['idEtudiant'], idSession))
            conn.execute("""INSERT INTO Notification (type,dateEnvoie,envoyee,canal,objet,idUtilisateur)
                           VALUES ('convocation',datetime('now'),1,'web',?,?)""",
                        (f"Convocation : {session['matiere']}", e['idEtudiant']))
        conn.commit()
        conn.close()


class Notification:
    @staticmethod
    def get_by_user(idUtilisateur):
        conn = get_connection()
        rows = conn.execute("""
            SELECT * FROM Notification WHERE idUtilisateur=? ORDER BY dateEnvoie DESC
        """, (idUtilisateur,)).fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_all():
        conn = get_connection()
        rows = conn.execute("""
            SELECT n.*, u.nom FROM Notification n
            JOIN Utilisateur u ON n.idUtilisateur = u.idUtilisateur
            ORDER BY n.dateEnvoie DESC
        """).fetchall()
        conn.close()
        return rows

    @staticmethod
    def creer(type_, objet, idUtilisateur, canal='web', url=None):
        conn = get_connection()
        conn.execute("""INSERT INTO Notification (type,dateEnvoie,envoyee,canal,objet,url,idUtilisateur)
                       VALUES (?,datetime('now'),1,?,?,?,?)""",
                    (type_, canal, objet, url, idUtilisateur))
        conn.commit()
        conn.close()
