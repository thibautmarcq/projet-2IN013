import logging

from src.constantes import *
from src.Robot import *


class StrategieAvancer:
    
    def __init__(self, rob, distance) :
        """ Statégie qui fait avancer le robot d'une distance donnée
            :param distance: la distance que doit parcourir le robot
            :param rob: l'adaptateur du robot qu'on veut avancer
            :returns: ne retourne rien, on initialise la stratégie
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.distance = distance
        self.rob = rob
        self.parcouru = 0
        self.getRob().distance_parcourue() # Met à jour les infos du robot avec le pt de départ

    def start(self) :
        """ Lancement de la stratégie avancer """
        self.logger.debug("Stratégie avancer démarée")
        self.rob.estSousControle = True
        self.parcouru = 0
        self.rob.setVitAngA(VIT_ANG_AVAN) # Puis on set les vitesses angulaires des deux roues à 5

    def step(self) :
        """ On fait avancer le robot d'un petit pas
            :returns: rien, on met juste à jour la distance parcourue par le robot
        """
        if not self.stop() and not self.rob.estCrash:
            self.parcouru += self.rob.distance_parcourue()
            self.logger.debug("distance de segment parcourue : %d", self.parcouru )

    def stop(self):
        """ Détermine si on a bien parcouru la distance souhaitée
            :returns: True si on a bien complété la stratégie, False sinon
        """
        return self.parcouru >= self.distance

    def getRob(self):
        """
            Getter du robot qui est sous contrôle de la stratégie séquentielle
            :returns: le robot qui est sous le contrôle du contrôleur
        """
        return self.rob



class StrategieTourner:
    
    def __init__(self, rob, angle):

        """ Stategie qui fait tourner le robot représenté par son adaptateur d'un angle donné
            :param rob: l'adaptateur du robot que l'on veut faire tourner
            :param angle: la rotation que l'on veut ordonner au robot d'effectuer
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        self.rob = rob
        self.angle = angle
        self.angle_parcouru = 0
        self.getRob().angle_parcouru()

    def start(self) :

        self.logger.debug("Stratégie tourner lancée")

        self.rob.estSousControle = True
        self.angle_parcouru = 0

        # On considère ici une rotation d'un angle alpha dans le sens horaire, c.à.d si positif on tourne vers la droite, sinon vers la gauche
        # On change les vitesses des deux roues, en leur donnant des vitesses opposées afin de tourner sur place

        self.rob.setVitAngGA(VIT_ANG_TOUR  if self.angle > 0 else -VIT_ANG_TOUR)
        self.rob.setVitAngDA(-VIT_ANG_TOUR  if self.angle > 0 else VIT_ANG_TOUR)

    def step(self):

        """ Le step de la stratégie tourner, qui met a jour l'angle qui a été parcouru jusqu'à maintenant sinon
            :returns: ne retourne rien, on met juste a jour le paramètre distance parcourue
        """
        if self.angle > 0:
            if not self.stop() and not self.rob.estCrash:
                self.angle_parcouru += self.rob.angle_parcouru()
                self.logger.debug("angle de rotation parcouru : %d",self.angle_parcouru)
        else:
            if not self.stop() and not self.rob.estCrash:
                self.angle_parcouru -= self.rob.angle_parcouru()
                self.logger.debug("angle de rotation parcouru : %d",-self.angle_parcouru)


    def stop(self):

        """ Détermine si on a fini de faire la rotation de l'angle self.angle
            :returns: True si la rotation a bien été effectuée, False sinon
        """
        return  self.angle_parcouru >= self.angle if self.angle > 0 else self.angle_parcouru <= self.angle
    
    def getRob(self):
        """ Getter du robot qui est sous contrôle de la stratégie séquentielle
            :returns: le robot qui est sous le contrôle du contrôleur
        """
        return self.rob
    

class StrategieArretMur:
    def __init__(self, rob, distarret, env):
        """ Stategie qui fait arreter le robot a une distance donnée
            :param rob: le robot que l'on veut faire arreter avant un mur/obtacle
            :param distarret: la distance que l'on veut entre le robot et le mur/obstacle
            :param env: L'environemment pour le capteur de distance du robot simu
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        
        self.rob = rob
        self.distarret = distarret
        self.env = env
        self.distrob = self.rob.capteurDistance(env) # la distance entre le robot et le mur/obtacle le plus proche devant lui, obtenue avec le capteur de distance

    def start(self):
        """ Réinitialisation de la vitesse du robot et de la distance entre le robot et le mur/obstacle
        """
        self.rob.setVitAngA(4)
        self.distrob = self.rob.capteurDistance(self.env)
        
        self.logger.debug("Stratégie ArretMur lancée")

    def step(self):
        """ Le step de la stratégie arret mur : qui met à jour la distance entre le robot et le mur/obstacle devant lui
            :returns: rien, on met juste à jour la distance entre le robot et le mur/obstacle
        """
        if not self.stop():
            self.distrob = self.rob.capteurDistance(self.env)
        else:
            self.rob.setVitAngA(0)

    def stop(self):
        """ Détermine si la distance entre le robot et le mur/obstacle est plus petite ou égale a la distarret souhaitée
            :return: True si oui, non sinon
        """
        return self.distrob <= self.distarret

    def getRob(self):
        """
            Getter du robot qui est sous contrôle de la stratégie séquentielle
            :returns: le robot qui est sous le contrôle du contrôleur
        """
        return self.rob
    

class StrategieSeq:

    def __init__(self, listeStrat, rob) :
        """ Statégie séquentielle
            :param listeStrat: liste de stratégies qui vont être executées à la suite
            :param rob: le robot que l'on veut faire tourner
            :returns: rien, on initialise la stratégie séquentielle
        """
        self.listeStrat = listeStrat
        self.rob = rob
        self.indice = -1

    def start(self):
        self.indice = -1
        self.rob.estSousControle = True
        

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
            self.listeStrat[self.indice].rob.setVitAngA(0)

    def stop(self) :
        """ Détermine si la stratégie séquentielle est terminée, donc si toutes ses sous-stratégies son terminées
            :returns: True si toutes les stratégies ont bien été accomplies, False sinon
        """
        if self.indice == len(self.listeStrat)-1 and self.listeStrat[self.indice].stop() :
            self.rob.estSousControle = False
            return True
        return False
    
    def getRob(self):
        """
            Getter du robot qui est sous contrôle de la stratégie séquentielle
            :returns: le robot qui est sous le contrôle du contrôleur
        """
        return self.rob

class StrategieCond:
    def __init__(self, rob, strat, cond):
        """ Stratégie conditionnelle 
        :param rob: le robot que l'on veut faire executer la strat
        :param strat: la stratégie à executer tant que la cond est remplie
        :param cond: fonction conditionnelle / booleenne (ex: <module>.distSup(rob, 5) renverrai True si le captDist renvoie > 5)
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.rob = rob
        self.strat = strat
        self.cond = cond
        
    def start(self):
        self.logger.debug("Stratégie conditionnelle lancée")
        
        self.rob.estSousControle = True
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
            self.rob.estSousControle = False
            return True
        return False
    
    def getRob(self):
        """ Getter du robot qui est sous contrôle de la stratégie séquentielle
            :returns: le robot qui est sous le contrôle du contrôleur
        """
        return self.rob
    
    
class StrategieBoucle:
    def __init__(self, rob, strat, nbTours):
        """ Stratégie de boucle
        :param rob: le robot que l'on veut faire executer la strat
        :param strat: la stratégie à executer
        :param nbTours: nombre de tours que la boucle doit faire
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.rob = rob
        self.strat = strat
        self.nbTours = nbTours
        self.restants = self.nbTours
        
    def start(self):
        self.logger.debug("Stratégie de boucle lancée")
        self.restants = self.nbTours
        self.rob.estSousControle = True
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
            self.rob.estSousControle = False
            return True
        return False

    def getRob(self):
        """ Getter du robot qui est sous contrôle de la stratégie séquentielle
            :returns: le robot qui est sous le contrôle du contrôleur
        """
        return self.rob
             
        
def setStrategieCarre(rob, longueur_cote):
    avance = StrategieAvancer(rob, longueur_cote)
    tourne = StrategieTourner(rob, 90)
    carre  = StrategieSeq([avance, tourne, avance, tourne, avance, tourne, avance, tourne],rob)
    return carre

def setStrategieArretMur(rob, distarret, env) :
    arret = StrategieArretMur(rob, distarret, env)
    return arret

# Méthodes conditionnelles pour la stratCond
def distSup(rob, env, dist):
    """ Verifie que le robot est à une distance supérieure à dist d'un obstacle
    :param robot: le robot pour lequel on va utiliser le capteur de distance
    :param env: l'environnement du robot en question
    :param dist: la distance utilisée pour la condition
    """
    return (rob.capteurDistance(env)>dist)
