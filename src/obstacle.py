import logging
import math
from turtle import width


import time

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
        