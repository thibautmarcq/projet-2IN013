from ..robot import Robot
from Code.outil import *
import time

class StrategieAvancer:
    def __init__(self, rob, distance):
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
        self.debut = 0
    
    def step(self): #Fait augmenter la distance parcourue + appelle la fonction avancerdirection
        """ On fait avancer le robot d'un petit pas
            :returns: rien, on met juste à jour la distance parcourue par le robot
        """
        if self.debut < 1:
            self.debut = 1
            self.rob.setVitAng(0) # On initialise les vitesses angulaires des deux roues à 0
            self.rob.changeVitAng(0.1) # Puis on augmente les vitesses angulaires de 0.1

        else :
            pos_actuelle = (self.rob.x, self.rob.y)
            self.parcouru = distance(self.pt_depart, pos_actuelle)
        

    def stop(self): # Fait arreter le robot quand la distance parcourue est supérieur ou égale à la distance que l'on souhaitait parcourir
        if self.parcouru >= self.distance:
            self.rob.setVitAng(0)
            return True


class StrategieTourner:
    def __init__(self, rob, angle):
        """Stategie qui fait tourner le robot d'un angle donné"""
        self.rob = rob
        self.angle = angle
        self.angle_parcouru = 0
        self.dir_depart = self.rob.direction
        self.debut = 0

    def step(self):

        if (self.debut < 1) : # Dans le cas où c'est le premier step, on initialise tout pour se mettre dans les bonnes conditions
            self.debut = 1
            self.rob.setVitAng(0)

            # On considère ici une rotation d'un angle alpha dans le sens horaire, c.à.d si positif on tourne vers la droite, sinon vers la gauche
            # On change les vitesses des deux roues, en leur donnant des vitesses opposées afin de tourner sur place
            if self.angle > 0 :
                self.rob.changeVitAngG(0.1)
                self.rob.changeVitAngD(-0.1)

            elif self.angle < 0 :
                self.rob.changeVitAngD(0.1)
                self.rob.changeVitAngG(-0.1)

        else : # Si ce n'est pas le premier step, on met à jour l'angle parcouru par le robot
            self.angle_parcouru = getAngleFromVect(self.dir_depart, self.rob.direction)


    def stop(self): #fait arreter le robot lorsqu'on a parcouru l'angle souhaité
        if self.angle_parcouru >= self.angle :
            self.rob.setVitAng(0)
            return True


class StrategieSeq:
    def __init__(self, listeStrat):
        """ Statégie séquentielle
            :param listeStrat: liste de stratégies qui vont être executées à la suite
            :param indice: permet de parcourir la liste de stratégies
        """
        self.listeStrat = listeStrat
        self.indice = -1
        self.last_refresh = 0

    def step(self): # Tant que la strategie en cours n'est pas arretée on passe pas à la prochaine stratégie
        if self.indice < 0 or self.listeStrat[self.indice].stop(): 
            self.indice += 1
            self.last_refresh = 0

        self.listeStrat[self.indice].step()

        now = time.time()
        if self.last_refresh == 0 :
            self.last_refresh = now
        duree = now - self.last_refresh()
        
        self.listeStrat[self.indice].rob.refresh(duree)


    def stop(self): # S'arrête quand l'indice est sur la dernière strat de la liste et que celle-ci est arretée
        return self.indice == len(self.listeStrat)-1 and self.listeStrat[self.indice].stop() 

