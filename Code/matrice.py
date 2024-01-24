import numpy as np

class Matrice :
    """La matrice sert à faire le lien entre la partie continue de l'environnement et la partie discrète
    Elle prend en attribut les obstacle et le robot sous forme discrète"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.matrice = np.empty((y,x))