from src.Controleur.controleur import *
from src.Controleur.Strategies import *
from src.Interface.interface import *
from src.Robot.robot import *
from src.constantes import *
from src.environnement import *
from src.obstacle import *
from src.outil import *

from time import sleep


def loopEnv(env):
    while True:
        env.refresh_env()
        sleep(TIC_SIMULATION)

def q1_1() :

    controleur = Controler()
    robot = Adaptateur_simule("Rob1", 375, 275, 30, 55, 20)

    env1 = Environnement(750, 550, 1)
    T_env = Thread(target=loopEnv, args=[env1], daemon=True)
    T_env.start()

    env1.addObstacle("obs1", [ (100,100), (150, 100), (150,150), (100, 150) ] )
    env1.addObstacle("obs2", [ (575, 450), (626, 450), (650, 475), (675, 450), (725, 450), (650, 520) ] )
    env1.addObstacle("obs3", [ (423, 27), (480, 70), (350, 70) ])
    env1.addObstacle("obs4", [ (670, 80), (720, 80), (720, 150), (670, 150) ] )
    env1.addObstacle("obs5", [ (160, 410), (100, 460), (200, 460) ] )

    env1.setRobot(robot, "lightgreen")

    interface1 = Interface(env1, controleur)
    interface1.mainloop()

#q1_1()


def q1_2() :
    # pour cette question j'ai juste modifié la ligne 96 du fichier interface.py dans create obs j'ai mis le fill à 'orange'
    q1_1()

#q1_2()
    

def q1_3() :
    # pour cette question j'ai rajouté la fonction dessine dans l'interface en ligne 200 (juste après la fonction dessine_point), et j'ai rajouté deux bind
    # j'ai retiré un if a la ligne 213 de l'interface qui mettait le robot.draw = False
    # le bind avec la touche t (comme trace) permet d'activer le crayon
    # le bind avec la touche e (comme efface) permet de désactiver le crayon
    q1_1()

#q1_3()


def q1_4() :

    # J'ai modifié la fonction choisir stratégie et j'ai crée la stratégie demandée dans la question en la mettant en option 3 de cette fonction
    # j'ai bind la touche p à cette stratégie 
    controleur = Controler()
    robot = Adaptateur_simule("Rob1", 375, 275, 30, 55, 20)

    env2 = Environnement(750, 550, 1)
    T_env = Thread(target=loopEnv, args=[env2], daemon=True)
    T_env.start()

    env2.setRobot(robot, "lightgreen")

    interface1 = Interface(env2, controleur)
    interface1.mainloop()

    #la stratégie fonctionne lorsqu'on est dans un environnement sans obstacles comme celui-ci, cependant il peut y avoir des problèmes lorsqu'on a des obstacles car le capteur de distance regarde droit devant lui, et ne prend pas en compte la largeur du robot


#q1_4()

def q1_5() :

    #J'ai modifié la fonction choisir_stratégie dans l'interface pour ajouter l'option 4 avec la fonction demandée dans cette question
    # il faut utiliser la touche O pour lancer la stratégie
    controleur = Controler()
    robot = Adaptateur_simule("Robot", 700, 500, 30, 55, 20)

    env3 = Environnement(750, 550, 1)
    T_env = Thread(target=loopEnv, args=[env3], daemon=True)
    T_env.start()

    env3.setRobot(robot, "lightgreen")

    interface1 = Interface(env3, controleur)
    interface1.mainloop()

q1_5()


