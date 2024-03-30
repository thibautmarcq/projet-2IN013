from logging import DEBUG, basicConfig
from threading import Thread
from time import sleep

from src.constantes import (LARGEUR_ENV, LARGEUR_ROBOT, LIST_PTS_OBS_CARRE,
                            LIST_PTS_OBS_COEUR, LIST_PTS_OBS_TRIANGLE,
                            LONGUEUR_ENV, LONGUEUR_ROBOT, SCALE_ENV_1,
                            TAILLE_ROUE, TIC_SIMULATION)
from src.Controleur.controleur import Controler
from src.Controleur.Strategies import setStrategieCarre
from src.environnement import Environnement
from src.Interface.interface import Interface
from src.Robot.mockupRobot import Adaptateur
from src.Robot.robot import Adaptateur_simule

basicConfig(filename='logs.log', 
                    level=DEBUG, 
                    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s', 
                    datefmt='%d/%m/%y %H:%M:%S', 
                    encoding='UTF-8') # niveaux : DEBUG INFO WARNING ERROR CRITICAL

def loopEnv(env):
    while True:
        env.refresh_env()
        sleep(TIC_SIMULATION)

env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1) # Initialisation de l'env
T_env = Thread(target=loopEnv, args=[env], daemon=True)
T_env.start()
env.addObstacle('J',LIST_PTS_OBS_TRIANGLE)
env.addObstacle('P',LIST_PTS_OBS_CARRE)
env.addObstacle('C',LIST_PTS_OBS_COEUR)
#env.print_matrix()

#On crée un controleur
controleur = Controler()

# Ajoute le premier robot
robot = Adaptateur_simule("Bob", 250, 250, LARGEUR_ROBOT, LONGUEUR_ROBOT, TAILLE_ROUE, env)

env.addRobot(robot, "lightgreen")


# ajoute le deuxieme robot pour test
robot2 = Adaptateur_simule("Stuart", 400, 250, LARGEUR_ROBOT, LONGUEUR_ROBOT, TAILLE_ROUE, env)
env.addRobot(robot2, "red")

# Ajoute un robot réel pour le tester
robot3 = Adaptateur()

def menu():
    global RUNNING
    print("0 - Quit (termine la simulation et arrête le programme)")
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
            print("------ Robot",rob.robot.nom,"------")
            print(f"vitAngG = {rob.robot.vitAngG}, vitAngD = {rob.robot.vitAngD}")
            print(f"Coords: ({rob.robot.x},{rob.robot.y}), Width: {rob.robot.width}, Length: {rob.robot.length}")
            print("Le robot n'est plus fonctionnel"if rob.robot.estCrash else "Le robot est toujours fonctionnel")
            print("Le robot n'est pas controlé par le controleur"if not rob.estSousControle else "Le robot est controlé par le controlleur")
            print("------------"+"-"*(len(rob.robot.nom)+2)+"------")
            
    elif cmd == "3" :
        long = float(input("Quelle largeur voulez-vous pour le carré ? \n"))
        carre = setStrategieCarre(robot3, long)
        controleur.lancerStrategie(carre)



RUNNING = True

while RUNNING:
    menu()