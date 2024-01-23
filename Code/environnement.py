import numpy as np

import robot as Robot
import matrice as Matrice
import rectangle as Rectangle

class Environnement:
    
    def __init__(self, x, y): #initialise l'environnement de taille x*y
        self.robot = Robot() #Voir avec ines les parametres
        self.matrice = Matrice(x,y) #Instanciation de la matrice - Matrice.Matrice(x,y) ??
        self.rectangle = None #Constructeur du rectangle




    def trace(self):
        """Permet de tracer un environnement"""
        for ligne in range(y):
            print("|", end="") #Permet de ne pas sauter à la ligne à ch fois
            for colonne in range(x):
                if (ligne==0) or (ligne==self.matrice.y): #Premiere ou derniere ligne
                    print("-", end="") #Contour haut de la box

                ## RECHERCHE DELEMENTS ET PRINT EN FCT
                # if isinstance(self.matrice, Obstacle):
                    # print("x")
                # if - in 
                
                else :
                    print(" ", end="") #Espace (rien dans la case)

            print("|")
        






