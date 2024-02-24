import logging
import math
from time import *


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
            :param rayonRoue: la taille des roue
            :returns: ne retourne rien, ça initalise seulement le robot
        """

        self.nom = nom
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.rayonRoue = rayonRoue # taille des roues en m donc 1 m = 1/100 cm

        self.direction = (0,-1) # vecteur directeur du robot
        self.vitAngG = 0 # Vitesses angulaires des deux roues initialisées à 0
        self.vitAngD = 0 


    def refresh(self, duree):

        """ Méthode de update du robot, qui va modifier les coordonnées du robot et son vecteur directeur en fonction des vitesses angulaires des roues et du temps qui s'est écoulé depuis la dernière update.
            :param duree: le temps qui s'est écoulé depuis la dernière mise à jour du robot
            :returns: ne retourne rien, on met juste à jour le robot
        """

        vit = self.getVitesse() # on récupère la vitesse du centre du robot 
        dirBasex, dirBasey = self.direction

        # on récupère les coordonnées des deux roues sous la forme de point

        orto = [dirBasex*math.cos(math.pi/2)-dirBasey*math.sin(math.pi/2),
                dirBasex*math.sin(math.pi/2)+dirBasey*math.cos(math.pi/2)]
        coordRG = (self.x-(orto[0]*(self.width/2)), self.y-(orto[1]*(self.width/2)))
        coordRD = (self.x+orto[0]*(self.width/2), self.y+orto[1]*(self.width/2))

        # on calcule le vecteur vitesse de chaque roue
        vg = self.getVitesseG()
        vg = (vg*dirBasex*duree, vg*dirBasey*duree)
        vd = self.getVitesseD()
        vd = (vd*dirBasex*duree, vd*dirBasey*duree)

        # on obtient les points qui sont au bout des vecteurs vitesse des roues
        newg = (coordRG[0] + vg[0], coordRG[1] + vg[1])
        newd = (coordRD[0] + vd[0], coordRD[1] + vd[1])

        # ce qui nous permet d'obtenir la pente entre ces deux points 
        pente = ((newg[1] - newd[1])/(newg[0] - newd[0]))

        # ceci nous permet de regler le probleme de saut lorsqu'on passe dans le cadran du bas [pi, 2pi]
        if newg[0] > newd[0]:
            pente = [-1, -pente]
        else:
            pente = [1, pente]

        # on trouve le vecteur ortogonal a notre pente
        penteOrto = [pente[0]*math.cos((3*math.pi)/2)-pente[1]*math.sin((3*math.pi)/2),
                pente[0]*math.sin((3*math.pi)/2)+pente[1]*math.cos((3*math.pi)/2)]
        penteOrto = self.normaliserVecteur(penteOrto) # on le normalise

        self.direction = penteOrto # il devient notre nouvelle direction

        # et on fait notre déplacement
        self.x += self.direction[0]*vit*duree
        self.y += self.direction[1]*vit*duree


    def normaliserVecteur(self, vect) :

        """ Prend en argument un vecteur et renvoie la normalisation de ce vecteur (pour avoir une longueur de 1)
            :param vect: le vecteur que l'on souhaite normaliser
            :returns: un vecteur correspondant au vecteur donné en argument, mais normalisé à 1 de longueur
        """
        x, y = vect
        long = math.sqrt(x**2 + y**2) # la longueur du vecteur tel quel
        return (x/long, y/long) # on divise chacune des coordonnées par la longueur du vecteur, de cette manière le vecteur sera de norme 1


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

        """ Fait avancer le robot en suivant son vecteur directeur d'une distance donnée
            :param distance: la distance sur laquelle on veut faire avancer le robot
            :returns: ne retourne rien, on modifie juste les coordonées du robot
        """
        
        if self.robotDansCadre() :
            self.x = self.x + self.direction[0]*distance
            self.y = self.y + self.direction[1]*distance

    def reculerDirection(self, distance):

        """ Fait reculer le robot d'une certaine distance en suivant son vecteur directeur
            :param distance: la distance de recul que l'on veut faire parcourir au robot
            :returns: ne retourne rien, on modifie juste les coordonnées du robot 
        """
          
        if self.robotDansCadre() :
            self.x = self.x - self.direction[0]*distance
            self.y = self.y - self.direction[1]*distance

    
    def capteurDistance(self, env) :
        """
            Capteur de distance, donne la distance entre le robot et le 1er obstacle/mur
            :param env: l'environnement dans lequel on se trouve
            :returns: renvoie la distance entre le robot et un obstacle/mur
        """
        obs = (-1, -1) # True si il y a un mur/obstacle, False sinon
        rayon = (int(self.x/env.scale), int(self.y/env.scale)) # Coordonnées du rayon dans la matrice
        distance = 0 # Compteur de distance

        while( (obs[0] == -1) & (obs[1] == -1) ) :
            rayon = (rayon[0]+self.direction[0], rayon[1]+self.direction[1]) # On avance dans la direction du robot
            # Si on est sur un bord ou si on est sur un obstacle
            if ( (rayon[0] <= 0) | (rayon[0] >= env.width/env.scale) | (rayon[1] <= 0) | (rayon[1] >= env.length/env.scale) | (env.matrice[rayon[0]][rayon[1]] == 2) ) :               
                obs = (rayon[0], rayon[1]) # On sauvegarde les coordonnées de l'obstacle
                distance = math.sqrt((obs[0]-int(self.x/env.scale))**2 + (obs[1]-int(self.y/env.scale))**2)*env.scale # On calcule la distance entre le robot et l'obstacle

        return distance
    

    # Fonctions de manipulation des vitesses angulaires des roues 

    def setVitAngG(self, vit) :

        """ Setter de vitesse angulaire de la roue gauche
            :param vit: la vitesse anngulaire qu'on veut donner à la roue gauche
            :returns: ne retourne rien, on met juste à jour la vitesse angulaire de la roue gauche
        """
        self.vitAngG = vit

    def setVitAngD(self, vit) :

        """ Setter de vitesse angulaire de la roue droite
            :param vit: vitesse angulaire que l'on veut donner à la roue droite
            :returns: ne retourne rien, on change juste la vitesse angulaire de la roue droite
        """
        self.vitAngD = vit    

    def setVitAng(self, vit) :

        """ Setter qui va donner aux roues gauche et droite une certaine vitesse angulaire
            :param vit: la vitesse angulaire qu'on veut donner aux roues droite et gauche
            :returns: ne retourne rien, on met à jour les vitesses angulaires des roues
        """
        self.setVitAngD(vit)
        self.setVitAngG(vit)

    def changeVitAngG(self, quant) :
        """ Setter qui ajoute quant à la vitesse angulaire de la roue gauche
            :quant: la quantite que l'on veut rajouter à la vitesse angulaire de la roue gauche
            :returns: rien, on change juste la vitesse angulaire de la roue gauche
        """
        self.vitAngG += quant

    def changeVitAngD(self, quant) :
        """ Setter qui ajoute quant à la vitesse angulaire de la roue droite
            :quant: la quantite que l'on veut rajouter à la vitesse angulaire de la roue droite
            :returns: rien, on change juste la vitesse angulaire de la roue droite
        """
        self.vitAngD += quant

    def changeVitAng(self, quant) :
        """ Setter qui ajoute quant aux vitesses angulaires des deux roues
            :param quant: la quantite que l'on veut rajouter aux vitesses angulaires des deux roues
            :returns: ne retourne rien, on modifie les vitesses angulaires des roues
        """
        self.changeVitAngG(quant)
        self.changeVitAngD(quant)



    def getVitesseG(self) :

        """ Getter qui renvoir la vitesse d'un point qui serait sur la roue gauche
            :returns: la vitesse d'un point sur la roue gauche
        """
        return self.vitAngG*self.rayonRoue
    
    def getVitesseD(self) :

        """ Getter qui renvoie la vitesse d'un point qui serait sur la roue droite
            :returns: la vitesse d'un point sur la roue droite
        """
        return self.vitAngD*self.rayonRoue
    
    def getVitesse(self) :

        """ Getter de la vitesse du point central du robot
            :returns: la vitesse du robot en son centre
        """
        return (self.getVitesseD() + self.getVitesseG())/2
    

    

    def capteurDistance(self, env):
        """
        Capteur de distance du robot, donne la distance entre le pt milieu avant du robot (tete) et l'obstacle devant lui
        :param env: l'environnement dans lequel se trouve le robot
        :returns: retourne la distance entre la tete du robot et l'obstacle le plus proche devant lui
        """
        x1, y1 = (self.x+self.direction[0]*(self.length/2), self.y+self.direction[1]*(self.length/2))
        mat = env.matrice
        (x2, y2) = (x1, y1) # Le pt d'avancement est, au début, au pt de départ

        while (mat[int(y2/env.scale)][int(x2/env.scale)]!=2): # Condition de boucle : tant qu'on est pas sur un obstacle
            dirNorm = self.normaliserVecteur(self.direction)
            x2, y2 = (x2+dirNorm[0], y2+dirNorm[1]) # on avance en case suivant le vect dir

        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)