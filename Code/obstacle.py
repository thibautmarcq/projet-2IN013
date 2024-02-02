class Obstacle :
    """ L'obsctacle est un objet aux coordonnées discrètes, se place dans la matrice de l'environnement 
    """

    def __init__(self, nom, x, y) :

        """ Constructeur de l'obstacle, il crée et initialise un obstacle en fonction des coordonnées passées en paramètre
            :param x: coordonnée x initiale de l'obstacle
            :param y: coordonnée y initiale de l'obstacle
            :returns: ne retourne rien, crée uniquement l'obstacle
        """
        
        self.nom = nom
        self.x = x
        self.y = y

    def presenter_obstacle(self):
        """Affichage (console) de l'obstacle"""
        print("Je suis l'obstacle " + self.nom + " et je suis à la position(", self.x,", ", self.y,")")
