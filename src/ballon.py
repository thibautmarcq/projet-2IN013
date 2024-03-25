from src.outil import *
import math
class Ballon:

    def __init__(self, x, y, cote):
        self.x = x
        self.y = y
        self.cote = cote # notre ballon est carré donc mesure d'un coté
        self.vitesse = 5
        self.direction = (0,-1)

    def setVitesse(self, x):
        self.vitesse = x
    

    def update(self, dt):
        self.setVitesse(max(0, (self.vitesse-dt*(0.01*self.vitesse*self.vitesse - 0.06 * self.vitesse ))))

		# et on fait notre déplacement
        self.x += self.direction[0]*self.vitesse
        self.y += self.direction[1]*self.vitesse
