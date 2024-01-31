import random

import numpy as np

import obstacle as Obstacle
import robot as Robot


class Environnement:
    
    def __init__(self, width, height, scale): #initialise l'environnement de taille x*y 
        #scale = l'echelle c'est un int ainsi scale = la taille d'un cot'e d'une case de la matrice dans dans le rectangle?
        self.width=width; self.height=height
        self.matrice = np.empty([int(width/scale), int(height/scale)], dtype=int) # Création d'une matrice int(width/scale)*int(height/scale) grâce à np.empty
        self.robots = []
        self.scale = scale

    def addRobot(self, nom, x, y, width, length, vitesse):
        """Ajoute un robot a notre environnement"""
        rob = Robot.Robot(nom, x, y, width, length, vitesse)
        self.robots.append(rob)
        self.matrice[int(x/self.scale)][int(y/self.scale)] = 1 # Ajoute le robot représenté par le chiffre 1 dans la matrice

    def addObstacle(self,nom):
        """Ajout d'un obstacle dans la matrice"""
        oqp = False
        while( oqp == False ) :
            random_x = random.randrange(0,self.width) #prend des coordonnees aleatoires pour l'obstacle
            random_y = random.randrange(0,self.height)
            x = int(random_x/self.scale)
            y = int(random_y/self.scale)
            if ( self.matrice[x][y] != 1 | self.matrice[x][y] != 2) :
                Obstacle.Obstacle(nom, x, y)
                self.matrice[x][y] = 2 #  Ajoute l'obstacle représenté par le chiffre 2 dans la matrice
                oqp = True

    def detect_obs(self, rob) :
        """
            Detection d'obstacle autour du robot

            Param : rob : Objet de type Robot

            Renvoie True si il y a un obstacle sinon False
        """
        obs = False
        # Detecte si il y a un obstacle devant
        if ( isinstance(self.matrice[rob.x+1][rob.y], Obstacle.Obstacle) ) :
            print("Il y a un obstacle devant, le robot ne peut pas avancer")
            obs = True
        # Detecte si il y a un obstacle devant
        if ( isinstance(self.matrice[rob.x-1][rob.y], Obstacle.Obstacle) ) :
            print("Il y a un obstacle derriere, le robot ne peut pas reculer")
            obs = True
        # Detecte si il y a un obstacle à droite
        if ( isinstance(self.matrice[rob.x][rob.y+1], Obstacle.Obstacle) ) :
            print("Il y a un obstacle à droite, le robot ne peut pas faire de rotation à droite")
            obs = True
        # Detecte si il y a un obstacle à gauche
        if ( isinstance(self.matrice[rob.x][rob.y-1], Obstacle.Obstacle) ) :
            print("Il y a un obstacle à gauche, le robot ne peut pas faire de rotation à gauche")
            obs = True

        return obs

    def affiche(self):
        #methodes pour affichage avec tkinter
        pass


env = Environnement(50,20,5)
print(env.height)
