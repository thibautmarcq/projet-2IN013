from numpy import 

class Matrice :
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.matrice = np.empty((y,x))