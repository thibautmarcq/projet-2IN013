from Code.outil import *
import time
from threading import Thread


class Controler:

    def __init__(self):
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
                    self.strat_en_cour.listeStrat[len(self.strat_en_cour.listeStrat)-1].rob.setVitAng(0)
                    self.strat_en_cour = None
            time.sleep(1/(2**30))
  
    def setStrategie(self, strat):
        if self.strategie:
            print("Impossible de lancer la stratégie tant que le controleur n'est pas libre")
        self.strat_en_cour = strat
        self.strategie = 1

    def setStategieCarre(controleur, rob, longueur_cote):
        avance = StrategieAvancer(rob, longueur_cote)
        tourne = StrategieTourner(rob, 90)
        carre  = StrategieSeq([avance, tourne, avance, tourne, avance, tourne, avance, tourne])
        controleur.setStrategie(carre)
        


class StrategieAvancer:
    
    def __init__(self, rob, distance) :
        """ Statégie qui fait avancer le robot d'une distance donnée
            :param distance: la distance que doit parcourir le robot  
            :param rob: le robot qui va avancer
            :param parcouru: la distance parcourue du robot
            :returns: ne retourne rien, on initialise la stratégie
        """
        self.distance = distance
        self.rob = rob 
        self.parcouru = 0
        self.pt_depart = (self.rob.x, self.rob.y)
  
    def start(self) :
        self.rob.estSousControle = True
        self.parcouru = 0
        self.pt_depart = (self.rob.x, self.rob.y)
        self.rob.setVitAng(10) # Puis on augmente les vitesses angulaires de 10

    def step(self) : 
        """ On fait avancer le robot d'un petit pas
            :returns: rien, on met juste à jour la distance parcourue par le robot
        """
        if not self.stop() and not self.rob.estCrash:
            pos_actuelle = (self.rob.x, self.rob.y)
            self.parcouru = distance(self.pt_depart, pos_actuelle)
            print("distance parcouru:", self.parcouru)
            

    def stop(self): 
        """ Détermine si on a bien parcouru la distance souhaitée
            :returns: True si on a bien complété la stratégie, False sinon
        """
        if self.parcouru >= self.distance :
            self.rob.estSousControle = False
            return True
        return False


class StrategieTourner:
    
    def __init__(self, rob, angle):

        """ Stategie qui fait tourner le robot d'un angle donné
            :param rob: le robot que l'on veut faire tourner
            :param angle: la rotation que l'on veut ordonner au robot d'effectuer
        """

        self.rob = rob
        self.angle = angle
        self.angle_parcouru = 0
        self.dir_depart = self.rob.direction

    def start(self) :
        self.rob.estSousControle = True
        self.angle_parcouru = 0
        self.dir_depart = self.rob.direction


        # On considère ici une rotation d'un angle alpha dans le sens horaire, c.à.d si positif on tourne vers la droite, sinon vers la gauche
        # On change les vitesses des deux roues, en leur donnant des vitesses opposées afin de tourner sur place

        self.vitesseAng = 1
        
        self.rob.setVitAngG( self.vitesseAng  if self.angle > 0 else -self.angle > 0)
        self.rob.setVitAngD(-self.vitesseAng  if self.angle > 0 else  self.angle > 0)


    def step(self):

        """ Le step de la stratégie tourner, qui met a jour l'angle qui a été parcouru jusqu'à maintenant sinon
            :returns: ne retourne rien, on met juste a jour le paramètre distance parcourue
        """
        if not self.stop() and not self.rob.estCrash:
            self.angle_parcouru = getAngleFromVect(self.dir_depart, self.rob.direction)
        else:
            self.rob.setVitAng(0)
        print("angle:", self.angle_parcouru)


    def stop(self) : 

        """ Détermine si on a fini de faire la rotation de l'angle self.angle
            :returns: True si la rotation a bien été effectuée, False sinon
        """
        #if abs(self.angle_parcouru - self.angle) < 0.5  :
        if self.angle_parcouru >= self.angle:
            self.rob.estSousControle = False
            return True
        return False


class StrategieSeq:

    def __init__(self, listeStrat) :
        """ Statégie séquentielle
            :param listeStrat: liste de stratégies qui vont être executées à la suite
            :param indice: permet de parcourir la liste de stratégies
            :returns: rien, on initialise la stratégie séquentielle
        """
        self.listeStrat = listeStrat
        self.indice = -1
        self.last_refresh = 0

    def start(self):
        self.indice = -1
        self.last_refresh = 0
        

    def step(self) : 
        """ Le step de la stratégie séquentielle, où on fait le step de la stratégie en cours ou on passe a la stratégie suivante selon le cas, et on met à jour le robot
            :returns: rien, il s'agit juste de lancement de sous-stratégies et de mise à jour de robots
        """
        if not self.stop():
            if (self.indice < 0 or self.listeStrat[self.indice].stop()) and self.indice != len(self.listeStrat)-1: # Si on n'a pas encore commencé à lancer les stratégies unitaire ou si la stratégie en cours est terminée, on avance à la stratégie suivante
                self.indice += 1
                self.last_refresh = 0
                self.listeStrat[self.indice].start()

            self.listeStrat[self.indice].step() # On fait le step de la stratégie en cours 

        else:
            self.listeStrat[self.indice].rob.setVitAng(0)

    def stop(self) : 
        """ Détermine si la stratégie séquentielle est terminée, donc si toutes ses sous-stratégies son terminées 
            :returns: True si toutes les stratégies ont bien été accomplies, False sinon
        """
        return self.indice == len(self.listeStrat)-1 and self.listeStrat[self.indice].stop() 
    


class StrategieArretMur:
    def __init__(self, rob, distarret):
        """ Stategie qui fait arreter le robot a une distance donnée
            :param rob: le robot que l'on veut faire arreter avant un mur/obtacle
            :param angle: la distance que l'on veut entre le robot et le mur/obstacle
            :param distrob: la distance entre le robot et le mur/obtacle le plus proche devant lui, obtenue avec le capteur de distance 
        """
        self.rob = rob
        self.distarret = distarret
        self.distrob = self.rob.capteurDistance()

    def start(self):
        """ Réinitialisation de la vitesse du robot et de la distance entre le robot et le mur/obstacle
        """
        self.rob.setVitAng(1/20)
        self.distrob = self.rob.capteurDistance()

    def step(self):
        """ Le step de la stratégie arret mur : qui met à jour la distance entre le robot et le mur/obstacle devant lui
        """
        if not self.stop():
            self.distrob = self.rob.capteurDistance()
        else:
            self.rob.setVitAng(0)

    def stop(self):
        """ Détermine si la distance entre le robot et le mur/obstacle est plus petite ou égale a la distarret souhaitée 
            :return: True si oui, non sinon
        """
        return self.distrob <= self.distarret

        


