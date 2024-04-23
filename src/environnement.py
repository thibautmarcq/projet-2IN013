from logging import getLogger
from math import sqrt
from time import time

import numpy as np

from .obstacle import Obstacle
from .outil import normaliserVecteur


class Environnement:
    
    def __init__(self, width, length, scale): 
        
        """ Initialise l'environnement où l'on va se placer, où on considère que l'environnement dans lequel évolue le robot est un rectangle
            :param width: largeur de l'environnement
            :param length: longueur de l'environnement
            :param scale: l'échelle qui permet de passer de l'environnement à la matrice, c'est la correspondance de la taille d'un côté d'une case de la matrice dans le rectangle
            :returns: ne retourne rien, fait juste l'initialisation
        """
        self.logger = getLogger(self.__class__.__name__)
        
        self.width=width
        self.length=length
        self.listeRobots = []
        self.robotSelect = 0 # robot selectionné pour bouger
        self.scale = scale #echelle en int positif 
        self.last_refresh = 0 # initialise la dernière fois où l'environnement a été rafraîchi à 0 pour savoir quand on le fait pour la première fois
        self.listeObs =[] # utile pour la représentation graphique
        self.dicoObs = dict()
        self.initBorders() # lance l'initialisation de la bordure de l'env
        self.logger.info("Environnement initialisé")

    def initBorders(self):
        """
            Initialise les bordures de l'environnement en tant qu'obstacles 
            :returns: rien, crée simplement les bordures de l'environnement dans le dico des obstacles
            """
        lstPoints = [(0,0), (self.width, 0), (self.width, self.length), (0, self.length)]

        for i in range(len(lstPoints)): # Parcours la liste des points
            x1, y1 = (lstPoints[i])
            x2, y2 = lstPoints[(i+1)%len(lstPoints)] # Cas où i est le dernier indice de la liste - Point d'arrivée

            self.dicoObs[(int(y1/self.scale),int(x1/self.scale))] = 'bordure'

            while (round(x1), round(y1)) != (round(x2), round(y2)):
                dir = normaliserVecteur((x2-x1,y2-y1)) # Vecteur directeur normalisé
                x1,y1 = ((x1+dir[0]), (y1+dir[1]))

                self.dicoObs[(int(y1/self.scale),int(x1/self.scale))] = 'bordure'
                
        self.logger.info("Obstacle %s ajouté", 'bordure')

    def addRobotSelect(self, n):
        """
        Change l'indice du robot sélectionné (lui ajoute n)
        :returns: rien, ajoute n à la valeur de sélection du robot
        """
        if (len(self.listeRobots)!=0): # éviter le modulo par 0
            self.robotSelect = (self.robotSelect + n)% len(self.listeRobots)
 
    def addObstacle(self, nom, lstPoints):
        """ Ajout d'un obstacle dans le dico des obstacles
            :param nom: nom de l'obstacle
            :param lstPoints: liste des points (x,y) qui définissent la forme de l'obstacle 
            :returns: ne retourne rien, place juste un obstacle dans le dico des obstacles
        """
        self.listeObs.append(Obstacle(nom, lstPoints))
        if any(x > self.width or x < 0 or y > self.length or y < 0 for (x, y) in lstPoints):
            raise ValueError("Obstacle %s hors environnement! Verifiez les coordonnées de ses points" % nom)

        # Placement des bordures de l'obstacle dans l'environnement
        for i in range(len(lstPoints)): # Parcours la liste des points
            x1, y1 = lstPoints[i]
            x2, y2 = lstPoints[(i+1)%len(lstPoints)] # Cas où i est le dernier indice de la liste - Point d'arrivée

            self.dicoObs[(int(y1/self.scale),int(x1/self.scale))] = nom

            while (round(x1), round(y1)) != (round(x2), round(y2)):
                dir = normaliserVecteur((x2-x1,y2-y1)) # Vecteur directeur normalisé
                x1,y1 = ((x1+dir[0]), (y1+dir[1]))

                self.dicoObs[(int(y1/self.scale),int(x1/self.scale))] = nom
                
        self.logger.info("Obstacle %s ajouté", nom)

    def printMatrix(self):
        for row in self.matrice:
            print(' '.join(str(item) for item in row))
        self.logger.debug("Affichage de la matrice")

    def setRobot(self, robA):
        """ Ajoute un robot à notre environnement
            :param robA: instance du robot (adapté!!)
            :returns: rien, on ajoute juste un robot à la liste des listeRobots de l'environnement
        """
        self.listeRobots.append(robA)
        self.logger.info("Robot %s initialisé", robA.robot.nom)
 
    def refreshEnvironnement(self) :
        """ Pour rafraichir l'environnement et faire updater tous les listeRobots qui le composent.
            :returns: ne retourne rien, fait juste la mise à jour de tous les éléments
        """
        temps = time()

        if self.last_refresh == 0 : # donc si c'est la première fois qu'on fait le rafraichissement
            self.last_refresh = temps

        for robA in self.listeRobots : # on fait avancer tous les listeRobots de l'environnement
            if (not(robA.robot.estCrash) and not(self.verifCollision(robA.robot))): # Si le robot est opérationnel et qu'il n'y a pas collision 
                duree = temps - self.last_refresh
                robA.robot.refresh(duree)

            elif not robA.robot.estCrash:
                robA.robot.estCrash = True

        self.last_refresh = temps # on met à jour l'heure du dernier rafraichissement 

    def verifCollision(self, rob):
        """
        Vérifie si le prochain mouvement du robot va le faire rentrer en collision avec un obstacle (2)
        :param rob: robot pour lequel on veut tester la collision prochaine (simulé! pas adaptateur!!)
        :returns: true si robot en collision prochaine, false sinon"""

        # liste des 4 points du robot après mouvement (liste de 4couples): HG HD BD BG
        lstPoints = [(rob.x-(rob.width/2)+rob.direction[0],rob.y+(rob.length/2)+rob.direction[1]), (rob.x+(rob.width/2)+rob.direction[0],rob.y+(rob.length/2)+rob.direction[1]), (rob.x+(rob.width/2)+rob.direction[0],rob.y-(rob.length/2)+rob.direction[1]), (rob.x-(rob.width/2)+rob.direction[0],rob.y-(rob.length/2)+rob.direction[1])]

        for i in range(len(lstPoints)):
            x1, y1 = lstPoints[i] #départ
            x2, y2 = lstPoints[(i+1)%len(lstPoints)] #arrivée

            while (round(x1), round(y1)) != (round(x2), round(y2)):
                if (int(y1/self.scale), int(x1/self.scale)) in self.dicoObs:
                    self.logger.warning("Collision de %s! Obstacle %s en (%d, %d)", rob.nom, self.dicoObs[(int(y1/self.scale), int(x1/self.scale))], x1, y1)
                    return True
                
                long = sqrt((x2-x1)**2 + (y2-y1)**2) # Longueur du vect dir
                dir = ((x2-x1)/long ,(y2-y1)/long) # Vect dir normalisé
                x1,y1 = ((x1+dir[0]), (y1+dir[1])) #nv point
            
        return False # Après le parcours de tout le contour, si pas d'obstacle rencontré -> False