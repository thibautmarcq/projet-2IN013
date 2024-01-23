import numpy as np

class Environnement:
    
    def __init__(self, x, y): #initialise l'environnement de taille x*y
        self.matrice = self.init_matrice((int)(x), (int)(y)) #init de la matrice discret pour les obstacles
        self.rectangle = self.init_rectangle((float)(x), (float)(y)) #init du rectangle continu 
        
    def init_matrice(self, x, y):
        return (tab[x][y])

    def init_rectangle():
        return None

    def trace(self):
        for ligne in range(y):
            print("|", end="")
            for colonne in range(x):
                print("-", end="")
            print("|")
        






