from src.Interface.interface import Interface
from src.environnement import Environnement
from src.Robot.robot import Robot,Adaptateur_simule
from threading import Thread
from time import sleep
from src.Controleur.controleur import Controler
from src.constantes import *


def loopEnv(env):
    while True:
        env.refresh_env()
        sleep(TIC_SIMULATION)
        
env = Environnement(750, 550, 1) # Initialisation de l'env
        
T_env = Thread(target=loopEnv, args=[env], daemon=True)
T_env.start()
        
#Ajout des obstacles
env.addObstacle('topMiddle',[(350,20),(400,20),(400,60), (350,60)])
env.addObstacle('topRight',[(620,20),(700,20),(700,120), (620,120)])
env.addObstacle('topLeft',[(50,60),(100,60),(100,100), (50,100)])
env.addObstacle('bottomLeft',[(20,480),(100,480),(100,540), (20,540)])
env.addObstacle('bottomRight',[(600,410),(700,410),(700,500), (600,500)])

robot = Adaptateur_simule("Bob", 375, 275, 30, 55, 20) #Crée le robot au milieu de la simulation
env.setRobot(robot, "lightgreen")


controleur = Controler() # Création du controleur pour lancer l'interface
run = Interface(env, controleur)


run.mainloop()