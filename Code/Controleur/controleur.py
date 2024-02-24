from ..robot import Robot
from Code.outil import *

class StrategieAvancer:
    def __init__(self, rob, distance):
        """ Statégie qui fait avancer le robot d'une distance donnée
            :param distance: la distance que doit parcourir le robot  
            :param rob: le robot qui va avancer
            :param parcouru: la distance parcourue du robot
        """
        self.distance = distance
        self.rob = rob 
        self.parcouru = 0
    

    def step(self): #Fait augmenter la distance parcourue + appelle la fonction avancerdirection
        self.parcouru += 1
        self.rob.avancerDirection(1)

    def stop(self): # Fait arreter le robot quand la distance parcourue est supérieur ou égale à la distance
        if self.parcouru >= self.distance:
            self.rob.setVitesse(0)
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
            self.rob.setVitesse(0)

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
            self.rob.setVitesse(0)
            return True


class StrategieSeq:
    def __init__(self, listeStrat):
        """ Statégie sequentielle
            :param listeStrat: liste de strategies qui vont etre executé à la suite
            :param indice: qui permet de parcourir la liste de strategies
        """
        self.listeStrat = listeStrat
        self.indice = -1

    def step(self): # Tant que la strategie en cours n'est pas arreté on passe pas a la prochaine strategie
        if self.indice < 0 or self.listeStrat[self.indice].stop(): 
            self.indice += 1
        self.listeStrat[self.indice].step()


    def stop(self): # S'arrete quand l'indice est sur la dernière strat de la liste et que celle-ci est arreté
        return self.indice == len(self.listeStrat)-1 and self.listeStrat[self.indice].stop() 

