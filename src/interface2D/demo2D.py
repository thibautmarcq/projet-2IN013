from logging import DEBUG, basicConfig
from threading import Thread
from time import sleep

from src import (HAUTEUR_ROBOT, LARGEUR_ENV, LARGEUR_ROBOT, LIST_PTS_OBS_CARRE,
                 LIST_PTS_OBS_COEUR, LIST_PTS_OBS_TRIANGLE, LONGUEUR_ENV,
                 LONGUEUR_ROBOT, SCALE_ENV_1, TAILLE_ROUE, TIC_SIMULATION,
                 Environnement, Controler, setStrategieCarre,
                 Adaptateur_reel, Adaptateur_simule, MockupRobot, Robot)

from src.interface2D.interface2D import Interface


basicConfig(filename='logs.log', 
            level=DEBUG, 
            format='%(asctime)s | %(levelname)s | %(name)s | %(message)s', 
            datefmt='%d/%m/%y %H:%M:%S', 
            encoding='UTF-8') # niveaux : DEBUG INFO WARNING ERROR CRITICAL

def loopEnv(env):
    """ La fonction de boucle de rafraîchissement de l'environnement
        :param env: l'environnement qu'on veut faire tourner
    """
    while True:
        env.refreshEnvironnement()
        sleep(TIC_SIMULATION)

env = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1) # Initialisation de l'env
T_env = Thread(target=loopEnv, args=[env], daemon=True)
T_env.start()
env.addObstacle('J',LIST_PTS_OBS_TRIANGLE)
env.addObstacle('P',LIST_PTS_OBS_CARRE)
env.addObstacle('C',LIST_PTS_OBS_COEUR)

#On crée un controleur
controleur = Controler()

# Ajout du premier robot
robot1 = Robot("Bob", 400, 250, LARGEUR_ROBOT, LONGUEUR_ROBOT, HAUTEUR_ROBOT, TAILLE_ROUE,"lightblue")
robotA1 = Adaptateur_simule(robot1, env)
env.setRobot(robotA1)


# Ajout du deuxième robot pour test
robot2 = Robot("Stuart", 250, 300, LARGEUR_ROBOT, LONGUEUR_ROBOT, HAUTEUR_ROBOT, TAILLE_ROUE,"red")
robotA2 = Adaptateur_simule(robot2, env)
env.setRobot(robotA2)

# Création du mockup robot
robMock = MockupRobot()

# Adapte le robot mockup pour le tester
robot3 = Adaptateur_reel(robMock)

T_env = Thread(target=loopEnv, args=[env], daemon=True)
T_env.start()

def menu2D(cmd):
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
