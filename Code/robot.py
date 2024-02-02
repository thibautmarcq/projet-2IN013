import math


class Robot :
    """Robot - Objet aux coordonnées continues, se place dans l'environnement, avance selon une direction"""

    def __init__(self, nom, x, y, width, length, vitesse):

        """ Initialise le robot grâce avec les paramètres passés en argument
            Initialise la direction du robot à (0, -1), donc vers le bas
            :param nom: nom du robot
            :param x: coordonnée x à laquelle on veut initialiser le robot
            :param y: coordonnée y à laquelle on veut initialiser le robot
            :param width: la largeur du robot
            :param length: la longueur du robot
            :param vitesse: la vitesse initiale du robot
            :returns: ne retourne rien, ça initalise et initaialise seulement le robot
        """

        self.nom = nom
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.vitesse = vitesse
        self.direction = (0,-1) # vecteur directeur du robot

    def setVitesse(self, vitesse):

        """ Change la vitesse du robot
            :param vitesse: la nouvelle vitesse qu'on veut donner au robot
            :returns: rien du tout, modifie juste la vitesse
        """

        self.vitesse = int(vitesse)
        print("Vitesse changée à "+ str(self.vitesse))

    def rotation(self, angle):

        """ Tourne d'un certain angle le vecteur directeur du robot
            :param angle: l'angle de rotation souhaité pour le changement de direction du robot
            :returns: ne retourne rien, on modifie juste la direction du robot
        """

        x, y = self.direction
        self.direction = (x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle))

    def robotDansCadre(self, newx, newy) :

        """ Détermine si le robot resterait bien dans le cadre après déplacement en (xnew, ynew)
            (pour l'instant juste pour le canva de tkinter)
            :param xnew: la coordonnée x où on souhaite se déplacer
            :param ynew: la coordonnée y où on souhaite se déplacer
            :returns: True si le déplacement est possible, False sinon
        """

        maxi = max(self.length, self.width)/2
        if (newx - maxi) < 0 or (newy - maxi) < 0 :
            return False
        if (newx + maxi) > 600 or (newy + maxi) > 400 :
            return False
        return True

    def avancerDirection(self):

        """ Fait avancer le robot en suivant son vecteur directeur et de sa vitesse
            :returns: True si le déplacement a réussi, False sinon
        """
        
        newx = self.x + self.direction[0]*self.vitesse
        newy = self.y + self.direction[1]*self.vitesse
        if self.robotDansCadre(newx, newy) :
            self.x = newx
            self.y = newy
            return True
        return False
    
