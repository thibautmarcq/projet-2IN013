from logging import DEBUG, basicConfig
from threading import Thread
from time import sleep

from src.constantes import (HAUTEUR_ROBOT, LARGEUR_ENV, LARGEUR_ROBOT,
                            LIST_PTS_OBS_CARRE, LIST_PTS_OBS_COEUR,
                            LIST_PTS_OBS_TRIANGLE, LONGUEUR_ENV,
                            LONGUEUR_ROBOT, SCALE_ENV_1, TAILLE_ROUE,
                            TIC_SIMULATION)
from src.Controleur.controleur import Controler
from src.Controleur.strategies import setStrategieCarre
from src.environnement import Environnement
from src.Interface.interface import Interface
from src.Robot.mockupRobot import Adaptateur_reel
from src.Robot.robot import Adaptateur_simule

basicConfig(filename='logs.log', 
                    level=DEBUG, 
                    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s', 
                    datefmt='%d/%m/%y %H:%M:%S', 
                    encoding='UTF-8') # niveaux : DEBUG INFO WARNING ERROR CRITICAL

def loopEnv(env):
    while True:
        env.refreshEnvironnement()
        sleep(TIC_SIMULATION)

env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1) # Initialisation de l'env
T_env = Thread(target=loopEnv, args=[env], daemon=True)
T_env.start()
env.addObstacle('J',LIST_PTS_OBS_TRIANGLE)
env.addObstacle('P',LIST_PTS_OBS_CARRE)
env.addObstacle('C',LIST_PTS_OBS_COEUR)
#env.printMatrix()

#On crée un controleur
controleur = Controler()

# Ajoute le premier robot
robotA1 = Adaptateur_simule("Bob", 250, 250, LARGEUR_ROBOT, LONGUEUR_ROBOT, HAUTEUR_ROBOT, TAILLE_ROUE, env, "lightgreen")
env.setRobot(robotA1)


# ajoute le deuxieme robot pour test
robotA2 = Adaptateur_simule("Stuart", 400, 250, LARGEUR_ROBOT, LONGUEUR_ROBOT, HAUTEUR_ROBOT, TAILLE_ROUE, env, "red")
env.setRobot(robotA2)

# Ajoute un robot réel pour le tester
robot3 = Adaptateur_reel()

T_env = Thread(target=loopEnv, args=[env], daemon=True)
T_env.start()

def menu(cmd):
    """
    Fonction qui affiche un menu pour choisir une action
    """
    if cmd == "1":
        run = Interface(env, controleur)
        run.mainloop()

    elif cmd == "2":
        print("\nInformation de la simulation:")
        print("Width:", env.width, "Length:", env.length)
        print("Nombre de robots dans notre simulation:", len(env.listeRobots))
        for robA in env.listeRobots:
            print("------ Robot",robA.robot.nom,"------")
            print(f"vitAngG = {robA.robot.vitAngG}, vitAngD = {robA.robot.vitAngD}")
            print(f"Coords: ({robA.robot.x},{robA.robot.y}), Width: {robA.robot.width}, Length: {robA.robot.length}")
            print("Le robot n'est plus fonctionnel"if robA.robot.estCrash else "Le robot est toujours fonctionnel")
            print("Le robot n'est pas controlé par le controleur"if not robA.robot.estSousControle else "Le robot est controlé par le controleur")
            print("------------"+"-"*(len(robA.robot.nom)+2)+"------")
            
    elif cmd == "3" :
        long = float(input("Quelle largeur voulez-vous pour le carré ? \n"))
        carre = setStrategieCarre(robot3, long)
        controleur.lancerStrategie(carre)
