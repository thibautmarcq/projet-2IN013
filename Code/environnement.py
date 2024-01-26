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
        self.matrice = Matrice.Matrice(int(width/scale),int(height/scale)) #Instanciation de la matrice - Matrice.Matrice(x,y) ??
        self.robots = []
        self.scale = scale

    def addRobot(self, nom, x, y):
        """Ajoute un robot a notre environnement"""
        rob = Robot(nom,x,y)
        self.robots.append(rob)
        self.matrice[int(x/self.scale)-1][int(y/self.scale)-1] = rob #met le robot dans la matrice

    def addObstacle(self,nom, x, y):
        """Ajout d'un obstacle dans la matrice"""
        obs = Obstacle(nom, x, y)
        x = random.randint(0,self.width) #prend des coordonnees aleatoires pour l'obstacle
        y = random.randint(0,self.height)
        self.matrice[x/self.scale-1][(y/self.scale)-1] = obs #met l'obstacle dans la matrice



    def affiche(self):
        #methodes pour affichage avec tkinter
        pass


env = Environnement(25,3)
env.trace()