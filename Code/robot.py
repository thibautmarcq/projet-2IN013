import math


class Robot :
    def __init__(self, nom, position_x, position_y):
        self.nom = nom
        self.posx = position_x
        self.posy = position_y
        self.direction = (0,0) # vecteur directeur du robot

    def rotation(self, angle):
        """Tourne d'un certain angle le vecteur directeur du robot"""
        x, y = self.directeur
        self.directeur = (x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle))

    def avancerDirection(self):
        """Fait avancer le robot en suivant son vecteur directeur"""
        self.x += self.direction[0]
        self.y += self.direction[1]
    
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


rob_le_robot = Robot("Robert", 1, 2)
rob_le_robot.afficher_etat()
rob_le_robot.deplacement()