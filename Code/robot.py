import logging
import math


class Robot :
    """Robot - Objet aux coordonnées continues, se place dans l'environnement, avance selon une direction"""

    def __init__(self, nom, x, y, width, length, rayonRoue):

        """ Initialise le robot grâce avec les paramètres passés en argument
            Initialise la direction du robot à (0, -1), donc vers le bas
            :param nom: nom du robot
            :param x: coordonnée x à laquelle on veut initialiser le robot
            :param y: coordonnée y à laquelle on veut initialiser le robot
            :param width: la largeur du robot
            :param length: la longueur du robot
            :param vitesse: la vitesse initiale du robot
            :param rayonRoue: la taille des roue
            :returns: ne retourne rien, ça initalise et initaialise seulement le robot
        """

        self.nom = nom
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.rayonRoue = rayonRoue # taille des roues en m donc 1 m = 1/100 cm

        self.vitesse = 0 # Vitesse du robot initialisée à 0
        self.direction = (0,-1) # vecteur directeur du robot
        self.nbToursRoueD = 0 # Nombre de tours/min de la roue droite initialisée à 0
        self.nbToursRoueG = 0 # Nombre de toues/min de la roue gauche initialisée à 0

    def refreshVitesse(self):

        """ Met à jour la vitesse du robot en fonction des nombres de tours par minute effectués par chacune des deux roues
            :returns: rien du tout, modifie juste la vitesse du robot
        """
        
        # if ( self.nbToursRoueG != self.nbToursRoueD) : # Si les 2 roues n'ont pas les memes tours/min, on prends la différence entre les 2 roues
        #     nbTour = max(self.nbToursRoueD, self.nbToursRoueG) - min(self.nbToursRoueD, self.nbToursRoueG)
        # else : # Si les roues ont le même nombre de tour/min alors prends le tours/min d'une des deux roues
        #     nbTour = self.nbToursRoueD
        nbTour = (int(self.nbToursRoueD) + int(self.nbToursRoueG))/2
        angulaire = 2*math.pi*(nbTour/60) # Calcul de la vitesse angulaire : w = 2*pi*(tours/60)
        self.vitesse = self.rayonRoue*angulaire # Calcul de la vitesse linéaire : v = rayonRoue * vitesse_angulaire
        logging.info("Vitesse changée à "+ str(self.vitesse))

    
    def setVitesse(self, vitesse) :

        """ Modifie la vitesse à la valeur donnée en argument
            :param vitesse: la vitesse qu'on veut donner au robot
            :returns: ne retourne rien, on fait juste la modification de la vitesse
        """
        self.vitesse = vitesse


    def rotation(self):
        """ Determine angle/sec que va faire le robot
            :returns: ne retourne rien, on modifie juste la direction du robot
        """
        x, y = self.direction
        nbTour = max(int(self.nbToursRoueD), int(self.nbToursRoueG)) - min(int(self.rnbToursRoueD), int(self.nbToursRoueG))
        # (int(self.nbToursRoueD) + int(self.nbToursRoueG))/2 # la moyenne des deux roues
        angulaire = 2*math.pi*nbTour # Calule de la vitesse angulaire
        angle = angulaire*(180/math.pi) 
        if ( angle > 40 ) :
            angle = 40
        else  :
            if ( int(self.nbToursRoueG) < int(self.nbToursRoueD) ):
                angle = -angle
                self.direction = ((x*math.cos(angle)-y*math.sin(angle)), (x*math.sin(angle)+y*math.cos(angle))) # Rotation du vecteur directeur
            else :
                self.direction = (x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle)) # Rotation du vecteur directeur

    def robotDansCadre(self) :

        """ Détermine si le robot resterait bien dans le cadre après déplacement en (xnew, ynew)
            (pour l'instant adaptée juste pour le canva de tkinter)
            :returns: True si le déplacement est possible, False sinon
        """

        x_dir = self.direction[0]
        y_dir = self.direction[1]

        # les coordonnées d'un point intermédiaire qui est sur la largeur du rectangle
        # il est pile entre les deux points de l'avant du rectangle qui représente le robot
        x_intermediaire = self.x + x_dir*self.length/2
        y_intermediaire = self.y + y_dir*self.length/2

        # deux vecteurs qui sont respectivement la rotation de 90° (sens anti-horaire) et -90° (sens horaire) du vecteur directeur du robot
        # ils vont permettre d'obtenir les coordonnées des coins avant gauche et droit du rectangle représentant le robot, en partant du point intermédiaire
        vect_droite = [-y_dir, x_dir]
        vect_gauche = [y_dir, -x_dir]

        # le calcul des coordonnées du point avant gauche du robot
        gauche_x = x_intermediaire + vect_gauche[0]*(self.width/2)
        gauche_y = y_intermediaire + vect_gauche[1]*(self.width/2)

        # le calcul des coordonnées du point avant droit du robot
        droit_x = x_intermediaire + vect_droite[0]*(self.width/2)
        droit_y = y_intermediaire + vect_droite[1]*(self.width/2)

        if gauche_x <= 0 or droit_x <= 0 : # vérifie si le robot touche dejà la bord gauche
            return False
        
        if gauche_x >= 600 or droit_x >= 600 : # vérifie si le robot touche déjà le bord droit
            return False
        
        if gauche_y <= 0 or droit_y <= 0 : # vérifie si le robot touche déjà le bord bas
            return False
        
        if gauche_y >= 400 or droit_y >= 400 : # vérifie si le robot touche déjà le bord haut
            return False
        
        return True


    def avancerDirection(self, distance):

        """ Fait avancer le robot en suivant son vecteur directeur et de sa vitesse
            :param distance: distance de laquelle on veut faire avancer le robot
            :returns: ne retourne rien, on modifie juste les coordonées du robot
        """
        
        if self.robotDansCadre() :
            self.x = self.x + self.direction[0]*distance
            self.y = self.y + self.direction[1]*distance

    def reculerDirection(self):

        """ Fait reculer le robot en suivant son vecteur directeur et de sa vitesse
            :returns: True si le déplacement a réussi, False sinon
        """
        
    
        if self.robotDansCadre() :
            self.x = self.x - self.direction[0]*self.vitesse
            self.y = self.y - self.direction[1]*self.vitesse


    
    def addTour(self) :
        """
            Augmente de 1 tour sur les 2 roues
            :returns: rien, on va modifier directement les 2 roues
        """
        self.nbToursRoueG += 1
        self.nbToursRoueD += 1

    def addTourG(self) :
        """
            Augmente de 1 tour sur la roue gauche
            :returns: rien, on va modifier directement la roue gauche
        """
        self.nbToursRoueG += 1

    def addTourD(self) :
        """
            Augmente de 1 tour sur la roue droite
            :returns: rien, on va modifier directement la roue droite
        """
        self.nbToursRoueD += 1

    def subTour(self) :
        """
            Réduit de 1 tour sur les 2 roues
            :returns: rien, on va modifier directement les 2 roues
        """
        self.nbToursRoueG -= 1
        self.nbToursRoueD -= 1

    def subTourG(self) :
        """
            Réduit de 1 tour sur la roue gauche
            :returns: rien, on va modifier directement la roue gauche
        """
        self.nbToursRoueG -= 1

    def subTourD(self) :
        """
            Réduit de 1 tour sur la roue droite
            :returns: rien, on va modifier directement la roue droite
        """
        self.nbToursRoueD -= 1
    
    def setTourG(self, nbTours):
        """ Modifie le nombre de tours de la roue gauche
            :param nbTours: le nombre de tours qu'on veut donner à la roue gauche
            :returns: ne retourne rien, on modifie la valeur de nbToursRoueG
        """
        self.nbToursRoueG=nbTours
        self.refreshVitesse()
        self.rotation()

    def setTourD(self, nbTours):
        """ Modifie le nombre de tours de la roue droite
            :param nbTours: le nombre de tours qu'on veut donner à la roue droite
            :returns: ne retourne rien, on modifie la valeur de roueD
        """
        self.nbToursRoueD=nbTours
        self.refreshVitesse()
        self.rotation()

    def getVitesseRoueD(self) :

        """ Calcule et renvoie la vitesse d'un point qui serait sur la roue droite
            :returns: la vitesse d'un point sur la roue droite
        """

        return self.nbToursRoueD*2*math.pi*self.rayonRoue
    
    def getVitesseRoueG(self) :

        """ Calcule et renvoie la vitesse d'un point qui serait sur la roue droite
            :returns: la vitesse d'un point sur la roue droite
        """

        return self.nbToursRoueD*2*math.pi*self.rayonRoue