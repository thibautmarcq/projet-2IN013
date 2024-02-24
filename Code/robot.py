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
        self.nbToursRoueD = 0 # Nombre de tours de la roue droite initialisée à 0
        self.nbToursRoueG = 0 # Nombre de toues de la roue gauche initialisée à 0
        self.vitAngG = 0 # Vitesses angulaires des deux roues initialisées à 0
        self.vitAngD = 0 


    def refreshVitesse(self):

        """ Met à jour la vitesse du robot en fonction des vitesses de chacune des deux roues
            :returns: rien du tout, modifie juste la vitesse du robot
        """
        
        self.vitesse = (self.getVitesseD() + self.getVitesseG())/2
        logging.info("Vitesse changée à "+ str(self.vitesse))

    def refresh(self, duree):
        self.refreshVitesse() # on rafraichit la vitesse
        dirBasex, dirBasey = self.direction

        # on récupère les coordonnées des deux roues sous la forme de point

        orto = [dirBasex*math.cos(math.pi/2)-dirBasey*math.sin(math.pi/2),
                dirBasex*math.sin(math.pi/2)+dirBasey*math.cos(math.pi/2)]
        coordRG = (self.x-(orto[0]*(self.width/2)), self.y-(orto[1]*(self.width/2)))
        coordRD = (self.x+orto[0]*(self.width/2), self.y+orto[1]*(self.width/2))

        # on calcule le vecteur vitesse de chaque roue
        vg = self.getVitesseRoueG()
        vg = (vg*dirBasex*duree, vg*dirBasey*duree)
        vd = self.getVitesseRoueD()
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
        self.x += self.direction[0]*self.vitesse*duree
        self.y += self.direction[1]*self.vitesse*duree
        
    
    def setVitesse(self, vitesse) :

        """ Modifie la vitesse à la valeur donnée en argument
            :param vitesse: la vitesse qu'on veut donner au robot
            :returns: ne retourne rien, on fait juste la modification de la vitesse
        """
        self.vitesse = vitesse

    def normaliserVecteur(self, vect) :

        """ Prend en argument un vecteur et renvoie la normalisation de ce vecteur (pour avoir une longueur de 1)
            :param vect: le vecteur que l'on souhaite normaliser
            :returns: un vecteur correspondant au vecteur donné en argument, mais normalisé à 1 de longueur
        """
        x, y = vect
        long = math.sqrt(x**2 + y**2) # la longueur du vecteur tel quel
        return (x/long, y/long) # on divise chacune des coordonnées par la longueur du vecteur, de cette manière le vecteur sera de norme 1


    def rotation(self):
        """ Determine angle/sec que va faire le robot
            :returns: ne retourne rien, on modifie juste la direction du robot
        """
        x, y = self.direction
        nbTour = max(int(self.nbToursRoueD), int(self.nbToursRoueG)) - min(int(self.nbToursRoueD), int(self.nbToursRoueG))
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

        """ Fait avancer le robot en suivant son vecteur directeur
            :param distance: distance de laquelle on veut faire avancer le robot
            :returns: ne retourne rien, on modifie juste les coordonées du robot
        """
        
        if self.robotDansCadre() :
            self.x = self.x + self.direction[0]*distance
            self.y = self.y + self.direction[1]*distance

    def reculerDirection(self):

        """ Fait reculer le robot en suivant son vecteur directeur
            :returns: True si le déplacement a réussi, False sinon
        """
        
    
        if self.robotDansCadre() :
            self.x = self.x - self.direction[0]*self.vitesse
            self.y = self.y - self.direction[1]*self.vitesse


    
    def addTour(self) :
        """
            Augmente de 1 tour sur les 2 roues
            :returns: rien, on va modifier directement les 2 roues et faire les rafraichissements nécessaires
        """
        self.nbToursRoueG += 0.1
        self.nbToursRoueD += 0.1
        self.refreshVitesse()
        self.rotation()

    def addTourG(self) :
        """
            Augmente de 1 tour sur la roue gauche
            :returns: rien, on va modifier directement la roue gauche et faire les rafraichissements nécessaires
        """
        self.nbToursRoueG += 0.1
        self.refreshVitesse()
        self.rotation()

    def addTourD(self) :
        """
            Augmente de 1 tour sur la roue droite
            :returns: rien, on va modifier directement la roue droite
        """
        self.nbToursRoueD += 0.1
        self.refreshVitesse()
        self.rotation()

    def subTour(self) :
        """
            Réduit de 1 tour sur les 2 roues
            :returns: rien, on va modifier directement les 2 roues
        """
        self.nbToursRoueG -= 0.1
        self.nbToursRoueD -= 0.1
        self.refreshVitesse()
        self.rotation()

    def subTourG(self) :
        """
            Réduit de 1 tour sur la roue gauche
            :returns: rien, on va modifier directement la roue gauche
        """
        self.nbToursRoueG -= 0.1
        self.refreshVitesse()
        self.rotation()

    def subTourD(self) :
        """
            Réduit de 1 tour sur la roue droite
            :returns: rien, on va modifier directement la roue droite
        """
        self.nbToursRoueD -= 0.1
        self.refreshVitesse()
        self.rotation()

    
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
            :returns: ne retourne rien, on modifie la valeur de nbToursRoueD
        """
        self.nbToursRoueD=nbTours
        self.refreshVitesse()
        self.rotation()

    
    def getVitesseAngulaireGauche(self) :

        """ Donne la vitesse angulaire de la roue gauche 
            :returns: la vitesse angulaire de la roue gauche
        """

        return 2*math.pi*self.nbToursRoueG
    
    def getVitesseAngulaireDroite(self) :

        """ Donne la vitesse angulaire de la roue droite 
            :returns: la vitesse angulaire de la roue droite
        """
        
        return 2*math.pi*self.nbToursRoueD
    

    def getVitesseRoueD(self) :

        """ Calcule et renvoie la vitesse d'un point qui serait sur la roue droite
            :returns: la vitesse d'un point sur la roue droite
        """

        return self.getVitesseAngulaireDroite()*self.rayonRoue
    
    def getVitesseRoueG(self) :

        """ Calcule et renvoie la vitesse d'un point qui serait sur la roue droite
            :returns: la vitesse d'un point sur la roue droite
        """

        return self.getVitesseAngulaireGauche()*self.rayonRoue
    
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

    
    def addVitAngG(self) :

        """ Setter qui va augmenter de 1 la vitesse angulaire de la roue gauche
            :returns: ne retourne rien, on fait juste une mise à jour
        """
        self.vitAngG += 1

    def addVitAngD(self) :

        """ Setter qui va augmenter la vitesse augulaire de la roue droite de 1
            :returns: ne retourne rien, on fait juste une mise à jour
        """
        self.vitAngD += 1

    def addVitAng(self) :

        """ Setter qui augmente les vitesses angulaires des deux roues de 1
            :returns: ne retourne rien, on fait une mise à jour des vitesses augulaires des deux roues.
        """
        self.vitAngD += 1
        self.vitAngG += 1


    def subVitAngG(self) :

        """ Setter qui va réduire de 1 la vitesse angulaire de la roue gauche
            :returns: ne retourne rien, on fait juste une mise à jour
        """
        self.vitAngG -= 1

    def subVitAngD(self) :

        """ Setter qui va diminuer la vitesse augulaire de la roue droite de 1
            :returns: ne retourne rien, on fait juste une mise à jour
        """
        self.vitAngD -= 1

    def subVitAng(self) :

        """ Setter qui diminue les vitesses angulaires des deux roues de 1
            :returns: ne retourne rien, on fait une mise à jour des vitesses augulaires des deux roues.
        """
        self.vitAngD -= 1
        self.vitAngG -= 1


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
    

    
