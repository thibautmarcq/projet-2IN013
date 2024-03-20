from Code.Interface.interface import Interface
from Code.environnement import Environnement
from Code.Robot.robot import Robot, Adaptateur_simule
from Code.Robot.mockupRobot import *
from threading import Thread
from time import sleep
from Code.Controleur.controleur import Controler
from Code.Controleur.Strategies import *
from Code.constantes import *

import logging

logging.basicConfig(filename='logs.log', 
                    level=logging.DEBUG, 
                    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s', 
                    datefmt='%d/%m/%y %Hh%M', 
                    encoding='UTF-8') # niveaux : DEBUG INFO WARNING ERROR CRITICAL

def loopEnv(env):
    while True:
        env.refresh_env()
        sleep(TIC_SIMULATION)

env = Environnement(750, 550, 1) # Initialisation de l'env
T_env = Thread(target=loopEnv, args=[env], daemon=True)
T_env.start()
env.addObstacle('J',[(400,400),(450,450),(350,450)])
env.addObstacle('P',[(300,300),(350,300),(350,350), (300,350)])
env.addObstacle('C',[(100,140),(170,55),(160,30), (130,30), (100,50), (70,30), (40,30), (30,55)])
env.print_matrix()

#On créer un controleur
controleur = Controler()

# Ajoute le premier robot
robot = Adaptateur_simule("Bob", 250, 250, 30, 55, 20)

env.setRobot(robot, "lightgreen")


# ajoute le deuxieme robot pour test
robot2 = Adaptateur_simule("Stuart", 400, 250, 30, 55, 20)
env.setRobot(robot2, "red")

# Ajoute un robot réel pour le tester
robot3 = Adaptateur()

def menu():
    global RUNNING
    print("0 - Quit ( termine la simmu et arrete le programme )")
    print("1 - Lance une interface Graphique ")
    print("2 - afficher les infos de la simulation")
    print("3 - faire tracer un carré au robot réel")
    cmd = input("Veuillez choisir une action:\n")
    if cmd == "0":
        RUNNING = False

    elif cmd == "1":
        run = Interface(env, controleur)
        run.mainloop()

    elif cmd == "2":
        print("\nInformation de la simulation:")
        print("Width:", env.width, "Length:", env.length)
        print("Nombre de robots dans notre simulation:", len(env.robots))
        for rob in env.robots:
            print("------ Robot",rob.nom,"------")
            print(f"vitAngG = {rob.vitAngG}, vitAngD = {rob.vitAngD}")
            print(f"Coords: ({rob.x},{rob.y}), Width: {rob.width}, Length: {rob.length}")
            print("Le robot n'est plus fonctionnel"if rob.estCrash else "Le robot est toujours fonctionnel")
            print("Le robot n'est pas controlé par le controleur"if not rob.estSousControle else "Le robot est controlé par le controlleur")
            print("------------"+"-"*(len(rob.nom)+2)+"------")
            
    elif cmd == "3" :
        long = float(input("Quelle largeur voulez-vous pour le carré ? \n"))
        carre = setStrategieCarre(robot3, long)
        controleur.lancerStrategie(carre)



RUNNING = True

while RUNNING:
    menu()