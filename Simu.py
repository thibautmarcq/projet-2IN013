import logging
from threading import Thread
from time import sleep

from src.constantes import *
from src.Controleur.controleur import Controler
from src.Controleur.Strategies import *
from src.environnement import Environnement
from src.Interface.interface import Interface
from src.Robot.ballon import ballon
from src.Robot.mockupRobot import *
from src.Robot.robot import Adaptateur_simule, Robot

logging.basicConfig(filename='logs.log', 
                    level=logging.DEBUG, 
                    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s', 
                    datefmt='%d/%m/%y %H:%M:%S', 
                    encoding='UTF-8') # niveaux : DEBUG INFO WARNING ERROR CRITICAL

def loopEnv(env):
    while True:
        env.refresh_env()
        sleep(TIC_SIMULATION)

env = Environnement(750, 550, 1) # Initialisation de l'env
T_env = Thread(target=loopEnv, args=[env], daemon=True)
T_env.start()
env.addObstacle('J',[(100,100),(150,100),(150,150), (100,150)])
env.addObstacle('K',[(350,50),(400,50),(400,100), (350,100)])
env.addObstacle('L',[(600,50),(650,50),(650,100), (600,100)])
env.addObstacle('M',[(150,400),(200,400),(200,450), (150,450)])
env.addObstacle('N',[(600,400),(650,400),(650,450), (600,450)])
#env.print_matrix()

#On crée un controleur
controleur = Controler()

# # Ajoute le premier robot
# robot = Adaptateur_simule("Bob", env.width/2, env.length/2, 30, 55, 20)

# env.setRobot(robot, "lightgreen")


# # ajoute le deuxieme robot pour test
# robot2 = Adaptateur_simule("Stuart", 400, 250, 30, 55, 20)
# env.setRobot(robot2, "red")

Ballon = ballon("Bob", env.width/2, env.length/2, 30, 55, 20)
env.setRobot(ballon, "blue")
Ballon.setVitAng(20)
truc = env.robots[0]
print(truc.nom)

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