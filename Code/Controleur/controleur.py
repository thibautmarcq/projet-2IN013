from ..robot import Robot

class StrategieAvancer:
    def __init__(self, distance, vitesse, rob):
        """ Statégie qui fais avancer le robot d'une distance donnée"""
        self.distance = distance
        self.vitesse = vitesse
        self.rob = rob 
        self.parcouru = 0
        #argument temporaire
    
    def refresh(self): #Changement de vitesse ?
        pass

    def step(self): #Fais augmenter la distance parcouru ?
        pass

    def stop(self): # Fais arreter le robot quand la distance est inferieure a parcouru ?
        pass


class StrategieTourner:
    def __init__(self, rob, angle):
        """Stategie qui fais tourner le robot d'un angle donné"""
        self.rob = rob
        self.angle = angle
        #argument temporaire

    def tourne(self): #appele la fonction tourner d robot?
        pass

    def stop(self): #fais arreter le robot quand il a tourner ?
        pass

