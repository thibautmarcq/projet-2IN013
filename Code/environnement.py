import random
import logging
import numpy as np
import time

from .obstacle import Obstacle
from .robot import Robot

logging.basicConfig(filename='Code/Logs/log-environnement.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s') # niveaux : DEBUG INFO WARNING ERROR CRITICAL

class Environnement:
    
    def __init__(self, width, height, scale): 
        
        """ Initialise l'environnement où l'on va se placer, où on considère que l'environnement dans lequel évolue le robot est un rectangle
            :param width: largeur de l'environnement
            :param height: longueur de l'environnement
            :param scale: l'échelle qui permet de passer de l'environnement à la matrice, c'est la correspondance de la taille d'un côté d'une case de la matrice dans le rectangle
            :returns: ne retourne rien, fait juste l'initialisation
        """
        
        self.width=width; self.height=height
        self.matrice = np.empty([int(width/scale), int(height/scale)], dtype=int) # Création d'une matrice int(width/scale)*int(height/scale) grâce à np.empty
        self.robots = []
        self.robotSelect = 0 # robot selectionné pour bouger
        self.scale = scale #echelle en int positif 
        self.last_refresh = 0 # initialise la dernière fois où l'environnement a été rafraîchi à 0 pour savoir quand on le fait pour la première fois

    def createRobot(self, nom, x, y, width, length, vitesse):

        """ Crée un robot et l'ajoute à notre environnement
            :param nom: nom du robot
            :param x: la coordonnée x où on veut placer le robot au départ
            :param y: la coordonnée y où on veut placer le robot au départ
            :param width: la largeur du robot
            :param length: la longueur du robot
            :param vitesse: la vitesse initiale du robot
            :returns: rien, on crée juste un robot qu'on ajoute a la liste des robots de l'environnement
        """

        rob = Robot(nom, x, y, width, length, vitesse)
        self.robots.append(rob)
        self.matrice[int(x/self.scale)][int(y/self.scale)] = 1 # Ajoute le robot représenté par le chiffre 1 dans la matrice

    def addRobot(self, rob) :

        """ Ajoute le robot rob à l'environnement et le place dans la matrice
            :param rob: le robot qu'on veut ajouter à l'environnement
            :returns: ne retourne rien
        """

        self.robots.append(rob)
        self.matrice[int(rob.x/self.scale)][int(rob.y/self.scale)] = 1 # Ajoute à la matrice le robot grâce a sa position en le représentant par un 1

    def addObstacle(self,nom):

        """ Ajout d'un obstacle dans la matrice, l'obstacle est représenté par '2' dans la matrice
            :param nom: nom de l'obstacle
            :returns: ne retourne rien, place juste un obstacle aléatoirement dans la matrice
        """

        obs_place = False
        while( obs_place == False ) :
            random_x = random.randrange(0,self.width) #prend des coordonnees aleatoires pour l'obstacle
            random_y = random.randrange(0,self.height)
            x = int(random_x/self.scale)
            y = int(random_y/self.scale)
            if ( self.matrice[x][y] != 1 | self.matrice[x][y] != 2) :
                Obstacle(nom, x, y)
                self.matrice[x][y] = 2 #  Ajoute l'obstacle représenté par le chiffre 2 dans la matrice
                obs_place = True

    def detect_obs(self, rob) :

        """ Détection d'un obstacle autour du robot
            :param rob: le robot autour duquel on veut vérifier s'il y a un obstacle
            :returns: true si un obstacle est détecté, false sinon
        """

        # Detecte si il y a un obstacle devant
        if ( self.matrice[int(rob.x/self.scale)+1][int(rob.y/self.scale)] == 2 ) :
            return True
        # Detecte si il y a un obstacle derriere
        if ( self.matrice[int(rob.x/self.scale)-1][int(rob.y/self.scale)] == 2 ) :
            return True
        # Detecte si il y a un obstacle à droite
        if ( self.matrice[int(rob.x/self.scale)][int(rob.y/self.scale)+1] == 2 ) :
            return True
        # Detecte si il y a un obstacle à gauche
        if ( self.matrice[int(rob.x/self.scale)][int(rob.y/self.scale)-1] == 2 ) :
            return True

        return False
    
    def refresh_env(self) :

        """ Pour rafraichir l'environnement et faire updater tous les robots qui le composent.
            :returns: ne retourne rien, fait juste la mise à jour de tous les éléments
        """
        temps = time.time()

        if self.last_refresh == 0 : # donc si c'est la première fois qu'on fait le rafraichissement
            self.last_refresh = temps

        for rob in self.robots : # on fait avancer tous les robots de l'environnement 
            duree = temps - self.last_refresh
            distance = rob.vitesse*duree
            rob.avancerDirection(distance)

        self.last_refresh = temps # on met à jour l'heure du dernier rafraichissement 


    def affiche(self):
        #methodes pour affichage avec tkinter
        pass

