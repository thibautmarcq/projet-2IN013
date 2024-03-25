from src.Interface.interface import Interface
from src.environnement import Environnement
from src.Robot.robot import Robot,Adaptateur_simule
from src.Robot.mockupRobot import *
from threading import Thread
from time import sleep
from src.Controleur.controleur import Controler
from src.Controleur.Strategies import *
from src.constantes import *
from src.ballon import Ballon

def loopEnv(env):
    while True:
        env.refresh_env()
        sleep(TIC_SIMULATION)

env = Environnement(700, 700, 1) # Initialisation de l'env

T_env = Thread(target=loopEnv, args=[env], daemon=True)
T_env.start()

#env.print_matrix()

#On crée un controleur
controleur = Controler()

# Ajoute le premier robot
robot = Adaptateur_simule("Bob", 350, 350, 30, 55, 20)

env.ballon = Ballon(200, 200, 50)

env.setRobot(robot, "lightgreen")


run = Interface(env, controleur)
run.mainloop()
