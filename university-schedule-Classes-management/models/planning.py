from database.db import get_connection

class Planning:
    @staticmethod
    def get_all():
        conn = get_connection()
        rows = conn.execute("""
            SELECT p.*, u.nom AS nomChef
            FROM Planning p
            LEFT JOIN Utilisateur u ON p.idChef = u.idUtilisateur
        """).fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_by_id(id):
        conn = get_connection()
        row = conn.execute("SELECT * FROM Planning WHERE idPlanning=?", (id,)).fetchone()
        conn.close()
        return row

    @staticmethod
    def get_by_filiere(filiere):
        conn = get_connection()
        rows = conn.execute("SELECT * FROM Planning WHERE filiere=?", (filiere,)).fetchall()
        conn.close()
        return rows

    @staticmethod
    def creer(semaine, annee, filiere, idChef):
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO Planning (semaine,annee,filiere,idChef) VALUES (?,?,?,?)",
                  (semaine, annee, filiere, idChef))
        new_id = c.lastrowid
        conn.commit(); conn.close()
        return new_id

    @staticmethod
    def supprimer(id):
        conn = get_connection()
        conn.execute("DELETE FROM Creneau WHERE idPlanning=?", (id,))
        conn.execute("DELETE FROM Planning WHERE idPlanning=?", (id,))
        conn.commit(); conn.close()


class Creneau:
    @staticmethod
    def get_by_planning(idPlanning):
        conn = get_connection()
        rows = conn.execute("""
            SELECT c.*, s.nomSalle
            FROM Creneau c
            JOIN Salle s ON c.idSalle = s.idSalle
            WHERE c.idPlanning=?
            ORDER BY CASE c.jour
                WHEN 'Lundi' THEN 1 WHEN 'Mardi' THEN 2
                WHEN 'Mercredi' THEN 3 WHEN 'Jeudi' THEN 4
                WHEN 'Vendredi' THEN 5 WHEN 'Samedi' THEN 6 ELSE 7 END,
            c.heureDebut
        """, (idPlanning,)).fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_by_filiere(filiere):
        conn = get_connection()
        rows = conn.execute("""
            SELECT c.*, s.nomSalle
            FROM Creneau c
            JOIN Salle s ON c.idSalle = s.idSalle
            JOIN Planning p ON c.idPlanning = p.idPlanning
            WHERE p.filiere = ?
            ORDER BY CASE c.jour
                WHEN 'Lundi' THEN 1 WHEN 'Mardi' THEN 2
                WHEN 'Mercredi' THEN 3 WHEN 'Jeudi' THEN 4
                WHEN 'Vendredi' THEN 5 WHEN 'Samedi' THEN 6 ELSE 7 END,
            c.heureDebut
        """, (filiere,)).fetchall()
        conn.close()
        return rows

    @staticmethod
    def creer(jour, heureDebut, heureFin, matiere, idPlanning, idSalle):
        conn = get_connection()
        conflit = conn.execute("""
            SELECT COUNT(*) FROM Creneau
            WHERE idSalle=? AND jour=?
            AND NOT (heureFin <= ? OR heureDebut >= ?)
        """, (idSalle, jour, heureDebut, heureFin)).fetchone()[0]
        if conflit > 0:
            conn.close()
            return False, "Conflit : salle deja occupee."
        conn.execute("""INSERT INTO Creneau (jour,heureDebut,heureFin,matiere,idPlanning,idSalle)
                       VALUES (?,?,?,?,?,?)""",
                    (jour, heureDebut, heureFin, matiere, idPlanning, idSalle))
        conn.commit(); conn.close()
        return True, "Creneau ajoute."

    @staticmethod
    def supprimer(id):
        conn = get_connection()
        conn.execute("DELETE FROM Creneau WHERE idCreneau=?", (id,))
        conn.commit(); conn.close()
