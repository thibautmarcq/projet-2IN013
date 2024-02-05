import math


class Robot :
    """Robot - Objet aux coordonnées continues, se place dans l'environnement, avance selon une direction"""

    def __init__(self, nom, x, y, width, length, tailleRoue):

        """ Initialise le robot grâce avec les paramètres passés en argument
            Initialise la direction du robot à (0, -1), donc vers le bas
            :param nom: nom du robot
            :param x: coordonnée x à laquelle on veut initialiser le robot
            :param y: coordonnée y à laquelle on veut initialiser le robot
            :param width: la largeur du robot
            :param length: la longueur du robot
            :param vitesse: la vitesse initiale du robot
            :param tailleRoue: la taille des roue
            :returns: ne retourne rien, ça initalise et initaialise seulement le robot
        """

        self.nom = nom
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.tailleRoue = tailleRoue

        self.vitesse = 0 # Vitesse du robot initialisée à 0
        self.direction = (0,-1) # vecteur directeur du robot
        self.roueD = 0 # Nombre de tours/min de la roue droite initialisée à 0
        self.roueG = 0 # Nombre de toues/min de la roue gauche initialisée à 0

    def setVitesse(self):

        """ Change la vitesse du robot
            :param vitesse: la nouvelle vitesse qu'on veut donner au robot
            :returns: rien du tout, modifie juste la vitesse
        """
        # if ( self.roueG != self.roueD) : # Si les 2 roues n'ont pas les memes tours/min, on prends la différence entre les 2 roues
        #     nbTour = max(self.roueD, self.roueG) - min(self.roueD, self.roueG)
        # else : # Si les roues ont le même nombre de tour/min alors prends le tours/min d'une des deux roues
        #     nbTour = self.roueD
        nbTour = max(self.roueD, self.roueG)
        angulaire = 2*math.pi*(nbTour/60) # Calcul de la vitesse angulaire : w = 2*pi*(tours/60)
        self.vitesse = self.tailleRoue*angulaire # Calcul de la vitesse linéaire : v = tailleRoue * vitesse_angulaire

    def rotation(self):
        """ Determine angle/sec que va faire le robot
            :param
            :returns: ne retourne rien, on modifie juste la direction du robot
        """
        x, y = self.direction
        nbTour = max(self.roueD, self.roueG) - min(self.roueD, self.roueG) # La différence entre les 2 roues
        angulaire = 2*math.pi*(nbTour/60) # Calule de la vitesse angulaire
        angle = angulaire*(180/math.pi) 
        if ( angle > 40 ) :
            angle = 40
        else  :
            if ( self.roueG < self.roueD ):
                angle = -angle
                self.direction = ((x*math.cos(angle)-y*math.sin(angle)), (x*math.sin(angle)+y*math.cos(angle))) # Rotation du vecteur directeur
            else :
                self.direction = (x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle)) # Rotation du vecteur directeur

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
    
    def addTour(self) :
        """
            Augmente de 1 tour sur les 2 roues
            :returns: rien, on va modifier directement les 2 roues
        """
        self.roueG += 1
        self.roueD += 1

    def addTourG(self) :
        """
            Augmente de 1 tour sur la roue gauche
            :returns: rien, on va modifier directement la roue gauche
        """
        self.roueG += 1

    def addTourD(self) :
        """
            Augmente de 1 tour sur la roue droite
            :returns: rien, on va modifier directement la roue droite
        """
        self.roueD += 1

    def subTour(self) :
        """
            Réduit de 1 tour sur les 2 roues
            :returns: rien, on va modifier directement les 2 roues
        """
        self.roueG -= 1
        self.roueD -= 1

    def subTourG(self) :
        """
            Réduit de 1 tour sur la roue gauche
            :returns: rien, on va modifier directement la roue gauche
        """
        self.roueG -= 1

    def subTourD(self) :
        """
            Réduit de 1 tour sur la roue droite
            :returns: rien, on va modifier directement la roue droite
        """
        self.roueD -= 1