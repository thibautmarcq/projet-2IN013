from ..robot import Robot


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

    def step(self): # Fait augmenter l'angle parcouru + appelle la fonction touner de robot
        if (self.angle > 0) :
            self.angle_parcouru += 1
            self.rob.TourneGauche()
        if (self.angle < 0) :
            self.angle_parcouru -= 1
            self.rob.TourneDroite()

    def stop(self): #fait arreter le robot quand l'angle parcouru est supérieur ou égale à l'angle
        if self.angle_parcouru >= self.angle or self.angle_parcouru <= self.angle:
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

