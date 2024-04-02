from src.environnement import Environnement
from src.Interface3D.interface3D import Interface3D
from src.Robot.robot import Adaptateur_simule
from src.constantes import (LARGEUR_ENV, LONGUEUR_ENV, LARGEUR_ROBOT, LONGUEUR_ROBOT, 
                            HAUTEUR_ROBOT, TAILLE_ROUE, SCALE_ENV_1, TIC_SIMULATION)

from time import sleep
from threading import Thread


envi = Environnement(LARGEUR_ENV+500, LONGUEUR_ENV+500, SCALE_ENV_1)

robot1 = Adaptateur_simule("moulinex3D", 25, 46, LARGEUR_ROBOT, LONGUEUR_ROBOT, HAUTEUR_ROBOT, TAILLE_ROUE, envi, "lightblue")
envi.setRobot(robot1)
robot2 = Adaptateur_simule("robocar3D", 250, 100, LARGEUR_ROBOT, LONGUEUR_ROBOT, HAUTEUR_ROBOT, TAILLE_ROUE, envi, "green")
envi.setRobot(robot2)

interface = Interface3D(envi)

def loopEnv(env):
    while True:
        env.refreshEnvironnement()
        sleep(TIC_SIMULATION)

T_env = Thread(target=loopEnv, args=[envi], daemon=True)
T_env.start()
# envi.printMatrix()


interface.run()