from database.db import get_connection

class Salle:

    @staticmethod
    def get_all():
        conn = get_connection()
        salles = conn.execute("SELECT * FROM Salle").fetchall()
        conn.close()
        return salles

    @staticmethod
    def get_by_id(idSalle):
        conn = get_connection()
        salle = conn.execute(
            "SELECT * FROM Salle WHERE idSalle = ?", (idSalle,)
        ).fetchone()
        conn.close()
        return salle

    @staticmethod
    def get_disponibles():
        conn = get_connection()
        salles = conn.execute(
            "SELECT * FROM Salle WHERE disponible = 1"
        ).fetchall()
        conn.close()
        return salles

    @staticmethod
    def creer(nomSalle, type_, capacite, batiment):
        conn = get_connection()
        conn.execute(
            "INSERT INTO Salle (nomSalle, type, capacite, disponible, batiment) VALUES (?,?,?,1,?)",
            (nomSalle, type_, capacite, batiment)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def modifier(idSalle, nomSalle, type_, capacite, disponible, batiment):
        conn = get_connection()
        conn.execute(
            "UPDATE Salle SET nomSalle=?, type=?, capacite=?, disponible=?, batiment=? WHERE idSalle=?",
            (nomSalle, type_, capacite, disponible, batiment, idSalle)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer(idSalle):
        conn = get_connection()
        conn.execute("DELETE FROM Salle WHERE idSalle = ?", (idSalle,))
        conn.commit()
        conn.close()
