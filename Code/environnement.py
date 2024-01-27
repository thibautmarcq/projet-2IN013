import random

import obstacle as Obstacle
import robot as Robot

#import numpy as np




class Environnement:
    
    def __init__(self, width, height, scale): #initialise l'environnement de taille x*y 
        #scale = l'echelle c'est un int ainsi scale = la taille d'un cot'e d'une case de la matrice dans dans le rectangle?
        self.width=width; self.height=height
        self.matrice = [[None] * int(width/scale)] * int(height/scale) # Création d'une matrice int(width/scale)*int(height/scale) avec que des Nones (Plus lent que np.empty)
        self.robots = []
        self.scale = scale

    def addRobot(self, nom, x, y, L,l,vit):
        """Ajoute un robot a notre environnement"""
        rob = Robot.Robot(nom,x,y,L,l,vit)
        self.robots.append(rob)
        self.matrice[int(x/self.scale)][int(y/self.scale)] = rob #met le robot dans la matrice

    def addObstacle(self,nom):
        """Ajout d'un obstacle dans la matrice"""
        x = random.randint(0,self.width) #prend des coordonnees aleatoires pour l'obstacle
        y = random.randint(0,self.height)
        obs = Obstacle.Obstacle(nom, x, y)
        self.matrice[int(x/self.scale)][int(y/self.scale)] = obs #met l'obstacle dans la matrice

    def detect_obs(self, n) :
        """
            La fonction prend en paramètre n qui correspond au n-ième robot de la liste robots
            Detection d'un obstacle a l'avant et a l'arriere pour avancer ou reculer
            Detection d'un obstacle sur les cotes pour faire une rotation à droite ou à gauche
            Si il y a un obstacle renvoie True sinon False
            L'utiliser avant de faire un déplacement
        """
        obs = False
        # Detecte si il y a un obstacle devant
        if ( isinstance(self.matrice[self.robots[n].posx+1][self.robots[n].posy], Obstacle.Obstacle) ) :
            print("Il y a un obstacle devant le robot ne peut pas avancer")
            obs = True
        # Detecte si il y a un obstacle devant
        if ( isinstance(self.matrice[self.robots[n].posx-1][self.robots[n].posy], Obstacle.Obstacle) ) :
            print("Il y a un obstacle derriere le robot ne peut pas reculer")
            obs = True
        # Detecte si il y a un obstacle à droite
        if ( isinstance(self.matrice[self.robots[n].posx][self.robots[n].posy+1], Obstacle.Obstacle) ) :
            print("Il y a un obstacle à droite le robot ne peut pas faire de rotation à droite")
            obs = True
        # Detecte si il y a un obstacle à gauche
        if ( isinstance(self.matrice[self.robots[n].posx][self.robots[n].posy-1], Obstacle.Obstacle) ) :
            print("Il y a un obstacle à gauche le robot ne peut pas faire de rotation à gauche")
            obs = True

        return obs

    def affiche(self):
        #methodes pour affichage avec tkinter
        pass


env = Environnement(50,20,5)
