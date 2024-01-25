import numpy as np

import robot as Robot
import matrice as Matrice
import rectangle as Rectangle

class Environnement:
    
    def __init__(self, width, height, scale): #initialise l'environnement de taille x*y et l'echelle pour la matrice
        self.width=width; self.height=height
        # self.robot = Robot.Robot() #Voir avec ines les parametres
        self.matrice = Matrice.Matrice(int(width/scale),int(height/scale)) #Instanciation de la matrice - Matrice.Matrice(x,y) ??
        self.rectangle = None #Constructeur du rectangle
        self.robots = []

    def addRobot(self, robot):
        """Ajoute un robot a notre environnement"""
        self.robots.append(robot)


    def affiche(self):
        #methodes pour affichage avec tkinter
        pass


env = Environnement(25,3)
env.trace()