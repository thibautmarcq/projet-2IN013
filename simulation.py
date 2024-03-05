from Code.Interface.interface import Interface
from Code.environnement import Environnement
from Code.Robot.robot import Robot
from threading import Thread
from time import sleep
from Code.Controleur.controleur import Controler

def loopEnv(env):
    while True:
        env.refresh_env()
        sleep(1/2000)

env = Environnement(750, 550, 1) # Initialisation de l'env
T_env = Thread(target=loopEnv, args=[env], daemon=True)
T_env.start()
env.addObstacle('J',[(400,400),(450,450),(350,450)])
env.addObstacle('P',[(300,300),(350,300),(350,350), (300,350)])
env.addObstacle('C',[(100,140),(170,55),(160,30), (130,30), (100,50), (70,30), (40,30), (30,55)])
# env.print_matrix()

# Ajoute le premier robot
robot = Robot("Bob", 250, 250, 30, 55, 20)
env.setRobot(robot, "lightgreen")

#On créer un controleur
controleur = Controler(robot)

# ajoute le deuxieme robot pour test
robot2 = Robot("Stuart", 400, 250, 30, 55, 20)
env.setRobot(robot2, "red")

def menu():
    global RUNNING
    print("0 - Quit ( termine la simmu et arrete le programme )")
    print("1 - Lance une interface Graphique ")
    print("2 - afficher les infos de la simulation")
    cmd = input("Veuillez choisir une action:")
    if cmd == "0":
        RUNNING = False
    elif cmd == "1":
        run = Interface(env, controleur)
        run.mainloop()
    elif cmd == "2":
        print("Information de la simulation:")
        print("Width:", env.width, "Length:", env.length)
        print("Nombre de robots dans notre simulation:", len(env.robots))
        for rob in env.robots:
            print("------ Robot",rob.nom,"------")
            print(f"vitAngG = {rob.vitAngG}, vitAngD = {rob.vitAngD}")
            print(f"Coords: ({rob.x},{rob.y}), Width: {rob.width}, Length: {rob.length}")
            print("Le robot n'est plus fonctionnel"if rob.estCrash else "Le robot est toujours fonctionnel")
            print("Le robot n'est pas controlé par le controleur"if not rob.estSousControle else "Le robot est controlé par le controlleur")
            print("------------"+"-"*(len(rob.nom)+2)+"------")



RUNNING = True

while RUNNING:
    menu()