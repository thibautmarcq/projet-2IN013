import logging
import math
from turtle import width


import time

#logging.basicConfig(filename='Code/Logs/logs.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s') # niveaux : DEBUG INFO WARNING ERROR CRITICAL

class Obstacle :
    """ L'obsctacle est un objet aux coordonnées discrètes, se place dans la matrice de l'environnement 
    """

    def __init__(self, nom, lstPoints) :

        """ Constructeur de l'obstacle, il crée et initialise un obstacle en fonction des coordonnées passées en paramètre
            :param listePoints: liste des points (x,y) qui définissent la forme de l'obstacle
            :returns: ne retourne rien, crée uniquement l'obstacle
        """
        
        self.nom = nom
        self.lstPoints = lstPoints
        


    def presenter_obstacle(self):

        """ Affichage (console) de l'obstacle
            :returns: ne retourne rien, fait un affichage console pour présenter rapidement l'obstacle
        """
        
        logging.debug("Je suis l'obstacle " + self.nom + " et je suis à la position(" + str(self.x) + ", " + str(self.y) + ")")
        
