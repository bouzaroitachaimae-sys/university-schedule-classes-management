from database.db import get_connection

class Reservation:

    @staticmethod
    def get_all():
        conn = get_connection()
        reservations = conn.execute("""
            SELECT r.*, u.nom AS nomUtilisateur, s.nomSalle
            FROM Reservation r
            JOIN Utilisateur u ON r.idUtilisateur = u.idUtilisateur
            JOIN Salle s       ON r.idSalle = s.idSalle
            ORDER BY r.dateHeure DESC
        """).fetchall()
        conn.close()
        return reservations

    @staticmethod
    def get_by_utilisateur(idUtilisateur):
        conn = get_connection()
        reservations = conn.execute("""
            SELECT r.*, s.nomSalle
            FROM Reservation r
            JOIN Salle s ON r.idSalle = s.idSalle
            WHERE r.idUtilisateur = ?
            ORDER BY r.dateHeure DESC
        """, (idUtilisateur,)).fetchall()
        conn.close()
        return reservations

    @staticmethod
    def creer(dateHeure, duree, motif, idUtilisateur, idSalle):
        conn = get_connection()
        conn.execute("""
            INSERT INTO Reservation (dateHeure, duree, statut, motif, idUtilisateur, idSalle)
            VALUES (?, ?, 'en_attente', ?, ?, ?)
        """, (dateHeure, duree, motif, idUtilisateur, idSalle))
        conn.commit()
        conn.close()

    @staticmethod
    def changer_statut(idReservation, statut):
        conn = get_connection()
        conn.execute(
            "UPDATE Reservation SET statut = ? WHERE idReservation = ?",
            (statut, idReservation)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer(idReservation):
        conn = get_connection()
        conn.execute("DELETE FROM Reservation WHERE idReservation = ?", (idReservation,))
        conn.commit()
        conn.close()
