import numpy as np
import random 
 
import robot as Robot
import matrice as Matrice
import rectangle as Rectangle
import obstacle as Obstacle

class Environnement:
    
    def __init__(self, width, height, scale): #initialise l'environnement de taille x*y et l'echelle pour la matrice
        self.width=width; self.height=height
        # self.robot = Robot.Robot() #Voir avec ines les parametres
        self.matrice = Matrice.Matrice(int(width/scale),int(height/scale)) #Instanciation de la matrice - Matrice.Matrice(x,y) ??
        self.rectangle = None #Constructeur du rectangle
        self.robots = []
        self.scale = scale

    def addRobot(self, robot):
        """Ajoute un robot a notre environnement"""
        self.robots.append(robot)

    def addObstacle(self):
        x = random.uniform(0,self.width) #prend des coordonnees aleatoire pour l'obstacle
        y = random.uniform(0,self.height)
        self.matrice[int(x)-1][int(y)-1] = Obstacle(x,y) #met l'obstacle dans la matrice



    def affiche(self):
        #methodes pour affichage avec tkinter
        pass


env = Environnement(25,3)
env.trace()