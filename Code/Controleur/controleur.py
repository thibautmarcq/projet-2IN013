from ..robot import Robot

class StrategieAvancer:
    def __init__(self, distance, rob):
        """ Statégie qui fait avancer le robot d'une distance donnée"""
        self.distance = distance
        self.rob = rob 
        self.parcouru = 0
        #argument temporaire
    

    def step(self): #Fait augmenter la distance parcourue
        self.parcouru += 1
        self.rob.avancerDirection(1)

    def stop(self): # Fait arreter le robot quand la distance est inferieure a parcourue 
        return self.parcouru >= self.distance


class StrategieTourner:
    def __init__(self, rob, angle):
        """Stategie qui fait tourner le robot d'un angle donné"""
        self.rob = rob
        self.angle = angle
        #argument temporaire

    def step(self): #appelle la fonction tourner d robot
        pass

    def stop(self): #fait arreter le robot quand il a tourné
        pass

