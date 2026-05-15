import sqlite3, os
DB_PATH = os.path.join(os.path.dirname(__file__), "gestion_salles.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS Utilisateur (
        idUtilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL, prenom TEXT NOT NULL DEFAULT '',
        email TEXT UNIQUE NOT NULL, motDePasse TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin','professeur','chef_dept','etudiant')))""")

    c.execute("""CREATE TABLE IF NOT EXISTS Administrateur (
        idAdmin INTEGER PRIMARY KEY, site TEXT,
        FOREIGN KEY (idAdmin) REFERENCES Utilisateur(idUtilisateur))""")

    c.execute("""CREATE TABLE IF NOT EXISTS Professeur (
        idProf INTEGER PRIMARY KEY, specialite TEXT,
        FOREIGN KEY (idProf) REFERENCES Utilisateur(idUtilisateur))""")

    c.execute("""CREATE TABLE IF NOT EXISTS ChefDepartement (
        idChef INTEGER PRIMARY KEY, departement TEXT,
        FOREIGN KEY (idChef) REFERENCES Utilisateur(idUtilisateur))""")

    c.execute("""CREATE TABLE IF NOT EXISTS Etudiant (
        idEtudiant INTEGER PRIMARY KEY,
        filiere TEXT, niveau TEXT, groupe TEXT,
        dateNaissance TEXT, cne TEXT, anneeInscription TEXT,
        FOREIGN KEY (idEtudiant) REFERENCES Utilisateur(idUtilisateur))""")

    c.execute("""CREATE TABLE IF NOT EXISTS Salle (
        idSalle INTEGER PRIMARY KEY AUTOINCREMENT,
        nomSalle TEXT NOT NULL, type TEXT NOT NULL,
        capacite INTEGER NOT NULL, disponible INTEGER DEFAULT 1, batiment TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS Planning (
        idPlanning INTEGER PRIMARY KEY AUTOINCREMENT,
        semaine INTEGER NOT NULL, annee INTEGER NOT NULL,
        filiere TEXT NOT NULL, idChef INTEGER,
        FOREIGN KEY (idChef) REFERENCES ChefDepartement(idChef))""")

    c.execute("""CREATE TABLE IF NOT EXISTS Creneau (
        idCreneau INTEGER PRIMARY KEY AUTOINCREMENT,
        heureDebut TEXT NOT NULL, heureFin TEXT NOT NULL,
        jour TEXT NOT NULL, matiere TEXT NOT NULL,
        idPlanning INTEGER NOT NULL, idSalle INTEGER NOT NULL,
        FOREIGN KEY (idPlanning) REFERENCES Planning(idPlanning),
        FOREIGN KEY (idSalle) REFERENCES Salle(idSalle))""")

    c.execute("""CREATE TABLE IF NOT EXISTS Reservation (
        idReservation INTEGER PRIMARY KEY AUTOINCREMENT,
        dateHeure TEXT NOT NULL, duree INTEGER NOT NULL,
        motif TEXT, statut TEXT DEFAULT 'en_attente'
        CHECK(statut IN ('en_attente','validee','refusee')),
        idUtilisateur INTEGER NOT NULL, idSalle INTEGER NOT NULL,
        FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur),
        FOREIGN KEY (idSalle) REFERENCES Salle(idSalle))""")

    c.execute("""CREATE TABLE IF NOT EXISTS SessionExamen (
        idSession INTEGER PRIMARY KEY AUTOINCREMENT,
        dateHeure TEXT NOT NULL, duree INTEGER NOT NULL,
        matiere TEXT NOT NULL, idSalle INTEGER NOT NULL, idChef INTEGER NOT NULL,
        FOREIGN KEY (idSalle) REFERENCES Salle(idSalle),
        FOREIGN KEY (idChef) REFERENCES ChefDepartement(idChef))""")

    c.execute("""CREATE TABLE IF NOT EXISTS Convocation (
        idConvocation INTEGER PRIMARY KEY AUTOINCREMENT,
        numPlace TEXT NOT NULL, salleAttribuee TEXT NOT NULL,
        envoyee INTEGER DEFAULT 0,
        idEtudiant INTEGER NOT NULL, idSession INTEGER NOT NULL,
        FOREIGN KEY (idEtudiant) REFERENCES Etudiant(idEtudiant),
        FOREIGN KEY (idSession) REFERENCES SessionExamen(idSession))""")

    c.execute("""CREATE TABLE IF NOT EXISTS Notification (
        idNotification INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL CHECK(type IN ('conflit','annulation','emploi_du_temps','convocation')),
        dateEnvoie TEXT NOT NULL, envoyee INTEGER DEFAULT 0,
        canal TEXT DEFAULT 'web', objet TEXT, url TEXT,
        idUtilisateur INTEGER NOT NULL,
        FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur))""")

    c.execute("SELECT COUNT(*) FROM Utilisateur")
    if c.fetchone()[0] == 0:
        _test(c)

    conn.commit()
    conn.close()
    print("Base de donnees initialisee avec succes.")

def _test(c):
    # Utilisateurs
    c.execute("INSERT INTO Utilisateur (nom,prenom,email,motDePasse,role) VALUES (?,?,?,?,?)",
              ("Ben Ali","Karim","admin@uic.ma","admin123","admin"))
    c.execute("INSERT INTO Administrateur (idAdmin,site) VALUES (1,'Campus Principal')")

    c.execute("INSERT INTO Utilisateur (nom,prenom,email,motDePasse,role) VALUES (?,?,?,?,?)",
              ("Martin","Pierre","martin@uic.ma","prof123","professeur"))
    c.execute("INSERT INTO Professeur (idProf,specialite) VALUES (2,'Informatique')")

    c.execute("INSERT INTO Utilisateur (nom,prenom,email,motDePasse,role) VALUES (?,?,?,?,?)",
              ("Dupont","Ahmed","dupont@uic.ma","chef123","chef_dept"))
    c.execute("INSERT INTO ChefDepartement (idChef,departement) VALUES (3,'Informatique')")

    c.execute("INSERT INTO Utilisateur (nom,prenom,email,motDePasse,role) VALUES (?,?,?,?,?)",
              ("El Amrani","Ali","ali@uic.ma","etud123","etudiant"))
    c.execute("""INSERT INTO Etudiant (idEtudiant,filiere,niveau,groupe,dateNaissance,cne,anneeInscription)
                 VALUES (4,'Genie Informatique L3','Licence 3','Groupe 2','2002-05-15','D123456789','2024-2025')""")

    # Salles
    c.execute("INSERT INTO Salle (nomSalle,type,capacite,disponible,batiment) VALUES (?,?,?,?,?)",("Salle A101","cours",40,1,"Batiment A"))
    c.execute("INSERT INTO Salle (nomSalle,type,capacite,disponible,batiment) VALUES (?,?,?,?,?)",("Salle A102","cours",40,1,"Batiment A"))
    c.execute("INSERT INTO Salle (nomSalle,type,capacite,disponible,batiment) VALUES (?,?,?,?,?)",("Labo Info B201","laboratoire",25,1,"Batiment B"))
    c.execute("INSERT INTO Salle (nomSalle,type,capacite,disponible,batiment) VALUES (?,?,?,?,?)",("Labo Reseaux B202","laboratoire",25,1,"Batiment B"))
    c.execute("INSERT INTO Salle (nomSalle,type,capacite,disponible,batiment) VALUES (?,?,?,?,?)",("Amphi C","amphitheatre",200,1,"Batiment C"))

    # Planning L3 Informatique
    c.execute("INSERT INTO Planning (semaine,annee,filiere,idChef) VALUES (?,?,?,?)",(1,2026,"Genie Informatique L3",3))

    # Emploi du temps complet — 18 creneaux sur 6 jours
    creneaux = [
        # Lundi
        ("Lundi",   "08:00","10:00","Algorithmique Avancee",        1, 1),
        ("Lundi",   "10:00","12:00","Base de Donnees",               1, 3),
        ("Lundi",   "14:00","16:00","Genie Logiciel",                1, 1),
        ("Lundi",   "16:00","18:00","Travaux Diriges — Algo",        1, 2),
        # Mardi
        ("Mardi",   "08:00","10:00","Reseaux Informatiques",         1, 4),
        ("Mardi",   "10:00","12:00","Systemes d'Exploitation",       1, 1),
        ("Mardi",   "14:00","16:00","Programmation Web",             1, 3),
        ("Mardi",   "16:00","18:00","Travaux Pratiques — Reseaux",   1, 4),
        # Mercredi
        ("Mercredi","08:00","10:00","Intelligence Artificielle",     1, 1),
        ("Mercredi","10:00","12:00","Mathematiques Discretes",       1, 2),
        ("Mercredi","14:00","16:00","Travaux Pratiques — BD",        1, 3),
        # Jeudi
        ("Jeudi",   "08:00","10:00","Architecture des Ordinateurs",  1, 1),
        ("Jeudi",   "10:00","12:00","Compilation",                   1, 2),
        ("Jeudi",   "14:00","16:00","Travaux Diriges — SE",          1, 4),
        ("Jeudi",   "16:00","18:00","Projet de Fin d'Annee",         1, 3),
        # Vendredi
        ("Vendredi","08:00","10:00","Anglais Technique",             1, 2),
        ("Vendredi","10:00","12:00","Entrepreneuriat",               1, 1),
        ("Vendredi","14:00","16:00","Travaux Pratiques — Web",       1, 3),
    ]
    for j,hd,hf,mat,pid,sid in creneaux:
        c.execute("INSERT INTO Creneau (jour,heureDebut,heureFin,matiere,idPlanning,idSalle) VALUES (?,?,?,?,?,?)",
                  (j,hd,hf,mat,pid,sid))

    # Reservation
    c.execute("INSERT INTO Reservation (dateHeure,duree,motif,statut,idUtilisateur,idSalle) VALUES (?,?,?,?,?,?)",
              ("2026-05-10 08:00",2,"Cours de rattrapage","en_attente",2,1))

    # Session examen
    c.execute("INSERT INTO SessionExamen (dateHeure,duree,matiere,idSalle,idChef) VALUES (?,?,?,?,?)",
              ("2026-06-15 09:00",3,"Algorithmique Avancee",5,3))
    c.execute("INSERT INTO Convocation (numPlace,salleAttribuee,envoyee,idEtudiant,idSession) VALUES (?,?,?,?,?)",
              ("A-12","Amphi C",1,4,1))

    # Notifications pour l'etudiant
    c.execute("INSERT INTO Notification (type,dateEnvoie,envoyee,canal,objet,idUtilisateur) VALUES (?,?,?,?,?,?)",
              ("convocation","2026-05-20",1,"web","Convocation — Examen Algorithmique Avancee le 15 Juin a 09h00 — Amphi C — Place A-12",4))
    c.execute("INSERT INTO Notification (type,dateEnvoie,envoyee,canal,objet,idUtilisateur) VALUES (?,?,?,?,?,?)",
              ("emploi_du_temps","2026-05-01",1,"web","Votre emploi du temps Semaine 1 — 2026 est disponible",4))
    c.execute("INSERT INTO Notification (type,dateEnvoie,envoyee,canal,objet,idUtilisateur) VALUES (?,?,?,?,?,?)",
              ("annulation","2026-05-18",1,"web","ANNULATION — Cours Compilation du Jeudi 23 Mai annule",4))
