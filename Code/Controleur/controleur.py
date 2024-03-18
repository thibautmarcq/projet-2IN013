from Code.outil import *
import time
from threading import Thread
import logging


class Controler:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.strat_en_cour = None
        self.strategie = 0
        self.Running = True
        t = Thread(target=self.mainControleur, daemon=True)
        t.start()

    def mainControleur(self):
        while self.Running:
            if self.strategie:
                if not self.strat_en_cour.stop():
                    self.strat_en_cour.step()
                else:
                    self.strategie = 0
                    self.strat_en_cour.getRob().setVitAng(0)
                    self.strat_en_cour = None
            time.sleep(1/(2**30))
  
    def setStrategie(self, strat):
        if self.strategie:
            # print("Impossible de lancer la stratégie tant que le controleur n'est pas libre")
            self.logger.error("Impossible de lancer la stratégie tant que le controleur n'est pas libre")
        self.strat_en_cour = strat
        self.strategie = 1
        self.strat_en_cour.start()

    def setStrategieCarre(self, rob, longueur_cote):
        avance = StrategieAvancer(rob, longueur_cote)
        tourne = StrategieTourner(rob, 90)
        carre  = StrategieSeq([avance, tourne, avance, tourne, avance, tourne, avance, tourne],rob)
        self.setStrategie(carre)

    def setStrategieArretMur(self, rob, distarret, env):
        arret = StrategieArretMur(rob, distarret, env)
        self.setStrategie(arret)
        


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

    def start(self) :
        self.logger.debug("Stratégie avancer démarée")
        self.rob.estSousControle = True
        self.parcouru = 0
        self.rob.setVitAngA(10) # Puis on augmente les vitesses angulaires de 10

    def step(self) : 
        """ On fait avancer le robot d'un petit pas
            :returns: rien, on met juste à jour la distance parcourue par le robot
        """
        if not self.stop() and not self.rob.estCrash:
            self.parcouru += self.rob.distance_parcourue()


    def stop(self): 
        """ Détermine si on a bien parcouru la distance souhaitée
            :returns: True si on a bien complété la stratégie, False sinon
        """
        return self.parcouru >= self.distance 

    def getRob(self):
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

    def start(self) :

        self.logger.debug("Stratégie tourner lancée")

        self.rob.estSousControle = True
        self.angle_parcouru = 0
        self.dir_depart = self.rob.direction


        # On considère ici une rotation d'un angle alpha dans le sens horaire, c.à.d si positif on tourne vers la droite, sinon vers la gauche
        # On change les vitesses des deux roues, en leur donnant des vitesses opposées afin de tourner sur place

        self.vitesseAng = 1
        
        self.rob.setVitAngGA(1  if self.angle > 0 else -1)
        self.rob.setVitAngDA(-1  if self.angle > 0 else 1)
        


    def step(self):

        """ Le step de la stratégie tourner, qui met a jour l'angle qui a été parcouru jusqu'à maintenant sinon
            :returns: ne retourne rien, on met juste a jour le paramètre distance parcourue
        """
        self.logger.debug(self.angle_parcouru)        
        if not self.stop() and not self.rob.estCrash:
            self.angle_parcouru += self.rob.angle_parcouru()


    def stop(self) : 

        """ Détermine si on a fini de faire la rotation de l'angle self.angle
            :returns: True si la rotation a bien été effectuée, False sinon
        """
        return self.angle_parcouru >= self.angle
    
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
        return self.rob
      


