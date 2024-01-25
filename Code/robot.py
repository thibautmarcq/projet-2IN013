import math

class Obstacle :

    def __init__(self, nom, posx, posy) :
        self.nom = nom
        self.x = posx
        self.y = posy

    def presenter_obstacle(self):
        return(self.nom + "à la position (" + str(self.x) + ", " + str(self.y) + ")")


class Robot :
    def __init__(self, nom, position_x, position_y,):
        self.nom = nom
        self.posx = position_x
        self.posy = position_y
        self.direction = (0,-1) # vecteur directeur du robot

    def rotation(self, angle):
        """Tourne d'un certain angle le vecteur directeur du robot"""
        x, y = self.directeur
        self.directeur = (x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle))

    def avancerDirection(self):
        """Fait avancer le robot en suivant son vecteur directeur"""
        self.x += self.direction[0]
        self.y += self.direction[1]
    
    def avancer(self, quantite) :
        trouve = False
        for o in self.obstacles :
            if o.y == self.posx and (int(self.posy) + int(quantite))==o.y :
                trouve = True
                print("Je ne peux pas avancer en (" + str(self.posx) + ", " + str(self.posy + quantite) + ") car il y a l'obstacle " + o.presenter_obstacle())
                return
            
        if trouve == False :
            print("Position précédente : (" + str(self.posx) + ", " + str(self.posy) + "), nouvelle position : (" + str(self.posx) + ", " + str(int(self.posy) + int(quantite)) + ")" )
            self.posy = self.posy + quantite


    def reculer(self, quantite) :
        if (int(self.posy) - int(quantite)) < 0 :
            print("Le déplacement n'est pas possible car hors champ")
            return
        trouve = False
        for o in self.obstacles :
            if o.y == self.posx and (self.posy-quantite)==o.y :
                trouve = True
                print("Je ne peux pas avancer en (" + str(self.posx) + ", " + str(self.posy - quantite) + ") car il y a l'obstacle" + o.presenter_obstacle())
                return
            
        if trouve == False :
            print("Position précédente : (" + str(self.posx) + ", " + str(self.posy) + "), nouvelle position : (" + str(self.posx) + ", " + str(int(self.posy) - int(quantite)) + ")")
            self.posy = int(self.posy) - int(quantite)

    def droite(self, quantite) :
        trouve = False
        for o in self.obstacles :
            if o.x == self.posx and (int(self.posx) + int(quantite)) == o.x :
                trouve = True
                print("Je ne peux pas avancer en (" + str(self.posx + quantite) + ", " + str(self.posy) + ") car il y a l'obstacle" + o.presenter_obstacle())
                return
        
        if trouve == False :
            print("Position précédente : (" + str(self.posx) + ", " + str(self.posy) + "), nouvelle position : (" + str(int(self.posx) + int(quantite)) + ", " + str(self.posy) + ")")
            self.posx = int(self.posx) + int(quantite)

    def gauche(self, quantite) :
        if (int(self.posx) - int(quantite)) < 0 :
            print("Le déplacement n'est pas possible car hors champ")
            return
        trouve = False
        for o in self.obstacles :
            if o.x == self.posx and (int(self.posx) - int(quantite) )== o.x :
                trouve = True
                print("Je ne peux pas avancer en (" + str(int(self.posx) - quantite) + ", " + str(self.posy) + ") car il y a l'obstacle" + o.presenter_obstacle())
                return
        
        if trouve == False :
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


o1 = Obstacle("obstacle 1", 2, 3)
o2 = Obstacle("obstacle 2", 5, 6)
o3 = Obstacle("obstacle 3", 1, 4)

liste_obstacles = [o1, o2, o3]

rob_le_robot = Robot("Robert", 1, 2, liste_obstacles)
rob_le_robot.afficher_etat()
rob_le_robot.deplacement()