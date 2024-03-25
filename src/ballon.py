class Ballon:
    def __init__(self, x,y):
        """ Initialise le ballon
        :param x: coordonnée x
        :param y: coordonnée y
        """
        self.x = x
        self.y = y
        self.vitInit = 0
        self.direction = (0,0)