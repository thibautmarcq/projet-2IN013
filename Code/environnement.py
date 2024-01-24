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


    def trace(self):
        """Permet de tracer un environnement"""
        for ligne in range((self.y)+1):
            print("|", end="") #Permet de ne pas sauter à la ligne à ch fois
            for colonne in range(self.x):
                if (ligne==0) or (ligne==(self.y)+1): #self.y = derniere lg de l'env, on veut la ligne d'après pr le cadre
                    print("-", end="") #Contour de la box

                ## RECHERCHE DELEMENTS ET PRINT EN FCT
                # if isinstance(self.matrice, Obstacle):
                    # print("x")
                # if - in 
                
                print(" ", end="") #Espace (rien dans la case)

            print("|")


env = Environnement(25,3)
env.trace()






