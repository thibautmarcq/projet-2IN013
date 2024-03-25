from src.Interface.interface import Interface
from src.environnement import Environnement
from src.Robot.robot import Robot,Adaptateur_simule
from src.Robot.mockupRobot import *
from threading import Thread
from time import sleep
from src.Controleur.controleur import Controler
from src.Controleur.Strategies import *
from src.constantes import *

def loopEnv(env):
    while True:
        env.refresh_env()
        sleep(TIC_SIMULATION)

env = Environnement(700, 700, 1) # Initialisation de l'env

T_env = Thread(target=loopEnv, args=[env], daemon=True)
T_env.start()

env.addObstacle('P',[(100,100),(150,100),(150,150), (100,150)])
env.addObstacle('P',[(500,100),(550,100),(550,150), (500,150)])
env.addObstacle('P',[(600,50),(650,50),(650,100), (600,100)])

env.addObstacle('J',[(600,500),(650,500),(650,550), (600,550)])

env.addObstacle('J',[(100,600),(150,600),(150,650), (100,650)])
#env.print_matrix()

#On crée un controleur
controleur = Controler()

# Ajoute le premier robot
robot = Adaptateur_simule("Bob", 350, 350, 30, 55, 20)

env.setRobot(robot, "lightgreen")


run = Interface(env, controleur)
run.mainloop()
