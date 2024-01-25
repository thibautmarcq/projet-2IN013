class Obstacle :

    def __init__(self, nom, posx, posy) :
        self.nom = nom
        self.x = posx
        self.y = posy

    def presenter_obstacle(self):
        return(self.nom + "à la position (" + str(self.x) + ", " + str(self.y) + ")")
