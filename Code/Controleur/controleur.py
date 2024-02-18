from ..robot import Robot

class StrategieAvancer:
    def __init__(self, distance, rob):
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
            return 0


class StrategieTourner:
    def __init__(self, rob, angle):
        """Stategie qui fait tourner le robot d'un angle donné"""
        self.rob = rob
        self.angle = angle
        self.angle_parcouru = 0

    def step(self): # Fait augmenter l'angle parcouru + appelle la fonction touner de robot
        pass

    def stop(self): #fait arreter le robot quand l'angle parcouru est supérieur ou égale à l'angle
        pass

