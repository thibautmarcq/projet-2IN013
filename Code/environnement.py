import numpy as np
import random 
 
import robot as Robot
import obstacle as Obstacle

class Environnement:
    
    def __init__(self, width, height, scale): #initialise l'environnement de taille x*y 
        #scale = l'echelle c'est un int ainsi scale = la taille d'un cot'e d'une case de la matrice dans dans le rectangle?
        self.width=width; self.height=height
        self.matrice = [[None for _ in range(width)] for _ in range(height)] # Matrice python basique - initialisation avec taille
        self.robots = []
        self.scale = scale

    def addRobot(self, nom, x, y):
        """Ajoute un robot a notre environnement"""
        rob = Robot(nom,x,y)
        self.robots.append(rob)
        self.matrice[int(x/self.scale)-1][int(y/self.scale)-1] = rob #met le robot dans la matrice

    def addObstacle(self,nom):
        """Ajout d'un obstacle dans la matrice"""
        x = random.randint(0,self.width) #prend des coordonnees aleatoires pour l'obstacle
        y = random.randint(0,self.height)
        obs = Obstacle(nom, x, y)
        self.matrice[x/self.scale-1][(y/self.scale)-1] = obs #met l'obstacle dans la matrice



    def affiche(self):
        #methodes pour affichage avec tkinter
        pass


env = Environnement(25,3)
env.trace()