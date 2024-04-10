from threading import Thread
from time import sleep

from src import (HAUTEUR_ROBOT, LARGEUR_ENV, LARGEUR_ROBOT, LONGUEUR_ENV,
                 LONGUEUR_ROBOT, SCALE_ENV_1, TAILLE_ROUE, TIC_SIMULATION,
                 LIST_PTS_OBS_CARRE, LIST_PTS_OBS_COEUR, LIST_PTS_OBS_TRIANGLE,
                 Environnement)
from src.interface3D import Interface3D
from src.robots import Adaptateur_simule

envi = Environnement(LARGEUR_ENV, LONGUEUR_ENV, SCALE_ENV_1)

robot1 = Adaptateur_simule("moulinex3D", 400, 250, LARGEUR_ROBOT, LONGUEUR_ROBOT, HAUTEUR_ROBOT, TAILLE_ROUE, envi, "lightblue")
envi.setRobot(robot1)
robot2 = Adaptateur_simule("robocar3D", 250, 300, LARGEUR_ROBOT, LONGUEUR_ROBOT, HAUTEUR_ROBOT, TAILLE_ROUE, envi, "green")
envi.setRobot(robot2)
envi.addObstacle('J',LIST_PTS_OBS_TRIANGLE)
envi.addObstacle('P',LIST_PTS_OBS_CARRE)
envi.addObstacle('C',LIST_PTS_OBS_COEUR)

interface = Interface3D(envi)

def loopEnv(env):
    while True:
        env.refreshEnvironnement()
        sleep(TIC_SIMULATION)

T_env = Thread(target=loopEnv, args=[envi], daemon=True)
T_env.start()
# envi.printMatrix()


interface.run()