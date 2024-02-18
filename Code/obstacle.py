import logging
import math
from turtle import width

from .environnement import Environnement

import time

#logging.basicConfig(filename='Code/Logs/log-obstacle.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s') # niveaux : DEBUG INFO WARNING ERROR CRITICAL

class Obstacle :
    """ L'obsctacle est un objet aux coordonnées discrètes, se place dans la matrice de l'environnement 
    """

    def __init__(self, nom, lstPoints, env) :

        """ Constructeur de l'obstacle, il crée et initialise un obstacle en fonction des coordonnées passées en paramètre
            :param listePoints: liste des points (x,y) qui définissent la forme de l'obstacle
            :param env: environnement dans lequel placer l'obstacle
            :returns: ne retourne rien, crée uniquement l'obstacle
        """
        
        self.nom = nom
        self.lstPoints = lstPoints
        self.env = env
        # Ne place pas l'obstacle s'il est (partiellement) en dehors de l'environnement
        if any(x > env.width or y > env.length for (x, y) in lstPoints):
            return print("Obstacle hors environnement")


        # Placement des bordures de l'obstacle dans l'environnement
        for i in range(len(lstPoints)): # Parcours la liste des points
            x1, y1 = lstPoints[i]
            x2, y2 = lstPoints[(i+1)%len(lstPoints)] # Cas où i est le dernier indice de la liste - Point d'arrivée

            self.env.matrice[int(x1/env.scale)][int(y1/env.scale)] = 2 # Place le pt de départ dans la matrice
            print('\nOBJECTIF :', x2, y2)

            while (int(x1), int(y1)) != (int(x2), int(y2)):
                long = math.sqrt((x2-x1)**2 + (y2-y1)**2) # Longueur du vect dir
                dir = ((x2-x1)/long ,(y2-y1)/long) # Vect dir normalisé
                
                # x1,y1 = (round((x1+dir[0]), 10), round((y1+dir[1]), 10)) # arrondi à 10
                x1,y1 = ((x1+dir[0]), (y1+dir[1]))

                print('int', int(x1),int(y1))
                print('float', x1,y1)
                time.sleep(0.025)

                self.env.matrice[int(x1/env.scale)][int(y1/env.scale)] = 2 # Update la matrice
                self.env.matrice[int(x1/env.scale)+1][int(y1/env.scale)+1] = 2 # Deuxieme couche pour aucun pb de hitbox

            print('Arrivé en :', x1, y1)
        time.sleep(1)


    def print_matrix(self):
        for row in self.env.matrice:
            print(' '.join(str(item) for item in row))


    def presenter_obstacle(self):

        """ Affichage (console) de l'obstacle
            :returns: ne retourne rien, fait un affichage console pour présenter rapidement l'obstacle
        """
        
        logging.debug("Je suis l'obstacle " + self.nom + " et je suis à la position(" + str(self.x) + ", " + str(self.y) + ")")
        
