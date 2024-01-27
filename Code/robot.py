import math


class Robot :
    """Robot - Objet aux coordonnées continues, se place dans l'environnement, avance selon une direction"""

    def __init__(self, nom, position_x, position_y, width, height, vitesse):
        self.nom = nom
        self.posx = position_x
        self.posy = position_y
        self.width = width
        self.height = height
        self.speed = vitesse
        self.direction = (0,-1) # vecteur directeur du robot

    def rotation(self, angle):
        """Tourne d'un certain angle le vecteur directeur du robot"""
        x, y = self.direction
        self.direction = (x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle))

    def avancerDirection(self):
        """Fait avancer le robot en suivant son vecteur directeur et de sa vitesse"""
        self.posx += self.direction[0]*self.speed
        self.posy += self.direction[1]*self.speed
    
    def avancer(self, quantite) : 
        print("Position précédente : (" + str(self.posx) + ", " + str(self.posy) + "), nouvelle position : (" + str(self.posx) + ", " + str(int(self.posy) + int(quantite)) + ")" )
        self.posy = self.posy + quantite


    def reculer(self, quantite) :
        if (int(self.posy) - int(quantite)) < 0 :
            print("Le déplacement n'est pas possible car hors champ")
            return
        print("Position précédente : (" + str(self.posx) + ", " + str(self.posy) + "), nouvelle position : (" + str(self.posx) + ", " + str(int(self.posy) - int(quantite)) + ")")
        self.posy = int(self.posy) - int(quantite)

    def droite(self, quantite) :
        print("Position précédente : (" + str(self.posx) + ", " + str(self.posy) + "), nouvelle position : (" + str(int(self.posx) + int(quantite)) + ", " + str(self.posy) + ")")
        self.posx = int(self.posx) + int(quantite)

    def gauche(self, quantite) :
        if (int(self.posx) - int(quantite)) < 0 :
            print("Le déplacement n'est pas possible car hors champ")
            return
        print("Position précédente : (" + str(self.posx) + ", " + str(self.posy) + "), nouvelle position : (" + str(int(self.posx) - int(quantite)) + ", " + str(self.posy) + ")")
        self.posx = int(self.posx) - int(quantite)

    def get_position_string(self) :
        return ("(" + str(self.posx) + ", " + str(self.posy) + ")")  
    
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

