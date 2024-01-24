import numpy as np

import robot as Robot ##
import matrice as Matrice
import rectangle as Rectangle

class Environnement:
    
    def __init__(self, x, y): #initialise l'environnement de taille x*y
        self.x=x; self.y=y
        # self.robot = Robot.Robot() #Voir avec ines les parametres
        self.matrice = Matrice.Matrice(x,y) #Instanciation de la matrice - Matrice.Matrice(x,y) ??
        self.rectangle = None #Constructeur du rectangle


    def affiche(self):
        #methodes pour affichage avec tkinter
        pass


env = Environnement(25,3)
env.trace()






