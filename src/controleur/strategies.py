from logging import getLogger
from time import time

from src import (VIT_ANG_AVAN, VIT_ANG_TOUR, contientBalise,
                DEBUT_POLI, DEBUT_ROY, DEBUT_AMBRE, DEBUT_HELI, FIN_PERSONNAGES, FIN_GENERIQUE)


# ------------------------- Stratégies de base -------------------------------

class StrategieAvancer():

    def __init__(self, robAdapt, distance) :
        """ Stratégie qui fait avancer le robot d'une distance donnée
            :param distance: la distance que doit parcourir le robot
            :param robAdapt: l'adaptateur du robot qu'on veut avancer
            :returns: ne retourne rien, on initialise la stratégie
        """
        self.logger = getLogger(self.__class__.__name__)
        self.distance = distance
        self.robA = robAdapt
        self.parcouru = 0
        self.robA.initialise()


    def start(self) :
        """ Lancement de la stratégie avancer """
        self.logger.debug("Stratégie avancer démarée")

        self.robA.robot.estSousControle = True
        self.parcouru = 0
        self.robA.setVitAngA(VIT_ANG_AVAN) # Puis on set les vitesses angulaires des deux roues à 5
        self.robA.initialise()


    def step(self) :
        """ On fait avancer le robot d'un petit pas
            :returns: rien, on met juste à jour la distance parcourue par le robot
        """
        if not self.stop() and not self.robA.robot.estCrash:
            self.parcouru = self.robA.getDistanceParcourue()
            self.logger.debug("distance de segment parcourue : %d", self.parcouru )


    def stop(self):
        """ Détermine si on a bien parcouru la distance souhaitée
            :returns: True si on a bien complété la stratégie, False sinon
        """
        if self.parcouru >= self.distance :
            self.robA.robot.estSousControle = False
            return True
        return False



class StrategieTourner():   

    def __init__(self, robAdapt, angle):
        """ Strategie qui fait tourner le robot représenté par son adaptateur d'un angle donné
            :param robAdapt: l'adaptateur du robot que l'on veut faire tourner
            :param angle: la rotation que l'on veut ordonner au robot d'effectuer
        """
        self.logger = getLogger(self.__class__.__name__)
        self.robA = robAdapt
        self.angle = angle
        self.angle_parcouru = 0
        self.robA.initialise()


    def start(self) :
        """ Lancement de la stratégie tourner """
        self.logger.debug("Stratégie tourner lancée")

        self.robA.robot.estSousControle = True
        self.angle_parcouru = 0
        self.robA.initialise()

        # On considère ici une rotation d'un angle alpha dans le sens horaire, c.à.d si positif on tourne vers la droite, sinon vers la gauche
        # On change les vitesses des deux roues, en leur donnant des vitesses opposées afin de tourner sur place
        self.robA.setVitAngGA(VIT_ANG_TOUR  if self.angle > 0 else -VIT_ANG_TOUR)
        self.robA.setVitAngDA(-VIT_ANG_TOUR  if self.angle > 0 else VIT_ANG_TOUR)


    def step(self):
        """ Le step de la stratégie tourner, qui met a jour l'angle qui a été parcouru jusqu'à maintenant
            :returns: ne retourne rien, on met juste a jour le paramètre distance parcourue
        """
        if not self.stop() and not self.robA.robot.estCrash:
            self.angle_parcouru = self.robA.getAngleParcouru()
            self.logger.debug("angle de rotation parcouru : %d",self.angle_parcouru)


    def stop(self):
        """ Détermine si on a fini de faire la rotation de l'angle self.angle
            :returns: True si la rotation a bien été effectuée, False sinon
        """
        if abs(self.angle_parcouru) > abs(self.angle) :
            self.robA.robot.estSousControle = False
            return True
        return False
    


class StrategieArretMur():

    def __init__(self, robAdapt, distarret):
        """ Strategie qui fait arreter le robot a une distance donnée
            :param robAdapt: le robot que l'on veut faire arreter avant un mur/obtacle
            :param distarret: la distance que l'on veut entre le robot et le mur/obstacle
        """
        self.logger = getLogger(self.__class__.__name__)
        self.robA = robAdapt
        self.distarret = distarret
        self.distrob = self.robA.getDistanceA() # la distance entre le robot et le mur/obtacle le plus proche devant lui, obtenue avec le capteur de distance
        self.robA.initialise()


    def start(self):
        """ Réinitialisation de la vitesse du robot et de la distance entre le robot et le mur/obstacle """
        self.robA.robot.estSousControle = True
        self.robA.setVitAngA(4)
        self.distrob = self.robA.getDistanceA()
        self.robA.initialise()
        self.logger.debug("Stratégie ArretMur lancée")


    def step(self):
        """ Le step de la stratégie arret mur : qui met à jour la distance entre le robot et le mur/obstacle devant lui
            :returns: rien, on met juste à jour la distance entre le robot et le mur/obstacle
        """
        if not self.stop():
            self.distrob = self.robA.getDistanceA()
        else:
            self.robA.setVitAngA(0)


    def stop(self):
        """ Détermine si la distance entre le robot et le mur/obstacle est plus petite ou égale a la distarret souhaitée
            :return: True si oui, non sinon
        """
        if self.distrob <= self.distarret :
            self.robA.robot.estSousControle = False
            return True
        return False
    


class StrategieSuivreBalise():

    def __init__(self, robAdapt):
        """ Strategie permettant au robot de suivre une balise  
            :param robAdapt: le robot qui va suivre la balise
        """
        self.logger = getLogger(self.__class__.__name__)
        
        self.robA = robAdapt
        self.robA.initialise()
        self.balise ,self.decale = contientBalise(self.robA.get_imageA()) 
        # balise : Booléen: True si le robot voit la balise
        # decalage : le decalage en x entre le milieu de son champ de vision et la balise


    def start(self):
        """ Réinitialisation du robot, du decalage et de balise """
        self.robA.robot.estSousControle = True
        self.robA.initialise()
        self.balise, self.decale = contientBalise(self.robA.get_imageA())
        self.logger.debug("Stratégie Suivre Balise lancé")


    def step(self):
        """ Le step de la stratégie suivre balise : qui met à jour le decalage entre le milieu de son champ de vision et la balise
            et qui set la vitesse des roues en fonction du decalage
            :returns: rien
        """
        if not self.stop():
            self.robA.setVitAngA(1)
            if self.decale > 0:
                self.robA.setVitAngGA(2)
                self.robA.setVitAngDA(1)
            if self.decale < 0:
                self.robA.setVitAngGA(1)
                self.robA.setVitAngDA(2)
            self.balise, self.decale = contientBalise(self.robA.get_imageA())
        else:
            self.robA.setVitAngA(0)


    def stop(self):
        """ Retourne si la balise est dans le champ de vision du robot
            :return: True si la balise n'y est pas, False sinon
        """
        if not self.balise:
            self.robA.robot.estSousControle = False
            return True
        return False
    
class StrategieRobocar() :

    def __init__(self, robAdapt) :
        """ Stratégie supplémentaire spéciale Robocar Poli, permet de lancer le générique en faisant des mouvement et en activant les couleurs en fonction des personnages
        """

        self.logger = getLogger(self.__class__.__name__)
        self.robA = robAdapt
        self.temps = time()

    def start(self) :
        """ Initialisation de la stratégie Robocar, on enregistre l'heure du débue de lancement, on met le robot en mouvement et on lance le son
            :returns: rien, on entame juste la stratégie
        """
        self.robA.robot.estSousControle = True
        self.temps_debut = time()
        self.robA.tourne(-50, 50)
        self.robA.playSound("autre/secret.wav")
        
    
    def step(self) :
        """ Step de la stratégie Robocar, on vérifie si le temps actuel correspond à une étape de changement de lumière du robot
        """
        if not self.stop :
            tmp = time()
            difference = time()-self.temps_debut

            if difference>=DEBUT_POLI and difference<DEBUT_ROY :
                self.robA.changeCouleur("blue")
            
            elif difference>=DEBUT_ROY and difference<DEBUT_AMBRE :
                self.robA.changeCouleur("red")

            elif difference>=DEBUT_AMBRE and difference<DEBUT_HELI :
                self.robA.changeCouleur("pink")
            
            elif difference>=DEBUT_HELI and difference<FIN_PERSONNAGES :
                self.robA.changeCouleur("green")

            elif difference>FIN_PERSONNAGES :
                self.robA.changeCouleur("base")

        else :
            self.robA.setVitAngA(0)
    

    def stop(self) :
        """ Stop de la stratégie Robocar, détermine si le générique a fini de jouer
            :returns: True si la stratégie est terminée, False sinon
        """
        if time()-self.temps_debut>FIN_GENERIQUE :
            self.robA.robot.estSousControle = False
            return True
        return False


# ------------------------- Types de stratégie multiples -------------------------------

class StrategieSeq():

    def __init__(self, listeStrat, robAdapt) :
        """ Stratégie séquentielle
            :param listeStrat: liste de stratégies qui vont être executées à la suite
            :param rob: le robot que l'on veut faire tourner
            :returns: rien, on initialise la stratégie séquentielle
        """
        self.listeStrat = listeStrat
        self.robA = robAdapt
        self.indice = -1
        self.robA.initialise()


    def start(self):
        """ Lancement de la stratégie séquentielle """
        self.robA.robot.estSousControle = True
        self.indice = -1
        self.robA.initialise()


    def step(self) : 
        """ Le step de la stratégie séquentielle, où on fait le step de la stratégie en cours ou on passe a la stratégie suivante selon le cas, et on met à jour le robot
            :returns: rien, il s'agit juste de lancement de sous-stratégies et de mise à jour de robots
        """
        if not self.stop():
            if (self.indice < 0 or self.listeStrat[self.indice].stop()) and self.indice != len(self.listeStrat)-1: # Si on n'a pas encore commencé à lancer les stratégies unitaire ou si la stratégie en cours est terminée, on avance à la stratégie suivante
                self.indice += 1
                self.listeStrat[self.indice].start()
            self.listeStrat[self.indice].step() # On fait le step de la stratégie en cours
        else:
            self.listeStrat[self.indice].robA.setVitAngA(0)


    def stop(self) :
        """ Détermine si la stratégie séquentielle est terminée, donc si toutes ses sous-stratégies son terminées
            :returns: True si toutes les stratégies ont bien été accomplies, False sinon
        """
        if self.indice == len(self.listeStrat)-1 and self.listeStrat[self.indice].stop() :
            self.robA.robot.estSousControle = False
            return True
        return False



class StrategieCond():

    def __init__(self, robAdapt, strat, cond):
        """ Stratégie conditionnelle 
            :param robAdapt: le robot que l'on veut faire executer la strat
            :param strat: la stratégie à executer tant que la cond est remplie
            :param cond: fonction conditionnelle / booleenne (ex: <module>.verifDistanceSup(rob, 5) renverrai True si le captDist renvoie > 5)
        """
        self.logger = getLogger(self.__class__.__name__)
        self.robA = robAdapt
        self.strat = strat
        self.cond = cond
        self.robA.initialise()


    def start(self):
        """ Lancement de la stratégie conditionnelle """
        self.logger.debug("Stratégie conditionnelle lancée")
        self.robA.initialise()
        self.robA.robot.estSousControle = True
        self.strat.start()


    def step(self):
        """ Exécute la strat demandée si la condition est remplie 
            :returns: rien, fait le step de la strat
        """
        if not self.stop() :
            self.strat.step() 


    def stop(self):
        """ Vérifie si la condition est toujours valide
            :returns: False si condition remplie (pas de stop), True si non remplie (stop)
        """
        if not self.cond() : 
            self.robA.robot.estSousControle = False
            return True
        return False



class StrategieBoucle():

    def __init__(self, robAdapt, strat, nbTours):
        """ Stratégie de boucle
            :param robAdapt: le robot que l'on veut faire executer la strat
            :param strat: la stratégie à executer
            :param nbTours: nombre de tours que la boucle doit faire
        """
        self.logger = getLogger(self.__class__.__name__)
        self.robA = robAdapt
        self.strat = strat
        self.nbTours = nbTours
        self.restants = self.nbTours
        self.robA.initialise()


    def start(self):
        """ Lancement de la stratégie de boucle """
        self.logger.debug("Stratégie de boucle lancée")
        self.restants = self.nbTours
        self.robA.robot.estSousControle = True
        self.robA.initialise()
        self.strat.start()


    def step(self):
        """ Exécute la strat demandée si on est encore dans un tour
            :returns: rien, fait le step de la strat
        """
        if not self.stop() :
            self.strat.step() 
            if self.strat.stop():
                self.restants-=1 
                if not self.stop():
                    self.strat.start()


    def stop(self):
        """ Vérifie si le nombre de tours a été fait
            :returns: False si il reste encore des tours à faire, True si les tours ont été faits
        """
        if self.restants<1 :
            self.robA.robot.estSousControle = False
            return True
        return False


# ------------------------- Setter de stratégie -------------------------------

def setStrategieCarre(robAdapt, longueur_cote):
    """ Crée une stratégie pour faire un carré"""
    avance = StrategieAvancer(robAdapt, longueur_cote)
    tourne = StrategieTourner(robAdapt, 90)
    carre  = StrategieSeq([avance, tourne, avance, tourne, avance, tourne, avance, tourne],robAdapt)
    return carre


def setStrategieArretMur(robAdapt, distarret) :
    """ Crée une stratégie pour faire arreter le robot à une distance donnée d'un mur """
    arret = StrategieArretMur(robAdapt, distarret)
    return arret


# -------------------------- Méthodes conditionnelles -------------------------

def verifDistanceSup(robAdapt, dist):
    """ Verifie que le robot est à une distance supérieure à dist d'un obstacle
    :param robAdapt: l'adaptateur pour lequel on va utiliser le capteur de distance
    :param dist: la distance utilisée pour la condition
    """
    return (robAdapt.getDistanceA()>dist)
