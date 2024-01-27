class Obstacle :
    """Obstacle - Objet aux coordonnées discrètes, se place dans la matrice de l'environnement """

    def __init__(self, nom, posx, posy) :
        """Constructeur de l'obstacle - Prend un nom et des coordonnées entières"""
        self.nom = nom
        self.x = posx
        self.y = posy

    def presenter_obstacle(self):
        """Affichage (console) de l'obstacle"""
        print("Je suis l'obstacle " + self.nom + " et je suis à la position(", self.x,", ", self.y,")")
