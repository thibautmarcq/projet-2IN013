import math


class Robot :
    """Robot - Objet aux coordonnées continues, se place dans l'environnement, avance selon une direction"""

    def __init__(self, nom, x, y, width, height, vitesse):
        self.nom = nom
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vitesse = vitesse
        self.direction = (0,-1) # vecteur directeur du robot

    def setVitesse(self, vitesse):
        """Change la vitesse du robot"""
        self.vitesse = int(vitesse)
        print("Vitesse changée à "+ str(self.vitesse))

    def rotation(self, angle):
        """Tourne d'un certain angle le vecteur directeur du robot"""
        x, y = self.direction
        self.direction = (x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle))

    def robotDansCadre(self, newx, newy) :
        """
        Détermine si le robot resterait bien dans le cadre
        après en déplacement aux newx et newy souhaités
        (pour l'instant en fonction des coordonnées de la fênetre actuelle de tkinter
        aka 600*400)
        """
        maxi = max(self.height, self.width)
        if (self.x + newx - maxi) < 0 or (self.y + newy - maxi) < 0 :
            return False
        if (self.x + newx - maxi) > 600 or (self.y + newy - maxi) > 400 :
            return False
        return True

    def avancerDirection(self):
        """
        Fait avancer le robot en suivant son vecteur directeur et de sa vitesse
        """
        newx = self.x + self.direction[0]*self.vitesse
        newy = self.y + self.direction[1]*self.vitesse
        if self.robotDansCadre(newx, newy) :
            self.x = newx
            self.y = newy
    
    def avancer(self, quantite) : 
        print("Position précédente : (" + str(self.x) + ", " + str(self.y) + "), nouvelle position : (" + str(self.x) + ", " + str(int(self.y) + int(quantite)) + ")" )
        self.y = self.y + quantite


    def reculer(self, quantite) :
        if (int(self.y) - int(quantite)) < 0 :
            print("Le déplacement n'est pas possible car hors champ")
            return
        print("Position précédente : (" + str(self.x) + ", " + str(self.y) + "), nouvelle position : (" + str(self.x) + ", " + str(int(self.y) - int(quantite)) + ")")
        self.y = int(self.y) - int(quantite)

    def droite(self, quantite) :
        print("Position précédente : (" + str(self.x) + ", " + str(self.y) + "), nouvelle position : (" + str(int(self.x) + int(quantite)) + ", " + str(self.y) + ")")
        self.x = int(self.x) + int(quantite)

    def gauche(self, quantite) :
        if (int(self.x) - int(quantite)) < 0 :
            print("Le déplacement n'est pas possible car hors champ")
            return
        print("Position précédente : (" + str(self.x) + ", " + str(self.y) + "), nouvelle position : (" + str(int(self.x) - int(quantite)) + ", " + str(self.y) + ")")
        self.x = int(self.x) - int(quantite)

    def get_position_string(self) :
        return ("(" + str(self.x) + ", " + str(self.y) + ")")  
    
    def afficher_etat(self) :
        print("Je suis le robot " + self.nom + " et je suis à la position" + self.get_position_string())

    def deplacement(self) :
        boucle = True
        while boucle :
            print("----------------------------------")
            print("Choisir une option : z pour avancer, s pour reculer, d pour aller a droite, q pour aller a gauche, ou e pour quitter")
            depl = input()
            if depl in ['z', 'q', 's', 'd'] :
                print("Taper la quantité du déplacement")
                quantite = int(input())
            if depl == 'z' :
                self.avancer(quantite)
            elif depl == 's' :
                self.reculer(quantite)
            elif depl == 'd' :
                self.droite(quantite)
            elif depl == 'q' :
                self.gauche(quantite)
            elif depl == 'e' :
                boucle = False
        print("Le déplacement du robot est terminé")
        self.afficher_etat()

