import logging
import math

from .environnement import Environnement

#logging.basicConfig(filename='Code/Logs/log-obstacle.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s') # niveaux : DEBUG INFO WARNING ERROR CRITICAL

class Obstacle :
    """ L'obsctacle est un objet aux coordonnées discrètes, se place dans la matrice de l'environnement 
    """

    def __init__(self, nom, lstPoints, env) :

        """ Constructeur de l'obstacle, il crée et initialise un obstacle en fonction des coordonnées passées en paramètre
            :param listePoints: liste des points (float,float) qui définissent la forme de l'obstacle
            :param env: environnement dans lequel placer l'obstacle
            :returns: ne retourne rien, crée uniquement l'obstacle
        """
        
        self.nom = nom
        self.lstPoints = lstPoints
        self.env = env

        # Placement des bordures de l'obstacle dans l'environnement
        for i in range(len(lstPoints)): # Parcours la liste des points
            x0,y0 = lstPoints[i]
            x1,y1 = lstPoints[(i+1)%len(lstPoints)] # Cas où i est le dernier indice de la liste - Point d'arrivée

            self.env.matrice[int(x0)][int(y0)]=2 # Ajout du pt de départ de l'obstacle à la matrice

            while ((x0,y0)!=(x1,y1)):
                long = math.sqrt((x1-x0)**2 + (y1-y0)**2) # (A remplacer par normaliserVecteur si mis dans outils)
                dir = ((x1-x0)/long, (y1-y0)/long) # Calcule le vecteur directeur (normalisé) du pt 0 vers le point 1 (arrivée)

                x0,y0 = (x0+dir[0], y0+dir[1])
                self.env.matrice[int(x0)][int(y0)]=2 # Rajoute le nb de l'obstacle dans la matrice


                


    def presenter_obstacle(self):

        """ Affichage (console) de l'obstacle
            :returns: ne retourne rien, fait un affichage console pour présenter rapidement l'obstacle
        """
        
        logging.debug("Je suis l'obstacle " + self.nom + " et je suis à la position(" + str(self.x) + ", " + str(self.y) + ")")
        
