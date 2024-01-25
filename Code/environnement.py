import numpy as np
import random 
 
import robot as Robot
import matrice as Matrice
import rectangle as Rectangle
import obstacle as Obstacle

class Environnement:
    
    def __init__(self, width, height, scale): #initialise l'environnement de taille x*y 
        #scale = l'echelle c'est un int ainsi scale = la taille d'un cot'e d'une case de la matrice dans dans le rectangle?
        self.width=width; self.height=height
        # self.robot = Robot.Robot() #Voir avec ines les parametres
        self.matrice = Matrice.Matrice(int(width/scale),int(height/scale)) #Instanciation de la matrice - Matrice.Matrice(x,y) ??
        self.rectangle = None #Constructeur du rectangle
        self.robots = []
        self.scale = scale

    def addRobot(self, nom, x, y):
        """Ajoute un robot a notre environnement"""
        self.robots.append(Robot(nom,x,y))
        self.matrice[int(x/self.scale)-1][int(y/self.scale)-1] = nom #met le robot dans la matrice (representer par son nom dans la matrice)

    def addObstacle(self,nom):
        """Ajout d'un obstacle dans la matrice"""
        x = random.uniform(0,self.width) #prend des coordonnees aleatoire pour l'obstacle
        y = random.uniform(0,self.height)
        self.matrice[int(x/self.scale)-1][int(y/self.scale)-1] = nom #met l'obstacle dans la matrice (representer par son nom dans la matrice)



    def affiche(self):
        #methodes pour affichage avec tkinter
        pass


env = Environnement(25,3)
env.trace()