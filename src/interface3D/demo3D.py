from threading import Thread
from time import sleep

from src import (HAUTEUR_ROBOT, LARGEUR_ENV, LARGEUR_ROBOT, LIST_PTS_OBS_CARRE,
                 LIST_PTS_OBS_COEUR, LIST_PTS_OBS_TRIANGLE, LONGUEUR_ENV,
                 LONGUEUR_ROBOT, SCALE_ENV_1, TAILLE_ROUE, TIC_SIMULATION,
                 Controler, Environnement, Adaptateur_simule, Robot)

from ..interface3D.interface3D import Interface3D

envi = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)

robot1 = Robot("moulinex3D", 400, 250, LARGEUR_ROBOT, LONGUEUR_ROBOT, HAUTEUR_ROBOT, TAILLE_ROUE,"lightblue")
robotA1 = Adaptateur_simule(robot1, envi)
envi.setRobot(robotA1)

robot2 = Robot("robocar3D", 250, 300, LARGEUR_ROBOT, LONGUEUR_ROBOT, HAUTEUR_ROBOT, TAILLE_ROUE,"green")
robotA2 = Adaptateur_simule(robot2, envi)
envi.setRobot(robotA2)

envi.addObstacle('J',LIST_PTS_OBS_TRIANGLE)
envi.addObstacle('P',LIST_PTS_OBS_CARRE)
envi.addObstacle('C',LIST_PTS_OBS_COEUR)


def loopEnv(envi):
    while True:
        envi.refreshEnvironnement()
        sleep(TIC_SIMULATION)

T_env = Thread(target=loopEnv, args=[envi], daemon=True)
T_env.start()
controleur = Controler()
def menu3D(cmd):
    """
    Fonction qui affiche un menu pour choisir une action
    """
    if cmd == "1":
        interface3D = Interface3D(envi, controleur)
        try: interface3D.run()
        except SystemExit:
            interface3D.running = False
            interface3D.destroy()


    elif cmd == "2":
        print("\nInformation de la simulation:")
        print("Width:", envi.width, "Length:", envi.length)
        print("Nombre de robots dans notre simulation:", len(envi.listeRobots))
        for robA in envi.listeRobots:
            print("------ Robot",robA.robot.nom,"------")
            print(f"vitAngG = {robA.robot.vitAngG}, vitAngD = {robA.robot.vitAngD}")
            print(f"Coords: ({robA.robot.x},{robA.robot.y}), Width: {robA.robot.width}, Length: {robA.robot.length}")
            print("Le robot n'est plus fonctionnel"if robA.robot.estCrash else "Le robot est toujours fonctionnel")
            print("Le robot n'est pas controlé par le controleur"if not robA.robot.estSousControle else "Le robot est controlé par le controleur")
            print("------------"+"-"*(len(robA.robot.nom)+2)+"------")
            