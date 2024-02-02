import math


class Robot :
    """Robot - Objet aux coordonnées continues, se place dans l'environnement, avance selon une direction"""

    def __init__(self, nom, x, y, width, length, vitesse):

        """ Initialise le robot grâce avec les paramètres passés en argument
            :param nom: nom du robot
            :param x: coordonnée x à laquelle on veut initialiser le robot
            :param y: coordonnée y à laquelle on veut initialiser le robot
            :param width: la largeur du robot
            :param length: la longueur du robot
            :param vitesse: la vitesse initiale du robot
        """
        
        self.nom = nom
        self.x = x
        self.y = y
        self.width = width
        self.length = length
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
        maxi = max(self.length, self.width)/2
        if (newx - maxi) < 0 or (newy - maxi) < 0 :
            return False
        if (newx + maxi) > 600 or (newy + maxi) > 400 :
            return False
        return True

    def avancerDirection(self):
        """
        Fait avancer le robot en suivant son vecteur directeur et de sa vitesse
        Retourne True si le déplacement a réussi (si il était possible dans le cadre) et False sinon
        """
        newx = self.x + self.direction[0]*self.vitesse
        newy = self.y + self.direction[1]*self.vitesse
        if self.robotDansCadre(newx, newy) :
            self.x = newx
            self.y = newy
            return True
        return False
    
