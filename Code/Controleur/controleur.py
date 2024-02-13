from ..robot import Robot

class StrategieAvancer:
    def __init__(self, distance, vitesse, rob):
        """ Statégie qui fait avancer le robot d'une distance donnée"""
        self.distance = distance
        self.vitesse = vitesse
        self.rob = rob 
        self.parcouru = 0
        #argument temporaire
    
    def refresh(self): #Changement de vitesse ?
        pass

    def step(self): #Fait augmenter la distance parcourue ?
        pass

    def stop(self): # Fait arreter le robot quand la distance est inferieure a parcourue ?
        pass


class StrategieTourner:
    def __init__(self, rob, angle):
        """Stategie qui fait tourner le robot d'un angle donné"""
        self.rob = rob
        self.angle = angle
        #argument temporaire

    def tourne(self): #appelle la fonction tourner d robot?
        pass

    def stop(self): #fait arreter le robot quand il a tourné ?
        pass

