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


    def refreshVitesse(self):

        """ Met à jour la vitesse du robot en fonction des nombres de tours par minute effectués par chacune des deux roues
            :returns: rien du tout, modifie juste la vitesse du robot
        """
        
        
        VitAngD = self.getVitesseAngulaireDroite() # Vitesse angulaire de la roue droite 
        VitAngG = self.getVitesseAngulaireGauche() # Vitesse angulaire de la roue gauche en rad/min
        VitesseD = self.rayonRoue*VitAngD # Vitesse de la roue droite en m/min
        VitesseG = self.rayonRoue*VitAngG # Vitesse de la roue gauche en m/min
        self.vitesse = (VitesseD + VitesseG)/2
        logging.info("Vitesse changée à "+ str(self.vitesse))

    def refresh(self, duree, canv):

        """ Fonction de mise à jour du robot, qui va donc mettre à jour les coordonnées du robot en fonction du mouvement des ses roues et du temps écoulé depuis la dernière mise à jour
            :param duree: la durée sur laquelle on veut actualiser le mouvement, donc combien de temps le robot a évolué
            :returns: ne retourne rien, on met juste à jour le robot 
        """

        # On commence par rafrîchir la vitesse du robot
        self.refreshVitesse()

        vectDirNorm = self.normaliserVecteur(self.direction)

        # On calcule le vecteur vitesse de la roue droite et la roue gauche
        vitD = self.getVitesseRoueD()
        vectVitD = vectDirNorm
        vectVitD = (vectVitD[0]*vitD, vectVitD[1]*vitD)

        vitG = self.getVitesseRoueG()
        vectVitG = vectDirNorm
        vectVitG = (vitG*vectVitG[0], vitG*vectVitG[1])

        dirD = (vectDirNorm[1], -vectDirNorm[0]) # le vecteur directeur tourné de 90° dans le sens horaire, donc vers la droite
        dirG = (-vectDirNorm[1], vectDirNorm[0]) # le vecteur directeur tourné de 90° dans le sens anti-horaire, donc vers la gauche

        # calcul des coordonnées des roues droite et gauche

        x_droit = self.x + (dirD[0]*self.width/2) 
        y_droit = self.y + (dirD[1]*self.width/2) 

        x_gauche = self.x + (dirG[0]*self.width/2) # pour cette ligne et la suivante, on peut aussi utiliser dirD uniquement et faire des - au lieu des +
        y_gauche = self.y + (dirG[1]*self.width/2)

        #calcul des "nouvelles" coordonnées des roue gauches et droite si elles suivaient uniquement les vecteurs vitesse des roues gauche et droite
        new_x_gauche = x_gauche + vectVitG[0]
        new_y_gauche = y_gauche + vectVitG[1]

        new_x_droit = x_droit + vectVitD[0]
        new_y_droit = y_droit + vectVitD[1]

        # calcul du vecteur qui part du "nouveau point droit" au "nouveau point gauche"
        vect_relie = (new_x_gauche - new_x_droit, new_y_gauche - new_y_droit)

        newVectDir = (vect_relie[1], -vect_relie[0]) # on tourne le vecteur précédent de 90° dans le sens horaire pour obtenir un nouveau vecteur directeur du robot
        newVectDir = self.normaliserVecteur(newVectDir)
        self.direction = newVectDir # on définit la nouvelle direction du vecteur comme étant celle-ci

        newVectVit = (newVectDir[0]*self.vitesse, newVectDir[1]*self.vitesse)

        self.x = self.x + newVectVit[0]*duree
        self.y = self.y + newVectVit[1]*duree


    def refreshTest(self, duree):
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
            print("pente", pente)
            pente = [-1, -pente]
            print("newpente", pente)
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
        self.nbToursRoueG += 0.1
        self.nbToursRoueD += 0.1
        self.refreshVitesse()
        self.rotation()

    def addTourG(self) :
        """
            Augmente de 1 tour sur la roue gauche
            :returns: rien, on va modifier directement la roue gauche
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

    def tourneGauche(self):
        """ Réduit de 1 tour la roue gauche et augmente de 1 la roue droite, permet de tourner plus facilement à gauche
            :returns: rien, on modifie seulement les tours
        """
        self.subTourG()
        self.addTourD()
        self.refreshVitesse()
        self.rotation()
        sleep(0.05)
        self.subTourD()
        self.subTourG()
        self.refreshVitesse()
        self.rotation()

    def tourneDroite(self):
        """ Réduit de 1 tour la roue droite et augmente de 1 la roue gauche, permet de tourner plus facilement à droite
            :returns: rien, on modifie seulement les tours
        """
        print('prout')
        self.subTourD()
        self.addTourG()
        self.refreshVitesse()
        self.rotation()
        sleep(1)
        self.subTourG()
        self.addTourD()
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
            :returns: ne retourne rien, on modifie la valeur de roueD
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
    
    def capteurDistance(self, env, matrice) :
        """
            Capteur de distance, donne la distance entre le robot et le 1er obstacle/mur
            :returns: renvoie la distance entre le robot et un obstacle/mur
        """
        coordonnees_rob = (round(self.x/env.scale), round(self.x/env.scale)) # Coordonnées du selfot
        vecteur = self.direction # Vecteur que l'on va envoyé pour connaître la distance
        point1Vecteur = coordonnees_rob # 1er point du vecteur
        point2Vecteur = (vecteur[0]+self.x, vecteur[1]+self.y) # 2e point du vecteur = tête du vecteur
        distance = 0 # Compteur de distance
        obs = False # Variable : si il y a un obstacle/mur = True sinon False

        while( obs == False ) :
            if ( (point2Vecteur[0] >= (env.width/env.scale)-1) | (point2Vecteur[1] >= (env.width/env.scale)-1 )) : # Si le x de la tête du vecteur >= à la largeur de la matrice ou si le y de la tête du vecteur >= à la longueur de la matrice, c'est que le vecteur à atteint un mur
                obs = True
            elif ( (point2Vecteur[0] < 0 | (point2Vecteur[1] < 0 )) ) : # Si le x de la tête du vecteur < 0 ou si le y de la tête du vecteur < 0,  c'est que le vecteur à atteint un mur
                obs = True
            elif ( env.matrice[point2Vecteur[0]][point2Vecteur[1]] == 2) : # Vérifie si la tête du vecteur est à la même position qu'un osbtacle
                obs = True
            else :
                # Vérification de la direction du vecteur et d'avancer en concéquence
                if ( vecteur[1] < 0 & round(self.y/env.scale) < (env.lenght/env.scale) ) : # Vérifie si le vecteur va vers le bas et si le point y du selfot est < à la longueur de la matrice
                    point1Vecteur = (point1Vecteur[0], point2Vecteur[1]+1) # Calcul du 1e point du vecteur
                    point2Vecteur = (point2Vecteur[0], point2Vecteur[1]+1) # Calcul du 2e point du vecteur
                    vecteur = (point2Vecteur[0]-point1Vecteur[0] ,point2Vecteur[1]-point1Vecteur[1]) # Calcul du vecteur grâce aux 2 vecteurs
                    distance += 1 # Incrémentation de la distance

                if ( vecteur[1] > 0 & round(self.y/env.scale) > 0 ) : # Vérifie si le vecteur va vers le haut et si le point y du selfot est > à 0
                    point1Vecteur = (point1Vecteur[0], point2Vecteur[1]-1)
                    point2Vecteur = (point2Vecteur[0], point2Vecteur[1]-1)
                    vecteur = (point2Vecteur[0]-point1Vecteur[0] ,point2Vecteur[1]-point1Vecteur[1])
                    distance += 1

                if ( vecteur[0] > 0 & round(self.x/env.scale) < (env.width/env.scale) ) : # Vérifie si le vecteur va vers la droite et si le point x du selfot est < à la largeur de la matrice
                    point1Vecteur = (point1Vecteur[0]+1, point2Vecteur[1])
                    point2Vecteur = (point2Vecteur[0]+1, point2Vecteur[1])
                    vecteur = (point2Vecteur[0]-point1Vecteur[0] ,point2Vecteur[1]-point1Vecteur[1])
                    distance += 1

                if ( vecteur[0] < 0 & round(self.x/env.scale) > 0 ) : # Vérifie si le vecteur va vers la gauche et si le point x du selfot est > à 0
                    point1Vecteur = (point1Vecteur[0]-1, point2Vecteur[1])
                    point2Vecteur = (point2Vecteur[0]-1, point2Vecteur[1])
                    vecteur = (point2Vecteur[0]-point1Vecteur[0] ,point2Vecteur[1]-point1Vecteur[1])
                    distance += 1

                if ( vecteur[0] == vecteur[1] & round(self.x/env.scale) < (env.width/env.scale) & round(self.y/env.scale) > 0): # Vérifie si le vecteur va vers en haut à droite et si le selfot n'est pas dans le coin supérieur droite
                    point1Vecteur = (point1Vecteur[0]+1, point2Vecteur[1]-1)
                    point2Vecteur = (point2Vecteur[0]+1, point2Vecteur[1]-1)
                    vecteur = (point2Vecteur[0]-point1Vecteur[0] ,point2Vecteur[1]-point1Vecteur[1])
                    distance += 1

                if ( vecteur[0] == -vecteur[1] & round(self.x/env.scale) < (env.width/env.scale) & round(self.y/env.scale) < (env.lenght/env.scale) ): # Vérifie si le vecteur va vers en bas à droite et si le selfot n'est pas dans le coin inférieur droit
                    point1Vecteur = (point1Vecteur[0]+1, point2Vecteur[1]+1)
                    point2Vecteur = (point2Vecteur[0]+1, point2Vecteur[1]+1)
                    vecteur = (point2Vecteur[0]-point1Vecteur[0] ,point2Vecteur[1]-point1Vecteur[1])
                    distance += 1

                if ( -vecteur[0] == vecteur[1] & round(self.x/env.scale) > 0 & round(self.y/env.scale) > 0): # Vérifie si le vecteur va vers en haut à gauche et si le selfot n'est pas dans le coin supérieur gauche
                    point1Vecteur = (point1Vecteur[0]-1, point2Vecteur[1]-1)
                    point2Vecteur = (point2Vecteur[0]-1, point2Vecteur[1]-1)
                    vecteur = (point2Vecteur[0]-point1Vecteur[0] ,point2Vecteur[1]-point1Vecteur[1])
                    distance += 1

                if ( -vecteur[0] == -vecteur[1] & round(self.x/env.scale) > 0 & round(self.y/env.scale) < (env.lenght/env.scale)): # Vérifie si le vecteur va vers en bas à gauche et si le selfot n'est pas dans le coin inférieur gauche
                    point1Vecteur = (point1Vecteur[0]-1, point2Vecteur[1]+1)
                    point2Vecteur = (point2Vecteur[0]-1, point2Vecteur[1]+1)
                    vecteur = (point2Vecteur[0]-point1Vecteur[0] ,point2Vecteur[1]-point1Vecteur[1])
                    distance += 1
                
                else : # Ou sinon il y a mur
                    obs = True

        return distance*env.scale

